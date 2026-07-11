# The State of AI-Readiness on Business Websites (2026)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21312372.svg)](https://doi.org/10.5281/zenodo.21312372)

Open data, code, and protocol for the working paper *The State of AI-Readiness on Business Websites
(2026): A Large-Scale Measurement of AI-Crawler Permission, llms.txt Adoption, and Structured-Data
Readiness.*

**Author:** Joshua R. Gutierrez, Axion Deep Labs, Inc. · Contact: hello@axiondeep.com
**Paper (SSRN):** `AI_Readiness_2026_SSRN.pdf` (this repo) · SSRN abstract 7057078 — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7057078 (submitted 2026-07-04, under moderation review).
**Preregistration:** https://osf.io/2q5er/ — confirmatory ≥1,000-site wave (plan: `osf_prereg.md`). The figures in this repo are the exploratory precursor.

## What this measures

We define **AI-readiness** operationally as adoption of three public, machine-checkable signals a
business fully controls: whether it permits AI crawlers (`robots.txt`), whether it guides them
(`llms.txt`), and whether it is structured for machine identification (`schema.org`). We measure
these across a stratified sample of local-business websites (n=766, 10 verticals, 15 cities) drawn
from OpenStreetMap. This is a supply-side study: it measures what businesses expose, not how AI
engines behave.

## Headline results (reachable n=594)

- Review/AggregateRating markup: **9%** (95% CI 7–11); FAQ: **4%** (3–6); identity: **49%** (45–53).
- Modal business scores **2/10** on the AI-Readiness index (42% of reachable sites).
- **Accounting** firms: **0% review, 0% Person** markup (0/27; Wilson CI 0–12), non-overlapping with
  **legal** firms (review 26%, CI 18–35). Accounting is the only vertical simultaneously at 0%
  review, 0% Person, and lowest identity.
- Valid **llms.txt**: 25% (22–29); at least 28% tool-generated (lower bound).
- Only **4%** block any AI crawler (3–6).
- Figures replicate across the 149-, 487-, and 766-site samples.

## Repository layout

```
data/
  crawl_confirmatory_766.jsonl   primary crawl (paper figures; reachable n=594)
  crawl_replication_487.jsonl    replication sample
  crawl_pilot_149.jsonl          pilot / first replication
sample_meta.csv                  domain -> vertical, city, stratum (the query frame)
seed_wave1.txt                   crawl seed (766 domains)
build_sample.py                  build the stratified OSM sample
crawl.py                         confirmatory crawler (public HTTP only)
analyze.py                       Wilson-CI analyzer (reproduces all paper numbers)
pilot_crawl.py, analyze_pilot.py pilot instrument (superseded by crawl.py/analyze.py)
PROTOCOL.md                      full measurement protocol
osf_prereg.md                    preregistration
CODEBOOK.md                      field-by-field definitions, schema sets, AI-crawler list
PAPER_DRAFT.md                   working-paper source (markdown)
AI_Readiness_2026_SSRN.pdf/.tex  submission PDF + LaTeX source
```

## Reproduce the paper's numbers

```bash
python3 analyze.py data/crawl_confirmatory_766.jsonl sample_meta.csv
```

No dependencies beyond the Python 3 standard library. Analysis is deterministic (fixed seed 12345).

## Re-run the crawl (optional)

```bash
python3 crawl.py --seed seed_wave1.txt      # writes results/crawl_<UTC>.jsonl
```

The crawler fetches only public `robots.txt`, `/llms.txt`, and homepage HTML with a self-identifying
user-agent, at ~0.6s/site. Adoption on the live web drifts, so a fresh crawl will not reproduce the
frozen dataset exactly; use the committed `data/` files to reproduce the paper.

## Licenses

- **Code** (`*.py`): MIT — see `LICENSE`.
- **Data** (`data/`, `sample_meta.csv`, `seed_wave1.txt`): CC BY 4.0 — see `LICENSE-DATA`.

Raw HTML is not redistributed; only parsed fields are released (see `CODEBOOK.md`).

## Citation

```
Gutierrez, J. R. (2026). The State of AI-Readiness on Business Websites (2026):
A Large-Scale Measurement of AI-Crawler Permission, llms.txt Adoption, and
Structured-Data Readiness. Axion Deep Labs working paper.
```
