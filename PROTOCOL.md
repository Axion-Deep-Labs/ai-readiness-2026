# Study Protocol (Pre-Registration Draft)
## The State of AI-Readiness on Business Websites (2026)

**Authors:** Axion Deep Labs / Axion Deep Digital. Project lead: Claude (with J. Gutierrez).
**Version:** 0.1 (pre-registration draft).
**Status:** Draft. To be registered on OSF before data collection. A calibration pilot precedes freezing the sample.
**Cost:** Zero. All measurements are HTTP fetches of public files. No paid APIs.
**Relationship to prior work:** The earlier "AI Visibility" study measured whether non-rendering AI crawlers can *read* a site's content (the JavaScript rendering gap). This study measures three different, upstream layers: whether a site *permits* AI crawlers, whether it *guides* them (llms.txt), and whether it is *structured* for them (schema). Rendering-visibility is "can AI see your content." AI-readiness is "are you set up for AI at all."

---

## 1. Summary

As AI answer engines (ChatGPT, Perplexity, Gemini, Google AI Overview) become a discovery channel, a website's participation depends on three public, machine-checkable signals:

1. **Permission:** does `robots.txt` allow or block the major AI crawlers?
2. **Guidance:** does the site publish an `llms.txt` file (the emerging convention for telling LLMs what matters)?
3. **Structure:** does the site expose schema.org structured data that lets machines identify the business, its people, and its reviews?

This study measures adoption of all three across a large, stratified sample of business websites, reports variation by vertical, platform, and size, and combines them into a transparent AI-Readiness index. The design is neutral: we do not pre-register specific adoption rates, only the measurement plan.

---

## 2. Motivation and contribution

Public commentary on "getting found by AI" is largely anecdotal. There is little systematic measurement of the three concrete, controllable signals above, especially for ordinary local and small-business sites (as opposed to top global domains). Contribution:

- First large, stratified measurement of AI-crawler permission, llms.txt adoption, and schema readiness together.
- A reproducible, zero-cost methodology and an open dataset.
- A defined AI-Readiness index that businesses and tools (DeepAudit AI) can apply.
- A baseline for longitudinal tracking of adoption over time.

---

## 3. Research questions

- **RQ1 (permission).** What fraction of business sites block each major AI crawler (GPTBot, ChatGPT-User, Google-Extended, ClaudeBot, anthropic-ai, PerplexityBot, CCBot, Bytespider, Amazonbot, Applebot-Extended, and others) in robots.txt? How does blocking vary by vertical, platform, and size?
- **RQ2 (guidance).** What fraction publish `llms.txt` (and `llms-full.txt`)? For those that do, what is the file's size and structure (headings, link counts)? Adoption by vertical and platform.
- **RQ3 (structure).** Which schema.org types are present on the homepage (Organization, LocalBusiness and subtypes, Person, Review/AggregateRating, FAQPage, Product, BreadcrumbList, etc.)? What fraction expose the entity-plus-trust combination (business identity + review markup) that recommendation engines rely on?
- **RQ4 (composite).** Under a pre-registered rubric, what is the distribution of an AI-Readiness index across the sample, and what predicts it (platform, size, vertical)?
- **RQ5 (tension).** Do the layers align or conflict? For example, how many sites carry rich schema yet block AI crawlers, or publish llms.txt yet expose no structured data?

---

## 4. Hypotheses (neutral)

We pre-register the analysis plan, not specific values.

- **H1.** Adoption of all three signals is non-uniform and varies systematically by platform and vertical. (No specific rate is pre-registered.)
- **H2.** llms.txt adoption is low relative to schema presence (weak prior: llms.txt is newer), but this is a measurement, not a required result.
- **H3.** Platform is a strong predictor of readiness (managed platforms like Shopify/Wix/Squarespace bundle some schema by default), tested rather than assumed.
- **H4 (tension exists).** A measurable minority of sites are internally inconsistent across the three layers.

---

## 5. Design

Cross-sectional observational crawl. Unit of analysis is the website (registrable domain). Factors recorded per site: vertical, platform, size proxy, and geography (for local verticals). One snapshot per site for the flagship; periodic re-crawls for the longitudinal sequel.

---

## 6. Sampling

