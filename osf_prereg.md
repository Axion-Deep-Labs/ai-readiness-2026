# OSF Pre-Registration (submission-ready)
## The State of AI-Readiness on Business Websites (2026)

Submit this on osf.io (Registrations > new, "OSF Preregistration" template). The full
methodology is in PROTOCOL.md; this is the condensed registration form. Register BEFORE
the confirmatory crawl. The 149-site and 487-site runs are exploratory calibration and are
disclosed as such (Appendices B, C, D of PROTOCOL.md).

### 1. Title
The State of AI-Readiness on Business Websites (2026): AI-crawler permission, llms.txt
adoption, and structured-data readiness across business verticals.

### 2. Hypotheses
Neutral. We register the analysis plan, not specific adoption rates.
- H1: Adoption of the three signals (AI-crawler permission, llms.txt, schema) is non-uniform
  and varies by vertical and platform.
- H2: There is a measurable entity-and-trust schema gap: Review/AggregateRating and Person
  markup are present on a small minority of homepages.
- H3: Adoption differs significantly across verticals (specifically, we will test whether
  Review-schema prevalence differs between professional-service verticals).
- No hypothesis pre-registers which source or vertical "wins."

### 3. Design plan
Cross-sectional observational web measurement. Unit = registrable domain. No manipulation,
no blinding. Each site is measured once (confirmatory wave); a longitudinal arm re-measures
periodically. Three public resources per site: robots.txt, /llms.txt, homepage HTML.

### 4. Sampling plan
- Frame: OpenStreetMap POIs carrying a `website` tag, selected by category (local-service
  verticals) and by five geographic strata (metro, mid, small, tourism, university), plus a
  Tranco slice for non-local verticals in later waves.
- Confirmatory sample size: target >= 1,000 reachable sites, with >= 40 reachable sites per
  (stratum) and per (vertical) cell where the frame permits; underpowered rural/tourism cells
  are pooled and flagged rather than dropped.
- Stopping rule: fixed frame and per-cell caps defined before collection; no data-dependent
  stopping.

### 5. Variables
- Measured (per site): reachability; set of schema.org @type values (homepage JSON-LD);
  derived booleans has_identity / has_review / has_faq / has_person; robots.txt status per
  AI crawler (versioned list) -> blocks_any_AI; llms.txt present (validated: not HTML/redirect
  stub, >= 40 bytes, markdown structure) with provenance (Rank Math / Yoast / other-generated /
  no-signature); detected platform.
- Index (pre-registered, additive, max 10): allows AI crawlers +2; valid llms.txt +2; identity
  schema +2; review schema +2; FAQ schema +1; Person schema +1.
- Grouping: vertical, stratum, city, platform.

### 6. Analysis plan
- Denominator: adoption proportions computed over REACHABLE sites; reachability reported
  separately. Non-reachable sites are excluded from adoption metrics (they yield no signal),
  and the exclusion rate is reported.
- Inference: bootstrap 95% confidence intervals (>= 2000 resamples, site as the resampling
  unit, fixed seed) on every proportion and on the index mean. Between-vertical differences
  tested with chi-square / permutation tests; family-wise correction (Benjamini-Hochberg).
- Primary comparison (H3): Review-schema prevalence across verticals, reported with
  non-overlapping-CI and permutation-test evidence.
- Weighting: estimates reported unweighted and re-weighted to a stated target population;
  weighting scheme fixed in advance.
- Exclusions: sites returning non-200 after one retry and an http fallback are marked
  unreachable; tiny-n cities (n < 5 reachable) are pooled into their stratum, not reported
  individually.

### 7. Other
- Ethics: measurement via polite HTTP only (rate-limited, identifiable User-Agent, three
  public resources per site, honoring robots.txt for our own fetches). No provider-UI scraping.
- Open science: query frame, parsed dataset (CC BY 4.0), code, and the versioned AI-crawler
  and schema codebooks are published. Raw HTML is not redistributed.
- Deviations from this plan will be reported in the paper.
