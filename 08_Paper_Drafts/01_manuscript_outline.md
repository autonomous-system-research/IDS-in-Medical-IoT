# Manuscript Outline — draft scaffold

Working title: **Intrusion Detection and AI-Driven Security for the Internet of Medical Things, Medical Image
Data and Federated Healthcare Settings: A PRISMA 2020 Systematic Literature Review of 50 Studies (2025-2026)**

## Abstract (structured, ~250 words)
Background / Methods (PRISMA 2020, 690 records, 594 unique, 50 included, 10-item appraisal at >=75/100) /
Results (RQ1-RQ3 headline findings) / Conclusions.

## 1. Introduction
1.1 Connected care as an attack surface - clinical consequence, not just data loss
1.2 Why IoMT, medical image data and federated settings belong in one review
1.3 Gap relative to existing reviews (Table 1: comparison of related reviews)
1.4 Contributions and research questions

## 2. Methods  -> draw directly from `00_Protocol/01_review_protocol.md`
2.1 Research questions (PICOC)
2.2 Information sources and search strategy  -> `01_Search_Keywords/`
2.3 Eligibility criteria  -> `00_Protocol/02_eligibility_criteria.csv`
2.4 Selection process and PRISMA flow  -> Figure 1
2.5 Quality assessment  -> rubric table plus one worked example (use P01 or P02 from the QA workbook)
2.6 Data extraction  -> template mapping table

## 3. Results
3.1 Bibliographic profile  -> Figure 2; `06_Insight_Analysis/04_venue_and_year_distribution.csv`
3.2 RQ1 - Reported detection performance
    - accuracy/F1 ranges by theme and by dataset; the 99-per-cent-accuracy saturation problem
    - which studies report MCC/AUC rather than accuracy alone, and why that matters on imbalanced IoMT data
3.3 RQ2 - Architectures, datasets and data volumes
    - Figure 3; `06_Insight_Analysis/01_dataset_usage_frequency.csv`, `02_technique_frequency.csv`
    - concentration on CICIoMT2024 (11/50) and WUSTL-EHMS-2020 (10/50): a benchmark monoculture
    - dataset sizes and what is simply not reported  -> `05_Data_Extraction/03_benchmark_dataset_reference.csv`
3.4 RQ3 - Privacy, robustness and deployment readiness
    - Figure 4; federated/DP/blockchain mechanisms; non-IID handling; explainability uptake
3.5 Research gaps  -> Figure 5

## 4. Discussion
4.1 What the evidence supports, and what it does not
4.2 Benchmark monoculture and the external-validity problem
4.3 Reporting gaps: dataset sizes, hardware, threat models, adversarial robustness
4.4 Geography and venue concentration of the evidence base
4.5 Practical recommendations for IoMT security researchers

## 5. Limitations of this review
Single index searched; venue-based proxy for Scopus/WoS/IEEE/PubMed indexing; abstract-level appraisal for
most studies; single rater in the first pass; open-access skew introduced by excluding records whose abstracts
could not be retrieved; two-year window.

## 6. Conclusion and future directions

## Appendices
A. Full search strings and per-string yields
B. Quality-assessment scores for all 112 appraised studies
C. The 50 included studies with extraction summaries

---
### Figure and table inventory
| Asset | Source file |
|---|---|
| Figure 1 - PRISMA 2020 flow | `07_Figures/Figure_1_PRISMA_flow.png` |
| Figure 2 - Bibliographic profile | `07_Figures/Figure_2_bibliographic_profile.png` |
| Figure 3 - Datasets and techniques | `07_Figures/Figure_3_datasets_and_techniques.png` |
| Figure 4 - Methodological rigour | `07_Figures/Figure_4_methodological_rigour.png` |
| Figure 5 - Research gaps radar | `07_Figures/Figure_5_research_gaps.png` |
| Table - Eligibility criteria | `00_Protocol/02_eligibility_criteria.csv` |
| Table - QA rubric items | `03_Screening/05_quality_assessment_rubric_items.csv` |
| Table - Included studies | `02_Downloaded_Papers/03_final_50_included_studies.csv` |
| Table - Insight master | `06_Insight_Analysis/05_insight_master_table.csv` |
| References | `02_Downloaded_Papers/05_final_50_references.bib` |

### Open actions before submission
1. Re-run the 14 search strings in Scopus / WoS / IEEE Xplore / PubMed and substitute real per-database counts.
2. Second-rater quality appraisal - complete the Rater 1 / Rater 2 fields in the QA workbook.
3. Full-text pass over the 46 studies currently extracted at abstract level, to fill dataset sizes, hardware,
   validation protocol, limitations and threat models.
4. Register the protocol (OSF) and add the registration DOI to the Methods section.
