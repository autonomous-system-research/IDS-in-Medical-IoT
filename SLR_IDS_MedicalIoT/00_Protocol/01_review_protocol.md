# Review Protocol
## A PRISMA 2020 Systematic Literature Review of Intrusion Detection and AI-Driven Security for the Internet of Medical Things, Medical Image Data and Federated Healthcare Settings

**Review period covered:** 1 January 2025 - 17 November 2026
**Protocol version:** 1.0  **Date prepared:** 2026-11-17
**Lead investigator:** Md Wahidur Rahman (WRESLab)

---

## 1. Rationale

Connected medical devices, hospital networks and collaborative learning pipelines have become a first-class
attack surface. Two prior reviews by this group frame the present work: a PRISMA review of ML/DL/IoT systems
(Sensors 2026, 26, 6569) and a PRISMA review of privacy-preserving deep learning for disease diagnosis in
medical imaging (IEEE Access 2026). This review applies the same methodological machinery - PRISMA 2020 flow,
explicit eligibility criteria, and a ten-item quality-appraisal rubric - to the security of the Internet of
Medical Things (IoMT), medical image data, and federated healthcare learning.

## 2. Research questions (PICOC)

- **Population:** IoMT / medical IoT networks, hospital and clinical networks, wireless body area networks,
  medical imaging pipelines, and multi-institution federated healthcare learning systems.
- **Intervention:** learned detection and protection mechanisms - intrusion detection systems, anomaly
  detection, attack/threat classification, adversarial defence, differential privacy, federated learning,
  and blockchain-assisted security controls.
- **Comparison:** baseline or alternative detection/protection methods reported in the primary study.
- **Outcome:** quantitative detection or protection performance (accuracy, F1, AUC, MCC, detection rate,
  latency, energy, privacy-leakage measures).
- **Context:** real or simulated healthcare deployments, 2025-2026.

**RQ1 - Detection performance.** What detection and classification performance do current AI-driven security
mechanisms report across IoMT networks, medical image pipelines and federated healthcare settings, and
against which baselines?

**RQ2 - Architectures and data.** Which model families, datasets and deployment architectures (cloud, edge,
fog, on-device, federated) dominate, and what data volumes underpin the reported results?

**RQ3 - Privacy, robustness and deployment readiness.** To what extent do studies address privacy guarantees,
adversarial robustness, non-IID heterogeneity, explainability and real-world deployment constraints?

## 3. Information sources

Records were identified through the **OpenAlex** scholarly index (which aggregates Crossref, PubMed, DOAJ,
publisher and repository metadata), with **Crossref** and **Semantic Scholar** used for verification of
individual records. Scopus, Web of Science and IEEE Xplore could not be queried directly from the review
environment; instead, eligibility was restricted to venues published by established scholarly publishers
that are indexed in those databases, and the verbatim search strings are reported in `01_Search_Keywords/`
so they can be re-executed natively in Scopus/WoS/IEEE Xplore and the per-database counts substituted.

**Search executed:** 17 November 2026. **Fourteen search strings** were run (see search log).
Filters applied at query time: `publication_year = 2025 OR 2026`, `language = English`, `type = article`.
Two strings were additionally constrained by author-institution continent (Europe; North America) to probe
geographic coverage, in line with the review's stated coverage objective.

## 4. Eligibility criteria

### Inclusion
1. Peer-reviewed **journal article** published 2025-2026 (inclusive), in English.
2. Published in a journal of an established scholarly publisher indexed in Scopus, Web of Science,
   IEEE Xplore or PubMed/MEDLINE.
3. **Primary empirical study** that proposes and evaluates a security or privacy mechanism for one of:
   (a) intrusion/anomaly/attack detection in IoMT, medical IoT, healthcare IoT or wireless body area networks;
   (b) security, privacy or adversarial robustness of medical image data;
   (c) federated learning security/privacy in a healthcare setting;
   (d) blockchain-assisted security for healthcare IoT.
4. Reports a described method and at least one quantitative result.
5. Abstract (at minimum) retrievable, so that eligibility can be assessed.

### Exclusion
- **EC1** Reviews, surveys, systematic reviews, bibliometric studies, taxonomies, tutorials, roadmaps and
  comparison-only studies.
- **EC2** Non-peer-reviewed sources: preprints (arXiv, Preprints.org, Research Square, TechRxiv, SSRN),
  self-archived Zenodo records, theses, technical reports.