### 6.1 Frame (free, defensible)
A hybrid frame, because no single free list covers both local businesses and top web properties:

- **Local-service businesses:** OpenStreetMap points of interest that carry a `website` tag, selected by category tags (e.g., dentist, accountant, lawyer, plumber, hvac, beauty) and by geography. OpenStreetMap is free, categorized, and geographically explicit, which supports stratified local sampling.
- **Ecommerce / SaaS / publisher / larger properties:** the Tranco top-sites list (free, research-grade, manipulation-resistant), sampled within category where category labels are available or assigned.
- **Continuity:** optionally include the prior Axion Deep Digital study cohorts (the 292-site and ~368-site samples) as a labeled subset for comparison across studies.

### 6.2 Strata
- **Vertical:** local services (10 categories), ecommerce, B2B SaaS, professional/enterprise, publisher/news.
- **Platform:** WordPress, Shopify, Wix, Squarespace, Webflow, Duda, custom/other (detected, Section 7.3).
- **Size proxy:** Tranco rank band for global sites; presence-of-multiple-locations or review-count band for local (where cheaply available), else "unknown."
- **Geography (local only):** the five city strata from the companion study (metro, mid, small/rural, tourism, university) plus a national spread.

### 6.3 Size
Target several thousand sites total for tight stratum-level confidence intervals. Exact per-stratum counts are frozen after the calibration pilot and published. A pilot (a few hundred sites) precedes freezing, to validate detectors and estimate variance.

---

## 7. Data collection (all free HTTP)

Per site, a polite fetch of at most three public resources:

### 7.1 robots.txt (RQ1)
Fetch `/robots.txt`. Parse `User-agent` blocks for the curated AI-crawler list (Section 8.1). Record, per crawler: explicitly disallowed (`Disallow: /`), partially disallowed, allowed, or not mentioned. Record presence of a wildcard block and of an llms/AI-specific directive.

### 7.2 llms.txt (RQ2)
Fetch `/llms.txt` and `/llms-full.txt`. Record HTTP status, byte size, and a light structural parse (markdown heading count, link count, presence of a title/description). A 200 with markdown content counts as adoption; a 404 or soft-404 does not.

