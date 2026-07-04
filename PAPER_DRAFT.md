# The State of AI-Readiness on Business Websites (2026)
### A large-scale measurement of AI-crawler permission, llms.txt adoption, and structured-data readiness

**Joshua R. Gutierrez**
Axion Deep Labs, Inc., Las Cruces, NM
Contact: hello@axiondeep.com

*Working paper. Version: 2026-07-04.*

**Keywords:** AI search, answer engines, generative engine optimization, llms.txt, schema.org,
structured data, AI crawlers, robots.txt, local business, measurement study

**JEL classification:** L86 (Information and Internet Services), M31 (Marketing), O33 (Technological
Change: Choices and Consequences)

> Status note: the numbers below are from a large-scale exploratory crawl (n=766; 2026-07-02, 10
> verticals, 15 cities), stable across the 149-, 487-, and 766-site runs (the central robustness
> result). These figures are exploratory. A confirmatory crawl of >= 1,000 reachable sites, with a
> frozen analysis plan, is preregistered on OSF at https://osf.io/2q5er/ (plan: osf_prereg.md);
> this working paper is posted to SSRN as the exploratory precursor. No figure here is
> a placeholder; each is a real measured value.

---

## Abstract

As AI answer engines become a discovery channel, a website's ability to participate is gated by
three public, machine-checkable signals: whether it permits AI crawlers (robots.txt), whether it
guides them (llms.txt), and whether it is structured for machine identification (schema.org). We
define AI-readiness operationally as adoption of these three public signals, and measure them across
a stratified sample of local-business websites (n=766, 10 verticals, 15 cities) drawn from
OpenStreetMap. Among reachable sites, adoption of the structured-data signals designed to make a
business machine-identifiable is low: review/AggregateRating markup appears on 9% of homepages
(95% CI 7-11) and FAQ markup on 4% (3-6). The modal business scores 2 of 10 on a pre-specified
AI-Readiness index (42% of reachable sites): it does not block AI crawlers, but exposes no schema,
reviews markup, or llms.txt. Readiness varies sharply by vertical: accounting firms show 0% review
and 0% Person markup (0 of 27; Wilson 95% CI 0-12 for each), non-overlapping with legal firms
(review 26%, CI 18-35; Person 31%, CI 22-41); accounting is the only vertical simultaneously at
zero review, zero Person, and lowest identity markup. llms.txt adoption is 25% (22-29), of which at
least 28% carries a tool-generation signature rather than being authored. Unlike publishers, local
businesses rarely block AI crawlers (4%, CI 3-6). Figures replicated across 149-, 487-, and
766-site samples. The dataset, code, and codebooks are released openly.

---

## 1. Introduction

Search interfaces increasingly include AI-generated summaries and conversational answer systems
(ChatGPT, Perplexity, Gemini, Google AI Overview) alongside traditional ranked results. Appearing
in those answers plausibly depends on signals different from classic ranking: whether the engine is
permitted to use the content, whether it can reach it, and whether the business is described in a
machine-readable form. This paper measures the supply side of that question: what businesses
actually expose, before any question is ever asked. It does not measure whether or how AI engines
use these signals; a companion study measures the demand side (what AI engines recommend and cite).

**Scope of "AI-readiness."** We use the term throughout as an *operational construct*, not a
comprehensive audit. A full account of AI-readiness would also include crawlability, rendering,
content quality, authority, citations, reviews on third-party platforms, Google Business Profile
completeness, and performance. We deliberately restrict measurement to three signals that are
public, machine-checkable at scale, and cost nothing to observe: AI-crawler permission (robots.txt),
llms.txt, and homepage schema.org markup. Where we write "AI-readiness," we mean adoption of these
three signals, and nothing broader is claimed.

Contributions: (1) the first stratified, multi-vertical measurement of AI-crawler permission,
llms.txt adoption, and schema readiness together; (2) a pre-specified operational AI-Readiness
index; (3) an open, reproducible, zero-cost methodology and dataset.

## 2. Background and related work

- **AI crawlers and permission.** Major model and answer engines publish named crawler
  user-agents (GPTBot, Google-Extended, ClaudeBot, PerplexityBot, CCBot, and others) that sites may
  allow or disallow in robots.txt. Publisher blocking has been widely reported; local-business
  behavior has not been measured systematically.
- **llms.txt.** A proposed convention for a root-level markdown file guiding LLMs to a site's key
  content. Adoption has not been quantified at scale, nor has the extent of plugin auto-generation.