- **EC3** Conference proceedings and book chapters - this review is restricted to journal articles, a
  deliberate narrowing relative to the two reference reviews.
- **EC4** Venues not indexed in Scopus/WoS/IEEE Xplore/PubMed, or published by predatory-risk publishers.
- **EC5** Studies outside the healthcare/medical context (generic IoT, smart city, industrial, grid,
  agricultural, financial, automotive), or without a security/privacy/detection objective.
- **EC6** Records with no retrievable abstract, so eligibility cannot be assessed.
- **EC7** Position papers, editorials, commentaries, teaching cases and dataset-only papers without a
  proposed and evaluated method.

## 5. Selection process

Four sequential stages, each with a recorded decision and reason code for **every** record:

| Stage | Input | Output | File |
|---|---|---|---|
| De-duplication | 690 raw records | 594 unique | `02_Downloaded_Papers/02_deduplicated_records.csv` |
| Title screening | 594 | 242 | `03_Screening/01_title_screening.csv` |
| Venue/type eligibility | 242 | 153 | `03_Screening/02_venue_eligibility_screening.csv` |
| Abstract screening | 153 | 112 | `03_Screening/03_abstract_screening.csv` |
| Quality assessment | 112 | 83 at >=75 | `03_Screening/04_quality_assessment_scores.csv` |
| Final selection | 83 | **50** | `02_Downloaded_Papers/03_final_50_included_studies.csv` |

**Final-selection rule (pre-specified).** Among studies scoring >=75, studies were allocated to four
thematic strata with target counts (IDS in Medical IoT 30; federated-learning security 10; medical image
security 6; blockchain healthcare IoT 4). Only three blockchain-centred studies cleared the threshold, so
the unused slot was reallocated to the IDS stratum (31). Within each stratum, studies with a European or
North American author affiliation were prioritised in line with the review's geographic coverage objective,
and within each affiliation stratum studies were ranked by quality-appraisal score (ties broken by
citation count). No study below the 75/100 threshold was admitted.

## 6. Quality assessment

The ten-item appraisal instrument supplied by the review team (derived from the NIH Quality Assessment Tool
for Systematic Reviews and Meta-Analyses and Zeng et al., 2015) was applied to all 112 abstract-eligible
studies. Each item is scored 0-10, giving a maximum of 100. **The inclusion threshold for this review is
>=75/100** (the uploaded template header states 80; the 75 threshold was specified by the review lead for
this review and is applied throughout).

Rating bands: **Good** >=75 - **Fair** 60-74 - **Poor** <60.

The ten items, and the evidence basis used to score each for a primary computational study, are listed in
`03_Screening/05_quality_assessment_rubric_items.csv`. Per-item evidence strings are recorded for every
study in `03_Screening/04_quality_assessment_scores.csv`.

**Stated limitation.** Scores were derived from the retrievable record (title, abstract, venue, metadata,
and open-access full text where available) rather than from a full-text read of every closed-access paper.
Item 7 (limitations/bias discussion) in particular is scored on an abstract-level proxy and is explicitly
flagged in the evidence column as requiring full-text verification. A second human rater should confirm
the scores before submission; rater-initial fields are provided in the QA workbook for this purpose.

## 7. Data extraction

Data were extracted into the review team's 19-row metadata template. Four rows of that template are written
for LLM-based studies and were mapped to their direct analogues for this domain, with the original label
retained:

| Template row | Mapped meaning in this review |
|---|---|
| LLM(s) Used | Model(s) used - architecture family, variant, open vs. proprietary |
| Integration Method | Training/deployment method - centralised, federated, split, transfer, edge/on-device |
| Evaluation Method for LLM Output | Evaluation method for model output - metrics, protocol, human/expert validation |
| LLM-Specific Risks Discussed | Security and privacy risks discussed - threat model, privacy budget, attack surface |

Dataset size and data volume are recorded as a required field. Where a value is not stated in the
retrievable record it is marked `Not reported in retrievable record` and never inferred.

## 8. Deviations from the reference protocols

1. Databases: OpenAlex/Crossref/Semantic Scholar rather than native Scopus/WoS/IEEE Xplore/PubMed queries.
2. Threshold: >=75/100 rather than the 80/100 used in both reference reviews.
3. Document types: journal articles only (both reference reviews also admitted conference papers).
4. Window: 2025-2026 only, a deliberately narrow two-year window to capture the current state of the art.
5. Single-rater appraisal in this pass; a second rater is required before submission.
