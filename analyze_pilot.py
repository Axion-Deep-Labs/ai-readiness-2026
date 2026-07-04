#!/usr/bin/env python3
"""
Analyze a pilot crawl, joined to the OSM sample metadata.

Reports AI-readiness adoption overall and by stratum / vertical / city, plus the
AI-Readiness index distribution and per-cell counts (for variance / sample sizing).

Usage:  python3 analyze_pilot.py results/pilot_<stamp>.jsonl [sample_meta.csv]
"""
import sys, json, csv, statistics
from collections import defaultdict, Counter

INDEX_POINTS = [  # pre-registered rubric (PROTOCOL Section 9)
    ("allows_ai",   lambda r: len(r.get("ai_bots_blocked", [])) == 0, 2),
    ("llms",        lambda r: r.get("llms_txt", {}).get("present"),   2),
    ("identity",    lambda r: r.get("has_identity_schema"),           2),
    ("trust",       lambda r: r.get("has_trust_schema"),              2),
    ("faq",         lambda r: r.get("has_qa_schema"),                 1),
    ("person",      lambda r: r.get("has_person_schema"),             1),
]

METRICS = [
    ("reachable",      lambda r: r.get("home_status") == 200),
    ("identity schema",lambda r: r.get("has_identity_schema")),
    ("trust schema",   lambda r: r.get("has_trust_schema")),
    ("FAQ schema",     lambda r: r.get("has_qa_schema")),
    ("person schema",  lambda r: r.get("has_person_schema")),
    ("llms.txt",       lambda r: r.get("llms_txt", {}).get("present")),
    ("blocks AI bot",  lambda r: len(r.get("ai_bots_blocked", [])) > 0),
]


def pct(rows, f):
    if not rows:
        return "  n/a"
    return f"{100*sum(1 for r in rows if f(r))/len(rows):4.0f}%"


def index_score(r):
    return sum(pts for _, f, pts in INDEX_POINTS if f(r))


def main(path, meta_path="sample_meta.csv"):
    rows = [json.loads(l) for l in open(path)]
    meta = {}
    try:
        for m in csv.DictReader(open(meta_path)):
            meta[m["domain"]] = m
    except FileNotFoundError:
        pass
    for r in rows:
        m = meta.get(r["domain"], {})
        r["vertical"] = m.get("vertical", "?")
        r["city"] = m.get("city", "?")
        r["stratum"] = m.get("stratum", "?")

    print("=" * 78)
    print(f"AI-READINESS PILOT ANALYSIS   n={len(rows)}   ({path})")
    print("=" * 78)

    # overall
    print("\nOVERALL")
    for name, f in METRICS:
        print(f"  {name:16} {pct(rows, f)}")

    # by grouping
    for key in ("stratum", "vertical", "city"):
        groups = defaultdict(list)
        for r in rows:
            groups[r[key]].append(r)
        print(f"\nBY {key.upper()}")
        header = "  " + f"{key:14}" + "n   " + "".join(f"{n[:9]:>10}" for n, _ in METRICS)
        print(header)
        for g, rs in sorted(groups.items()):
            line = f"  {g:14}{len(rs):<4}" + "".join(f"{pct(rs, f):>10}" for _, f in METRICS)
            print(line)

    # AI-Readiness index
    scores = [index_score(r) for r in rows]
    print("\nAI-READINESS INDEX (0-10)")
    print(f"  mean {statistics.mean(scores):.1f}   median {statistics.median(scores)}   "
          f"min {min(scores)}   max {max(scores)}")
    dist = Counter(scores)
    for s in range(0, 11):
        bar = "#" * dist.get(s, 0)
        print(f"  {s:2}: {dist.get(s,0):3} {bar}")

    # llms.txt provenance (plugin-driven adoption finding)
    prov = Counter(r["llms_txt"].get("provenance") for r in rows
                   if r.get("llms_txt", {}).get("present"))
    if prov:
        tot = sum(prov.values())
        print("\nLLMS.TXT PROVENANCE (of sites that have one)")
        for p, n in prov.most_common():
            print(f"  {str(p):16} {n:3}  ({100*n/tot:.0f}%)")

    # platform mix
    print("\nPLATFORM MIX")
    for p, n in Counter(r.get("platform", "?") for r in rows).most_common():
        print(f"  {p:14} {n}")

    # per-cell counts (variance / sizing)
    print("\nPER-CELL COUNTS (for sample sizing)")
    cells = Counter((r["stratum"], r["vertical"]) for r in rows)
    thin = [c for c, n in cells.items() if n < 8]
    print(f"  cells: {len(cells)}   thin cells (n<8): {len(thin)}")
    if thin:
        print("  thin: " + ", ".join(f"{s}/{v}={cells[(s,v)]}" for s, v in sorted(thin)))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python3 analyze_pilot.py results/pilot_<stamp>.jsonl [sample_meta.csv]")
        sys.exit(1)
    main(*sys.argv[1:])