- **Structured data.** schema.org markup lets machines identify entities, people, and reviews;
  its role in AI recommendation is an active question. Prior work (the authors' AI-visibility study)
  measured whether crawlers can render content; this study measures whether sites are structured and
  permitted for AI at all.
- **Sampling frames.** Tranco provides a manipulation-resistant top-sites list; OpenStreetMap
  provides categorized, geographic local-business coverage used here for the local frame.

## 3. Methods

Full protocol and pre-registration: PROTOCOL.md, osf_prereg.md; OSF registration of the confirmatory
wave at https://osf.io/2q5er/.

- **Frame.** OpenStreetMap POIs carrying a `website` tag, selected by vertical (local-service
  categories) and five geographic strata (metro, mid, small, tourism, university).
- **Measurement (public HTTP only).** Per site: robots.txt (AI-crawler permission, versioned bot
  list); /llms.txt (validated presence: not an HTML/redirect stub, >= 40 bytes, markdown structure;
  plus provenance signature); homepage JSON-LD schema.org @type extraction; platform fingerprint.
- **AI-Readiness index (pre-specified, 0-10):** allows AI crawlers +2; valid llms.txt +2; identity
  schema +2; review schema +2; FAQ schema +1; Person schema +1. The index is an *operational
  benchmark*, not a validated latent construct: the weights encode a simple editorial judgment
  (permission and the three highest-value structured signals count double; the two secondary schema
  types count single) and are not derived from factor analysis or an external criterion. It is
  intended as a transparent, reproducible summary score for tracking adoption over time, and should
  not be read as a psychometric measurement instrument. We report the full component distribution so
  readers can reweight.
- **Statistics.** Adoption computed over reachable sites; reachability reported separately. Every
  proportion (overall and by vertical/stratum) is reported with a Wilson score 95% confidence
  interval; Wilson is used in preference to the percentile bootstrap because several verticals sit at
  a boundary proportion (0% adoption), where the bootstrap degenerates to a zero-width interval and
  the Wilson interval remains correctly bounded. The index *mean*, being a mean of 0-10 scores rather
  than a proportion, is reported with a bootstrap 95% CI (>= 2000 resamples, site as unit, fixed
  seed). Between-vertical differences are read from non-overlapping 95% intervals; the flagship
  accounting-vs-legal contrast is confirmed by non-overlap on both review and Person markup.

## 4. Results (n=766; reachable n=594)

**Reachability.** 78% of OSM-listed business sites returned a usable homepage (95% CI 74-80);
the remainder were stale URLs, redirects, or blocked. Adoption figures are over reachable sites.

**Overall adoption (Wilson 95% CI).**
- Identity schema: 49% (45-53)
- Review / AggregateRating schema: 9% (7-11)
- FAQ schema: 4% (3-6)
- Person schema: 10% (8-13)
- Valid llms.txt: 25% (22-29)
- Blocks at least one AI crawler: 4% (3-6)

**The AI-Readiness index.** Mean 3.73 (bootstrap 95% CI 3.58-3.89), median 4. 42% of reachable
sites score exactly 2 of 10: they do not block AI crawlers but expose no schema, reviews markup, or
llms.txt.

**Vertical gradient (primary comparison).** Review-markup prevalence differs sharply by vertical.
Three verticals sit at 0% review markup (accounting 0/27, optician 0/30, HVAC 0/12), but accounting
is distinctive: it is the only vertical *simultaneously* at 0% review, 0% Person, and the lowest
identity markup (26%, CI 13-45). Its review and Person intervals (0 of 27; Wilson 0-12 for each) do
not overlap legal firms (review 26%, CI 18-35; Person 31%, CI 22-41), the flagship contrast.
Dentists sit between (review 10%, CI 6-17).

*Effect size.* Because accounting's review rate is exactly zero, a rate ratio against it is
undefined; we report the contrast as an absolute gap of 26 percentage points with non-overlapping
95% intervals. For a stable ratio among sizable verticals, legal firms are 2.6x more likely than
dentists (26% vs 10%) and roughly 2.9x the all-vertical review rate (26% vs 9%) to expose review
markup. Across ten verticals, the readiness gradient does not track the value of the services sold;
one candidate explanation, developed in the Discussion, is the maturity of each field's
digital-marketing ecosystem, but the design does not adjudicate among alternatives.

**llms.txt provenance.** Of the 151 sites with a valid llms.txt, *at least* 28% carry an explicit
auto-generation signature (Rank Math, Yoast, or other "generated by" markers). This is a lower
bound: the remaining 72% carry no signature but could equally be plugin output without a marker,
copied templates, or agency-supplied files, none of which our detector distinguishes from
hand-authored files. The finding shows that a substantial, and possibly much larger, share of
llms.txt adoption is tool-mediated rather than a deliberate optimization choice; the exact split
between authored and generated files is not identified.

**Permission.** AI-crawler blocking is rare among local businesses (4%), in contrast to the
near-universal blocking observed on major news publishers during instrument validation.

## 5. Discussion

**Permission is not the constraint; structure is.** Within the three signals we measured, the
limiting factor is not access but description. Local businesses overwhelmingly permit AI crawlers
(96% allow all) yet expose little machine-readable structure: half publish no identity markup and
nine in ten publish no review markup. We frame this as a description gap rather than a
recommendation gap on purpose. We did not observe any AI engine's behavior, so we cannot say these
sites are less likely to be recommended; we can say only that they hand a crawler fewer of the
public, machine-readable signals designed to identify and characterize a business. Whether those
signals causally affect AI recommendation is the question our companion demand-side study takes up,
and is out of scope here.

**Schema is one input among several.** The description gap we measure is specific to on-page
structured data. AI systems can also draw on rendered page text, inbound links and citations,
third-party review platforms, knowledge graphs, and Google Business Profile and Bing Places
listings, none of which this study observes. A business with no homepage schema is therefore not
necessarily invisible to AI; it is missing one class of signal it fully controls and can add at low
cost. We caution against reading the schema gap as the sole or even the primary bottleneck for AI
visibility; it is the machine-readable, self-published layer, measured because it is public and
uniform, not because it is established as dominant.

**Why the vertical gradient, and why accounting.** The gradient does not track the value of the
services sold: accounting, among the highest-value advisory verticals, is the least structured. One
plausible explanation is that adoption tracks the maturity of a vertical's digital-marketing
ecosystem: legal marketing has industrialized schema (specialist agencies, review-driven lead gen,
template ecosystems), and accounting has not. But this is one hypothesis among several the design
cannot separate. Accounting firms may on average run older sites or CMSs, depend more on referral
and relationship channels than on search, spend less on SEO, or skew smaller than the legal firms in
our frame; any of these would produce the same pattern without a "marketing maturity" story. Our
data support the *observation* of the gap far more strongly than any single *explanation* for it;
disentangling firm age, size, CMS, and channel mix would require firmographic covariates we did not
collect.

**llms.txt adoption is partly an artifact of defaults.** At least 28% of llms.txt files are
tool-generated, and the true share is plausibly higher. This reframes headline "adoption" as partly
a byproduct of plugin defaults rather than deliberate intent, and is a general caution: raw adoption
counts for any emerging convention conflate deliberate optimization with software that ships the
feature by default. Longitudinal tracking that separates authored from generated files would measure
intent more faithfully than a single cross-sectional count.

**Implications for AI-visibility practice.** For practitioners, the actionable part is concrete and
low-cost: identity, review, and Person markup plus a maintained llms.txt move a business from the
modal 2/10 toward the top of the observed distribution with no change to permission or content
strategy. We frame this as improving machine-readable self-description, a necessary-looking but
not proven-sufficient condition for AI visibility. Whether it moves actual AI recommendation is
exactly what a controlled demand-side study should test next, and is the natural continuation of
this work.

## 6. Limitations

Homepage-only schema (interior pages may differ); single snapshot (adoption is fast-moving; a
longitudinal arm is planned); robots.txt reflects stated policy, not enforcement; platform detection
is heuristic (a share remain unclassified); the OSM frame under-represents rural and tourism
businesses (a real signal, but it thins those strata); provenance detection catches only explicit
signatures. Localization is scoped to US English in this wave. We collected no firmographic
covariates (firm age, size, CMS vintage, marketing spend, channel mix), so the vertical gradient is
reported as an observed association and the design cannot attribute it to any single cause. Most
fundamentally, the study measures the supply of public signals, not their effect: it does not
observe AI-engine behavior, so no claim about actual recommendation or citation is tested here.

## 7. Conclusion

Local businesses are permitted-but-undescribed: they let AI crawlers in and expose little
machine-readable structure. Measured against the three public signals we define as AI-readiness, the
gap is widest in high-value advisory verticals such as accounting. Because the missing signals are
cheap, public, and machine-checkable, the gap is closable, and this study provides a baseline and an
open operational index to track it. Whether closing it changes what AI engines actually recommend is
the demand-side question we take up next.

## Open materials

All materials are released at **https://github.com/Axion-Deep-Labs/ai-readiness-2026**: the query
frame and parsed dataset (149-, 487-, and 766-site crawls; CC BY 4.0), the code (build/crawl/analyze;
MIT), the full protocol and preregistration, and the versioned AI-crawler and schema codebooks
(CODEBOOK.md). Raw HTML is not redistributed. All reported figures reproduce with
`python3 analyze.py data/crawl_confirmatory_766.jsonl sample_meta.csv`.

## References

1. Le Pochat, V., Van Goethem, T., Tajalizadehkhoob, S., Korczyński, M., & Joosen, W. (2019).
   *Tranco: A Research-Oriented Top Sites Ranking Hardened Against Manipulation.* Proceedings of the
   26th Network and Distributed System Security Symposium (NDSS).
2. schema.org. *Schema.org vocabulary.* https://schema.org (accessed 2026).
3. Howard, J., & Answer.AI. (2024). *The /llms.txt proposal.* https://llmstxt.org (accessed 2026).
4. OpenStreetMap contributors. *OpenStreetMap.* https://www.openstreetmap.org (accessed 2026).
5. Wilson, E. B. (1927). *Probable inference, the law of succession, and statistical inference.*
   Journal of the American Statistical Association, 22(158), 209-212.
6. Efron, B., & Tibshirani, R. J. (1993). *An Introduction to the Bootstrap.* Chapman & Hall.
7. Gutierrez, J. R. (2026). *Can AI Crawlers See Your Site? A Rendering-Based AI-Visibility Study.*
   Axion Deep Labs working paper (companion, supply-side rendering).
8. Gutierrez, J. R. (2026). *A Large-Scale Analysis of Commercial Recommendations by AI Search
   Engines.* Axion Deep Labs working paper (companion, demand-side; in preparation).
