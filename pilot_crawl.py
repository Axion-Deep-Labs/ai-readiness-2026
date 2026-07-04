#!/usr/bin/env python3
"""
Calibration pilot crawler for the AI-Readiness study.

For each domain, fetches THREE public resources (free HTTP, stdlib only):
  1. /robots.txt   -> AI-crawler permission (blocked / mentioned / not mentioned)
  2. /llms.txt     -> guidance-file adoption (present? size? structure?)
  3. homepage      -> schema.org @types (structure) + platform fingerprint

Purpose is INSTRUMENT VALIDATION, not confirmatory data. The six CPA sites in
the seed are ground truth for the schema extractor (we read them by hand earlier).

Usage:
  python3 pilot_crawl.py                 # all seed sites
  python3 pilot_crawl.py --limit 6       # first 6 (the CPA ground-truth set)
  python3 pilot_crawl.py --seed file.txt # custom domain list (one per line)
Out:
  results/pilot_<UTC>.jsonl  + a printed summary
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
            "Store", "Corporation", "LegalService"}
TRUST = {"Review", "AggregateRating"}
QA = {"FAQPage", "QAPage"}


def get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=CTX) as resp:
            raw = resp.read()
            enc = resp.headers.get_content_charset() or "utf-8"
            return {"status": resp.status, "text": raw.decode(enc, "replace"),
                    "url": resp.geturl(), "headers": dict(resp.headers)}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "text": "", "url": url, "headers": dict(e.headers or {})}
    except Exception as e:
        return {"status": None, "text": "", "url": url, "headers": {}, "error": str(e)}


def parse_robots(text):
    """Group robots.txt by user-agent; per AI bot: blocked_all / mentioned / not_mentioned."""
    groups, agents, dis = [], [], []
    prev_was_dis = False
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        field, val = line.split(":", 1)
        field, val = field.strip().lower(), val.strip()
        if field == "user-agent":
            if prev_was_dis and agents:
                groups.append((agents, dis)); agents, dis = [], []
            agents.append(val); prev_was_dis = False
        elif field in ("disallow", "allow"):
            if field == "disallow":
                dis.append(val)
            prev_was_dis = True
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
            data = json.loads(m.group(1).strip())
        except Exception:
            continue
        for t in walk_types(data):
            types.add(t)
    return sorted(types)


def detect_platform(html, headers):
    h = html.lower()
    for key, name in [("wp-content", "WordPress"), ("cdn.shopify", "Shopify"),
                      ("wixstatic", "Wix"), ("parastorage", "Wix"),
                      ("squarespace", "Squarespace"), ("webflow", "Webflow"),
                      ("static.parastorage", "Wix"), ("dudamobile", "Duda")]:
        if key in h:
            return name
    powered = (headers.get("X-Powered-By") or headers.get("x-powered-by") or "")
    if "php" in powered.lower():
        return "PHP/other"
    return "unknown"


def check_llms(base):
    r = get(base.rstrip("/") + "/llms.txt")
    if not r or r["status"] != 200 or not r["text"].strip():
        return {"present": False}
    body = r["text"]
    if "<html" in body[:600].lower():
        return {"present": False, "note": "soft404_html"}
    return {"present": True, "bytes": len(body),
            "headings": len(re.findall(r'^#', body, re.M)),
            "links": len(re.findall(r'\]\(http', body))}


def crawl(domain):
    base = "https://" + domain.strip().strip("/")
    rec = {"domain": domain, "timestamp_utc": datetime.now(timezone.utc).isoformat()}

    home = get(base)
    html = home["text"] if home else ""
    rec["home_status"] = home["status"] if home else None
    rec["platform"] = detect_platform(html, home["headers"]) if home and html else "unknown"
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
        rec["robots"] = None
        rec["ai_bots_blocked"] = []

    rec["llms_txt"] = check_llms(base)
    return rec


SEED = """capitaltax.com
joewucpa.com
jsscpa.com
thecreek.cpa
pattencpaco.com
carolkeanecpa.com
nytimes.com
reddit.com
theatlantic.com
en.wikipedia.org
shopify.com
squarespace.com
stripe.com
perplexity.ai""".split()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", help="file with one domain per line")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    domains = [l.strip() for l in open(args.seed) if l.strip()] if args.seed else SEED
    if args.limit:
        domains = domains[:args.limit]

    os.makedirs("results", exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = os.path.join("results", f"pilot_{stamp}.jsonl")

    rows = []
    with open(out_path, "w") as out:
        for d in domains:
            rec = crawl(d)
            out.write(json.dumps(rec) + "\n")
            rows.append(rec)
            blocked = ",".join(b for b in rec["ai_bots_blocked"]) or "none"
            llms = "yes" if rec["llms_txt"].get("present") else "no"
            print(f"  {d:22} plat={rec['platform']:11} schema={len(rec['schema_types']):2} "
                  f"id={int(rec['has_identity_schema'])} rev={int(rec['has_trust_schema'])} "
                  f"llms={llms}  AI-blocked=[{blocked}]")
            time.sleep(0.7)

    # summary
    n = len(rows)
    def pct(f):
        return f"{100*sum(1 for r in rows if f(r))/max(n,1):.0f}%"
    print("\n" + "=" * 60)
    print(f"PILOT SUMMARY  (n={n})")
    print("=" * 60)
    print(f"  homepage reachable:        {pct(lambda r: r['home_status']==200)}")
    print(f"  has identity schema:       {pct(lambda r: r['has_identity_schema'])}")
    print(f"  has trust/review schema:   {pct(lambda r: r['has_trust_schema'])}")
    print(f"  has FAQ schema:            {pct(lambda r: r['has_qa_schema'])}")
    print(f"  has llms.txt:              {pct(lambda r: r['llms_txt'].get('present'))}")
    print(f"  blocks >=1 AI crawler:     {pct(lambda r: len(r['ai_bots_blocked'])>0)}")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
