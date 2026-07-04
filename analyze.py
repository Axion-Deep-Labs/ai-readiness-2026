#!/usr/bin/env python3
"""
Paper-grade analyzer: bootstrap 95% CIs, reachable-only denominators.

Fixes vs analyze_pilot.py:
  - adoption metrics computed over REACHABLE sites (dead URLs are not "no schema")
  - bootstrap 95% confidence intervals on every headline proportion + the index
  - review-schema-by-vertical reported with CIs (the CPA-vs-lawyer gap, with error bars)

Usage:  python3 analyze.py results/crawl_<stamp>.jsonl [sample_meta.csv]
"""
import sys, json, csv, random, statistics, math
from collections import defaultdict, Counter

BOOT, SEED = 2000, 12345
Z = 1.959964  # 95% normal quantile

METRICS = [
    ("identity schema", lambda r: r["has_identity_schema"]),
    ("review schema",   lambda r: r["has_trust_schema"]),
    ("FAQ schema",      lambda r: r["has_qa_schema"]),
    ("person schema",   lambda r: r["has_person_schema"]),
    ("llms.txt",        lambda r: r["llms_txt"].get("present")),
    ("blocks AI bot",   lambda r: len(r["ai_bots_blocked"]) > 0),
]
INDEX = [(lambda r: len(r["ai_bots_blocked"]) == 0, 2), (lambda r: r["llms_txt"].get("present"), 2),
         (lambda r: r["has_identity_schema"], 2), (lambda r: r["has_trust_schema"], 2),
         (lambda r: r["has_qa_schema"], 1), (lambda r: r["has_person_schema"], 1)]


def boot_ci(vals, stat, n=BOOT):
    if not vals:
        return (float("nan"), float("nan"))
    rng = random.Random(SEED)
    N = len(vals)
    est = sorted(stat([vals[rng.randrange(N)] for _ in range(N)]) for _ in range(n))
    return est[int(0.025 * n)], est[int(0.975 * n)]


def wilson_ci(x, n):
    """Wilson score 95% interval for a binomial proportion, in percent.

    Well-behaved at the boundaries (x=0 or x=n), where the percentile
    bootstrap degenerates to a zero-width interval. Used for every
    proportion in the paper; the bootstrap is reserved for the index mean.
    """
    if n == 0:
        return float("nan"), float("nan")
    p = x / n
    denom = 1 + Z * Z / n
    center = (p + Z * Z / (2 * n)) / denom
    half = (Z / denom) * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n))
    return 100 * max(0.0, center - half), 100 * min(1.0, center + half)


def prop_ci(rows, f):
    bits = [1 if f(r) else 0 for r in rows]
    n = len(bits)
    x = sum(bits)
    p = 100 * (x / n) if n else float("nan")
    lo, hi = wilson_ci(x, n)
    return p, lo, hi


def fmt(rows, f):
    p, lo, hi = prop_ci(rows, f)
    return f"{p:4.0f}% [{lo:2.0f}-{hi:2.0f}]"


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
        r["vertical"], r["stratum"] = m.get("vertical", "?"), m.get("stratum", "?")

    N = len(rows)
    reach = [r for r in rows if r.get("reachable")]
    print("=" * 74)
    print(f"AI-READINESS  (paper-grade)   N={N}   reachable={len(reach)}")
    print("=" * 74)
    rp, rlo, rhi = prop_ci(rows, lambda r: r.get("reachable"))
    print(f"\nReachability: {rp:.0f}% [{rlo:.0f}-{rhi:.0f}]   "
          f"(adoption below is among the {len(reach)} reachable sites)")

    print("\nOVERALL ADOPTION (95% CI)")
    for name, f in METRICS:
        print(f"  {name:16} {fmt(reach, f)}")

    print("\nREVIEW-SCHEMA BY VERTICAL (the CPA-vs-lawyer gap, with CIs)")
    byv = defaultdict(list)
    for r in reach:
        byv[r["vertical"]].append(r)
    for v, rs in sorted(byv.items(), key=lambda kv: -prop_ci(kv[1], METRICS[1][1])[0]):
        print(f"  {v:14} n={len(rs):3}   review {fmt(rs, METRICS[1][1])}   "
              f"identity {fmt(rs, METRICS[0][1])}   person {fmt(rs, METRICS[3][1])}")

    print("\nBY STRATUM (point estimates)")
    bys = defaultdict(list)
    for r in reach:
        bys[r["stratum"]].append(r)
    hdr = "  " + f"{'stratum':11}" + "n    " + "".join(f"{n[:8]:>9}" for n, _ in METRICS)
    print(hdr)
    for s, rs in sorted(bys.items()):
        line = f"  {s:11}{len(rs):<5}" + "".join(
            f"{100*sum(1 for r in rs if f(r))/len(rs):8.0f}%" for _, f in METRICS)
        print(line)

    # index
    scores = [sum(pts for f, pts in INDEX if f(r)) for r in reach]
    m = statistics.mean(scores)
    lo, hi = boot_ci(scores, statistics.mean)
    print(f"\nAI-READINESS INDEX (0-10, reachable): mean {m:.2f} [{lo:.2f}-{hi:.2f}]  "
          f"median {statistics.median(scores)}")
    dist = Counter(scores)
    at2 = 100 * dist.get(2, 0) / len(scores)
    print(f"  {dist.get(2,0)} sites ({at2:.0f}%) score exactly 2/10 (allows AI, nothing else)")

    prov = Counter(r["llms_txt"].get("provenance") for r in reach if r["llms_txt"].get("present"))
    if prov:
        tot = sum(prov.values())
        gen = sum(n for p, n in prov.items() if p != "manual")
        print(f"\nLLMS.TXT PROVENANCE (n={tot} with llms.txt): "
              f">={100*gen/tot:.0f}% tool-generated")
        for p, n in prov.most_common():
            print(f"    {str(p):16} {n:3} ({100*n/tot:.0f}%)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python3 analyze.py results/crawl_<stamp>.jsonl [sample_meta.csv]")
        sys.exit(1)
    main(*sys.argv[1:])
