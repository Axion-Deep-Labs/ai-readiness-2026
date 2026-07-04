#!/usr/bin/env python3
"""
Confirmatory-grade AI-readiness crawler (v2 of pilot_crawl.py).

Improvements from the pilot (PROTOCOL Appendix C):
  - reachability retry + http fallback
  - llms.txt validity (reject HTML/redirect stubs, tiny files, non-markdown)
    and PROVENANCE detection (Rank Math / Yoast / other-generated / manual)
  - expanded platform fingerprints (headers + HTML)

Output rows are compatible with analyze_pilot.py (same core fields).
Usage:  python3 crawl.py --seed seed_wave1.txt
Out:    results/crawl_<UTC>.jsonl + summary
"""
import sys, os, re, json, time, ssl, argparse
import urllib.request, urllib.error
from datetime import datetime, timezone

AI_BOTS = ["GPTBot", "ChatGPT-User", "OAI-SearchBot", "Google-Extended", "ClaudeBot",
           "anthropic-ai", "Claude-Web", "PerplexityBot", "Perplexity-User", "CCBot",
           "Bytespider", "Amazonbot", "Applebot-Extended", "Meta-ExternalAgent"]
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AxionDeepDigitalResearch/0.1; +https://axiondeepdigital.com)"}
TIMEOUT = 15
CTX = ssl.create_default_context()

IDENTITY = {"Organization", "LocalBusiness", "AccountingService", "ProfessionalService",
            "Attorney", "Dentist", "MedicalBusiness", "HomeAndConstructionBusiness",
            "Store", "Corporation", "LegalService", "RealEstateAgent", "HealthAndBeautyBusiness",
            "DaySpa", "BeautySalon", "Plumber"}
TRUST = {"Review", "AggregateRating"}
QA = {"FAQPage", "QAPage"}


def get(url, retries=1):
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=TIMEOUT, context=CTX) as resp:
                raw = resp.read()
                enc = resp.headers.get_content_charset() or "utf-8"
                return {"status": resp.status, "text": raw.decode(enc, "replace"),
                        "url": resp.geturl(), "headers": dict(resp.headers)}
        except urllib.error.HTTPError as e:
            return {"status": e.code, "text": "", "url": url, "headers": dict(e.headers or {})}
        except Exception as e:
            if attempt < retries:
                time.sleep(1.5); continue
            return {"status": None, "text": "", "url": url, "headers": {}, "error": str(e)}


def parse_robots(text):
    groups, agents, dis, prev_dis = [], [], [], False
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        field, val = line.split(":", 1)
        field, val = field.strip().lower(), val.strip()
        if field == "user-agent":
            if prev_dis and agents:
                groups.append((agents, dis)); agents, dis = [], []
            agents.append(val); prev_dis = False
        elif field in ("disallow", "allow"):
            if field == "disallow":
                dis.append(val)
            prev_dis = True
    if agents:
        groups.append((agents, dis))
    out = {}
    for bot in AI_BOTS:
        status = "not_mentioned"
        for ags, dss in groups:
            if any(a.lower() == bot.lower() for a in ags):
                status = "blocked_all" if any(d == "/" for d in dss) else "mentioned"
                break
        out[bot] = status
    return out


def walk_types(obj):
    out = []
    if isinstance(obj, dict):
        t = obj.get("@type")
        if isinstance(t, list):
            out += [str(x) for x in t]
        elif t:
            out.append(str(t))
        for v in obj.values():
            out += walk_types(v)
    elif isinstance(obj, list):
        for x in obj:
            out += walk_types(x)
    return out