### 7.3 Homepage HTML (RQ3 and platform detection)
Fetch the homepage. Extract all `<script type="application/ld+json">` blocks and microdata; parse and record the set of schema.org `@type` values. This method is validated (used to read six firms' live schema in prior work). Detect platform from HTML/header fingerprints (e.g., `wp-content` for WordPress, `cdn.shopify` for Shopify, `wixstatic`/`parastorage` for Wix, `squarespace`, `webflow`, `d1csarkz`/Duda, plus `Server`/`X-Powered-By` headers).

### 7.4 Logging
Per site: timestamp, final URL after redirects, HTTP status for each resource, detected platform, and the raw parsed values. Fetches are rate-limited, identify our crawler in the User-Agent, and are limited to these public, intended-for-machines resources.

---

## 8. Variables and taxonomy

### 8.1 AI-crawler list (versioned)
Training/data crawlers and answer crawlers, kept as a version-controlled list: GPTBot, ChatGPT-User, OAI-SearchBot, Google-Extended, ClaudeBot, anthropic-ai, Claude-Web, PerplexityBot, Perplexity-User, CCBot, Bytespider, Amazonbot, Applebot-Extended, Meta-ExternalAgent, cohere-ai, Diffbot, Timpibot, others as they emerge.

### 8.2 Schema categories
Grouped: identity (Organization, LocalBusiness and subtypes such as AccountingService, ProfessionalService), people (Person), trust (Review, AggregateRating), Q&A (FAQPage, QAPage), commerce (Product, Offer), navigation (BreadcrumbList, SiteNavigationElement), content (Article, WebPage), other. The "entity plus trust" combination (identity + Review/AggregateRating) is a headline derived variable.

### 8.3 llms.txt structure
Present/absent, byte size band, heading count, link count, has-title, has-description.

---

## 9. AI-Readiness index (RQ4, pre-registered rubric)

A transparent additive score (points fixed in advance, published):

- Allows the major AI crawlers (not blocked in robots.txt): +2
- Publishes a valid llms.txt: +2
- Has identity schema (Organization or LocalBusiness/subtype): +2
- Has trust schema (Review or AggregateRating): +2
- Has FAQPage or QAPage schema: +1
- Has Person schema (named experts): +1

Maximum 10. The distribution is reported overall and by stratum. The rubric is a communication device, not a claim of causal weighting; weights are stated as a design choice and sensitivity to alternative weightings is reported.

---

## 10. Analysis plan

Resampling unit for confidence intervals is the site (bootstrap, 10k resamples).

- **RQ1 to RQ3.** Adoption proportions with bootstrap 95% CIs, overall and by vertical, platform, and size. Chi-square / permutation tests for differences across strata, with Benjamini-Hochberg correction within families.
- **RQ4.** Distribution of the index; logistic or ordinal regression of readiness on platform, vertical, and size, with odds ratios and CIs.
- **RQ5.** Cross-tabulations of the three layers; report the size of the inconsistent segments (rich schema but AI-blocked; llms.txt but no schema) with CIs.

Weighting: because the frame over-represents some strata, primary estimates are reported both unweighted and re-weighted to a stated target population; the weighting scheme is pre-registered.

---

## 11. Staging

- **Flagship (cross-sectional):** RQ1 to RQ5, one crawl.
- **Longitudinal sequel:** periodic re-crawls of the frozen sample to measure adoption change over time (especially llms.txt and AI-crawler blocking, both fast-moving).
- **Product tie-in:** every signal maps directly to a DeepAudit AI check; the readiness rubric can ship as a public score.

---

## 12. Feasibility

Zero marginal cost (HTTP only). The homepage-schema extraction method is already validated in prior work. A crawl of several thousand sites, rate-limited and polite, completes in hours. The collector can run from a standard workstation. A calibration pilot (a few hundred sites) runs first to validate the robots.txt parser, the llms.txt detector, the schema extractor, and platform fingerprints, and to estimate per-stratum variance for final sizing.

---

## 13. Limitations

- **Homepage-only schema.** Structure is measured on the homepage, not sitewide; stated explicitly. A deeper variant could sample interior pages.
- **Single snapshot.** Adoption is a moving target; the longitudinal arm addresses drift.
- **robots.txt is advisory.** Blocking directives express intent, not enforcement; some crawlers ignore them, and some sites cloak. We measure stated policy, not actual crawler behavior.
- **Detector error.** Platform fingerprints and soft-404 detection are heuristic; accuracy is validated on a hand-labeled sample and reported.
- **Frame bias.** OpenStreetMap coverage and Tranco popularity both bias the frame; mitigated by stratification, explicit weighting, and publishing the site list.
- **Localization and internationalization** are scoped (initial focus US English), stated as a boundary.

---

## 14. Open science and crawling ethics

- **Pre-registration** on OSF before data collection.
- **Polite crawling:** rate-limited, identifiable User-Agent, only the three public resources per site, honoring each site's robots.txt for our own fetches.
- **Open dataset** (CC BY 4.0): site list, parsed signals, and the readiness index. Raw HTML is not redistributed; parsed fields are.
- **Open code and codebook**, including the versioned AI-crawler list and schema taxonomy.

---

## 15. Deliverables

- Flagship working paper (SSRN) + Axion Deep Digital blog write-up + shareable stat cards + open dataset.
- A public AI-Readiness score/checker as a DeepAudit tie-in.
- Longitudinal adoption sequel.

---

## Appendix B. Calibration pilot (2026-07-01, n=14, instrument validation)

A stdlib crawler (`pilot_crawl.py`) fetched robots.txt, llms.txt, and homepage schema for 14 seed sites, including six Capital Tax competitor sites used as schema ground truth.

Validated:
- **Schema extractor:** exact match on all six ground-truth sites (e.g., capitaltax.com 14 types, has identity, no Review, has llms.txt; thecreek.cpa and pattencpaco.com zero).
- **AI-crawler blocking:** correctly detected NYTimes (13 AI bots blocked) and The Atlantic (11), while small firms and platforms showed none.
- **llms.txt and platform** detectors returned plausible, spot-checkable results (Shopify/Stripe/Squarespace have llms.txt; WordPress/Wix/Shopify/Squarespace fingerprints correct).

Design refinements adopted from the pilot:
1. **User-Agent sensitivity.** Some large, bot-hostile sites (e.g., reddit.com) degrade or block non-browser fetches, starving homepage-schema and robots parsing. The confirmatory crawl will use a more browser-like User-Agent, and sites returning a login wall / non-200 / empty homepage are flagged as UA-restricted rather than scored as "no schema."
2. **Zero homepage review schema** appeared even among large brands, suggesting Review/AggregateRating markup on the homepage specifically is rare; the confirmatory analysis will note homepage-only scope and consider an interior-page variant.

## Appendix C. Stratified pilot (2026-07-01, n=149 local businesses from OSM)

Sample: OpenStreetMap POIs with a `website` tag, 5 cities (one per stratum) x 6 local verticals, via a reachable Overpass mirror.

Preliminary signals (not the confirmatory estimates, but stable enough to shape the design):
- Modal AI-Readiness index = 2/10 (90 of 149): the typical local business does not block AI crawlers but exposes no schema, no reviews markup, and no llms.txt.
- Review/AggregateRating schema ~10%, FAQ ~3%, Person ~11%, identity ~35%.
- AI-crawler blocking ~3% (local businesses rarely block, unlike publishers).
- Strong vertical gradient: lawyers far more structured (identity 62%, review 31%) than accounting (identity 18%, review 0%, Person 0%). Confirms the value of vertical as a factor.

Design refinements adopted:
1. **llms.txt validity and provenance.** The raw detector over-counted: HTML 301/redirect stubs and sub-50-byte files served at /llms.txt were counted as present. Fix: reject responses containing HTML markers anywhere in the first 1KB, reject sub-threshold sizes, and require markdown structure. Separately, record **provenance**: many real small-business llms.txt files are auto-generated by SEO plugins (observed: "Generated by Rank Math SEO"). Provenance (Rank Math / Yoast / other / hand-authored) becomes a recorded variable, because it reframes adoption as plugin-driven rather than deliberate.
2. **Reachability.** ~30% of OSM-listed sites did not return a clean 200 (stale URLs, redirects, UA blocks). The confirmatory pipeline retries once, follows redirects, and reports on reachable sites, flagging the rest.
3. **Platform detection.** ~50% classified as "unknown"; the fingerprint set will be expanded before the confirmatory run.
4. **Sampling.** Rural (Bozeman) and tourism (Sedona) strata yielded very few OSM businesses with websites (a real signal), but too few to estimate stratum variance. The confirmatory sample uses multiple cities per stratum and larger bounding boxes.

## Appendix D. Confirmatory crawl (2026-07-02, n=487, 15 cities)

The 149-site pilot headlines REPLICATED at n=487 (15 cities, 3 per stratum), 77% reachable:
- Modal AI-Readiness index = 2/10 (265 of 487 = 54%): does not block AI, exposes no schema/reviews/llms.txt.
- Review/AggregateRating schema 8%, FAQ 3%, Person 10%, identity 40%, AI-blocking 4%. All within a couple points of the pilot: stable.
- Vertical gradient held: lawyers most structured (identity 48%, review 19%, Person 23%); accounting worst on trust/entity (identity 23%, review 0/31, Person 0/31). The entire CPA vertical shows zero review and zero Person schema.
- llms.txt adoption ~19%; provenance of those: ~65% no-signature ("manual"), ~35% tool-generated (Rank Math 7%, Yoast 10%, other-generated 18%). Note: "manual" is a residual that likely includes undetected builder auto-generation, so ">=35% tool-generated" is a floor.

Remaining work before the paper:
1. Expand small/tourism strata and plumber/accounting verticals (still underpowered; some cells n<8).
2. Improve platform detection (~40% still "unknown").
3. Add bootstrap confidence intervals and the agreement/diversity statistics to the analyzer.
4. Drop or pool tiny-n cities (Ithaca n=1, Key West n=2) from stratum estimates.

## Appendix A. Why this is the free companion to the recommendations study

The recommendations study ("who does AI recommend") requires paid AI-engine queries and is gated on budget. This readiness study ("are you set up for AI") requires only public HTTP fetches and can run at zero cost immediately. Together they form a two-part program: readiness measures the supply side (what sites offer to AI), recommendations measure the demand side (what AI does with it). Either can be published alone; together they are a stronger narrative.
