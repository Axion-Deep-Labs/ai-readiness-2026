#!/usr/bin/env python3
"""
Build a stratified sample of local-business websites from OpenStreetMap (free).
v2: 15 cities (3 per stratum), Overpass retry/backoff, aggregator filtering.

Emits: seed_wave1.txt (domains) + sample_meta.csv (domain,vertical,city,stratum)
Usage: python3 build_sample.py  [--limit-cells N]
"""
import sys, csv, time, json, argparse, urllib.request, urllib.parse, ssl
from urllib.parse import urlparse

OVERPASS = "https://maps.mail.ru/osm/tools/overpass/api/interpreter"  # reachable mirror
CTX = ssl.create_default_context()
UA = "Mozilla/5.0 (compatible; AxionDeepDigitalResearch/0.1; +https://axiondeepdigital.com)"

# 3 cities per stratum. Bounding boxes (S, W, N, E).
CITIES = {
    "San Francisco": ("metro",      (37.70, -122.52, 37.83, -122.35)),
    "Chicago":       ("metro",      (41.80,  -87.75, 41.98,  -87.55)),
    "Dallas":        ("metro",      (32.70,  -96.90, 32.90,  -96.70)),
    "Tucson":        ("mid",        (32.10, -111.10, 32.35, -110.80)),
    "Boise":         ("mid",        (43.55, -116.30, 43.70, -116.15)),
    "Grand Rapids":  ("mid",        (42.90,  -85.72, 43.02,  -85.58)),
    "Bozeman":       ("small",      (45.63, -111.12, 45.72, -110.93)),
    "Dubuque":       ("small",      (42.46,  -90.75, 42.55,  -90.63)),
    "Missoula":      ("small",      (46.83, -114.10, 46.92, -113.94)),
    "Sedona":        ("tourism",    (34.80, -111.86, 34.93, -111.70)),
    "Asheville":     ("tourism",    (35.53,  -82.62, 35.63,  -82.50)),
    "Key West":      ("tourism",    (24.54,  -81.81, 24.58,  -81.74)),
    "Ann Arbor":     ("university", (42.22,  -83.80, 42.33,  -83.66)),
    "Ithaca":        ("university", (42.42,  -76.53, 42.47,  -76.47)),
    "Madison":       ("university", (43.03,  -89.50, 43.14,  -89.32)),
}

VERTICALS = {
    "accounting":   '["office"~"accountant|tax_advisor"]',
    "dentist":      '["amenity"="dentist"]',
    "lawyer":       '["office"="lawyer"]',
    "plumber":      '["craft"="plumber"]',
    "real_estate":  '["office"="estate_agent"]',
    "beauty_medspa":'["shop"="beauty"]',
    "hvac":         '["craft"="hvac"]',
    "chiropractor": '["healthcare"="chiropractor"]',
    "veterinary":   '["amenity"="veterinary"]',
    "auto_repair":  '["shop"="car_repair"]',
    "optician":     '["shop"="optician"]',
}

SKIP_DOMAINS = {"facebook.com", "instagram.com", "twitter.com", "x.com", "linktr.ee",
                "yelp.com", "linkedin.com", "google.com", "sites.google.com",
                "wixsite.com", "business.site", "godaddysites.com", "youtube.com",
                "tiktok.com", "wordpress.com", "blogspot.com", "square.site"}
MAX_PER_CELL = 35


def domain_of(url):
    if not url:
        return None
    if not url.startswith("http"):
        url = "http://" + url
    try:
        d = urlparse(url).netloc.lower().split(":")[0]
        return d[4:] if d.startswith("www.") else (d or None)
    except Exception:
        return None


def overpass(bbox, tagfilter, retries=2):
    s, w, n, e = bbox
    q = f'[out:json][timeout:120];(nwr{tagfilter}["website"]({s},{w},{n},{e}););out tags 120;'
    data = urllib.parse.urlencode({"data": q}).encode()
    last = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(OVERPASS, data=data, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=150, context=CTX) as resp:
                return json.loads(resp.read().decode("utf-8", "replace"))
        except Exception as ex:
            last = ex
            if attempt < retries:
                time.sleep(6 * (attempt + 1))
    raise last


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit-cells", type=int, default=0)
    args = ap.parse_args()

    cells = [(c, v) for c in CITIES for v in VERTICALS]
    if args.limit_cells:
        cells = cells[:args.limit_cells]

    seen, meta = set(), []
    for city, vertical in cells:
        stratum, bbox = CITIES[city]
        try:
            js = overpass(bbox, VERTICALS[vertical])
        except Exception as ex:
            print(f"  [{city}/{vertical}] Overpass FAILED after retries: {ex}")
            continue
        added = 0
        for el in js.get("elements", []):
            d = domain_of(el.get("tags", {}).get("website"))
            if not d or d in seen:
                continue
            if d in SKIP_DOMAINS or any(d.endswith("." + s) for s in SKIP_DOMAINS):
                continue
            seen.add(d)
            meta.append({"domain": d, "vertical": vertical, "city": city, "stratum": stratum})
            added += 1
            if added >= MAX_PER_CELL:
                break
        print(f"  [{city:14}/{vertical:13}] +{added:2}  (total {len(seen)})")
        time.sleep(3)

    with open("seed_wave1.txt", "w") as f:
        f.write("\n".join(sorted(seen)) + "\n")
    with open("sample_meta.csv", "w", newline="") as f:
        wri = csv.DictWriter(f, fieldnames=["domain", "vertical", "city", "stratum"])
        wri.writeheader(); wri.writerows(meta)
    print(f"\nWrote {len(seen)} unique domains to seed_wave1.txt + sample_meta.csv")


if __name__ == "__main__":
    main()