def extract_schema(html):
    types = set()
    for m in re.finditer(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', html, re.S | re.I):
        try:
            types.update(walk_types(json.loads(m.group(1).strip())))
        except Exception:
            continue
    return sorted(types)


def detect_platform(html, headers):
    h = html.lower()
    hdr = " ".join(f"{k}:{v}" for k, v in headers.items()).lower()
    fp = [("wp-content", "WordPress"), ("wp-json", "WordPress"), ("cdn.shopify", "Shopify"),
          ("myshopify", "Shopify"), ("wixstatic", "Wix"), ("parastorage", "Wix"),
          ("squarespace", "Squarespace"), ("webflow", "Webflow"), ("dudaone", "Duda"),
          ("dudamobile", "Duda"), ("editmysite", "Weebly"), ("weebly", "Weebly"),
          ("hs-scripts", "HubSpot"), ("hubspot", "HubSpot"), ("_next/static", "Next.js"),
          ("drupal", "Drupal"), ("joomla", "Joomla"), ("godaddy", "GoDaddy")]
    for k, name in fp:
        if k in h or k in hdr:
            return name
    xgen = (headers.get("X-Generator") or headers.get("x-generator") or "").lower()
    if "wordpress" in xgen: return "WordPress"
    if "drupal" in xgen: return "Drupal"
    if "wix" in xgen: return "Wix"
    powered = (headers.get("X-Powered-By") or headers.get("x-powered-by") or "").lower()
    if "asp.net" in powered: return "ASP.NET"
    if "php" in powered: return "PHP/other"
    return "unknown"


HTML_MARKERS = ("<html", "<!doctype", "301 moved", "302 found", "<head", "<body",
                "not found", "<?xml", "page not found")


def check_llms(base):
    r = get(base.rstrip("/") + "/llms.txt")
    if not r or r["status"] != 200:
        return {"present": False, "reason": "no_200"}
    body = r["text"]
    head = body[:1024].lower()
    if any(m in head for m in HTML_MARKERS):
        return {"present": False, "reason": "html_or_stub"}
    if len(body.strip()) < 40:
        return {"present": False, "reason": "too_small"}
    if not (("#" in body) or ("](http" in body)):
        return {"present": False, "reason": "no_markdown"}
    low = body[:500].lower()
    prov = "manual"
    if "rank math" in low: prov = "RankMath"
    elif "yoast" in low: prov = "Yoast"
    elif "generated by" in low: prov = "generated_other"
    return {"present": True, "bytes": len(body), "provenance": prov,
            "headings": len(re.findall(r'^#', body, re.M)),
            "links": len(re.findall(r'\]\(http', body))}


def crawl(domain):
    domain = domain.strip().strip("/")
    rec = {"domain": domain, "timestamp_utc": datetime.now(timezone.utc).isoformat()}
    base = "https://" + domain
    home = get(base, retries=1)
    if (not home or home["status"] != 200 or not home["text"]):
        alt = get("http://" + domain, retries=1)   # http fallback
        if alt and alt["status"] == 200 and alt["text"]:
            home, base = alt, "http://" + domain
    html = home["text"] if home else ""
    rec["home_status"] = home["status"] if home else None
    rec["reachable"] = bool(html)
    rec["platform"] = detect_platform(html, home["headers"]) if html else "unknown"
    rec["schema_types"] = extract_schema(html) if html else []
    st = set(rec["schema_types"])
    rec["has_identity_schema"] = bool(st & IDENTITY)
    rec["has_trust_schema"] = bool(st & TRUST)
    rec["has_qa_schema"] = bool(st & QA)
    rec["has_person_schema"] = "Person" in st

    rob = get(base + "/robots.txt")
    if rob and rob["status"] == 200 and rob["text"].strip() and "<html" not in rob["text"][:600].lower():
        rec["robots"] = parse_robots(rob["text"])
        rec["ai_bots_blocked"] = sorted(b for b, s in rec["robots"].items() if s == "blocked_all")
    else:
        rec["robots"], rec["ai_bots_blocked"] = None, []

    rec["llms_txt"] = check_llms(base)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", default="seed_wave1.txt")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    domains = [l.strip() for l in open(args.seed) if l.strip()]
    if args.limit:
        domains = domains[:args.limit]

    os.makedirs("results", exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = os.path.join("results", f"crawl_{stamp}.jsonl")
    rows = []
    with open(out_path, "w") as out:
        for i, d in enumerate(domains, 1):
            rec = crawl(d)
            out.write(json.dumps(rec) + "\n"); out.flush()
            rows.append(rec)
            if i % 25 == 0:
                print(f"  ...{i}/{len(domains)}")
            time.sleep(0.6)

    n = len(rows)
    reach = [r for r in rows if r["reachable"]]
    def pct(rs, f): return f"{100*sum(1 for r in rs if f(r))/max(len(rs),1):.0f}%"
    print(f"\nCRAWL DONE  n={n}  reachable={len(reach)} ({pct(rows, lambda r: r['reachable'])})")
    print(f"  (of reachable) identity={pct(reach, lambda r: r['has_identity_schema'])} "
          f"trust={pct(reach, lambda r: r['has_trust_schema'])} "
          f"llms={pct(reach, lambda r: r['llms_txt'].get('present'))} "
          f"blocksAI={pct(reach, lambda r: len(r['ai_bots_blocked'])>0)}")
    print(f"Wrote {out_path}\nNext: python3 analyze_pilot.py {out_path} sample_meta.csv")


if __name__ == "__main__":
    main()
