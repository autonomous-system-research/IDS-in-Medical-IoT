# Leveraging AI and Federated Learning for Security in Medical IoT (IoMT) and Medical Imaging Data: A Systematic Literature Review

1. Md Wahidur Rahman; md_wahidur.rahman@students.tamuk.edu
2. Mohammad Sadman Tahsin; mohammad.tahsin@students.tamuk.edu
3. Haitham Y. Adarbah; haitham.adarbah@tamuk.edu
4. Afzel Noore; afzel.noore@tamuk.edu

AI-Based Autonomous Systems Research Lab, Department of Electrical Engineering and Computer Science, Frank H. Dotterweich College of Engineering, Texas A&M University-Kingsville, MSC 192, 917 W. Avenue B, Kingsville, TX 78363, USA

* Corresponding Author email: haitham.adarbah@tamuk.edu

## What this package contains

```
00_Protocol/            Review protocol, research questions, eligibility criteria
01_Search_Keywords/     The 14 verbatim search strings and the PICOC keyword blocks
02_Downloaded_Papers/   Identification register, de-duplicated records, the final 50, BibTeX
03_Screening/           Title -> venue -> abstract -> quality-assessment decisions, every record, every reason
04_PRISMA_Flow/         PRISMA 2020 counts, flow diagram (PNG + SVG), verification report
05_Data_Extraction/     Metadata extraction for all 50 (CSV + DOCX) and the benchmark dataset reference
06_Insight_Analysis/    Dataset usage, technique frequency, country/venue distribution, master insight table
07_Figures/             Figures 01-14 at 300 dpi + vector PDF, and FIGURE_CAPTIONS.md
08_Paper_Drafts/        Manuscript outline and the results narrative scaffold
Paper_Tracker.xlsx      Master tracker: all 50 papers, screening funnel, manuscript progress
```

## Headline numbers

| | |
|---|---|
| Records identified | 690 (14 search strings, OpenAlex, 17 Nov 2026) |
| Unique after de-duplication | 594 |
| Included at title screening | 242 |
| Sought for retrieval (venue eligible) | 153 |
| Included at abstract screening | 112 |
| Scored >= 75/100 on the quality rubric | 83 |
| **Included in the review** | **50** |
| Year split | 25 x 2025, 25 x 2026 |
| European / North American affiliation | 31 of 50 (62 per cent) |
| Quality-appraisal score range | 75 - 92 (mean 82.0) |
| Theme split | 31 IDS in Medical IoT, 10 federated security, 6 medical image security, 3 blockchain healthcare IoT |

Every one of the 594 unique records carries a recorded decision and reason code at every stage it reached.
`04_PRISMA_Flow/03_verification_report.csv` runs 40 automated consistency checks across the whole package;
all 40 pass.

## Four things to know before you use this

1. **The evidence is real and verified.** Every DOI was resolved individually against the OpenAlex index;
   journal, publisher, year, authors and author-affiliation countries come from that resolved record, not
   from memory. No paper, DOI, author or figure in this package is invented.

2. **Databases.** Scopus, Web of Science and IEEE Xplore cannot be queried from this environment. The search
   was run on OpenAlex and eligibility was restricted to venues of established publishers indexed in those
   databases. The verbatim strings are in `01_Search_Keywords/` so you can re-run them natively and substitute
   the true per-database counts before submission.

3. **Quality appraisal is single-rater and partly abstract-level.** Scores were derived from the retrievable
   record. Item 7 (limitations/bias) in particular is an abstract-level proxy and is flagged as such in the
   evidence column. The QA workbook has empty Rater 1 / Rater 2 initial fields — a second human rater should
   confirm the scores before submission.

4. **Full text was obtainable for 4 of the 50.** Nature, IEEE, Elsevier, Springer and Wiley block automated
   full-text retrieval; MDPI and Frontiers do not. Papers P02, P18, P34 and P39 carry full-text-verified
   extraction, including exact dataset sizes. The other 46 are extracted from abstract plus verified metadata,
   with unavailable fields marked `Not reported in retrievable record` — never guessed. With your institutional
   access those fields can be completed; `05_Data_Extraction/03_benchmark_dataset_reference.csv` gives the
   canonical size of each named benchmark in the meantime, with the provenance of every size figure stated.

## Threshold note

The uploaded quality-assessment template header states a threshold of 80. This review applies **>= 75**, as you
specified. Both numbers are documented in the protocol and in the workbook header.

## Geographic note

"Europe / North America" counts a study if **any** author institution is in Europe or North America, and
counts Turkiye as European. Reclassifying Turkiye moves the share from 62 per cent to 60 per cent. The full
country breakdown is in `06_Insight_Analysis/03_country_frequency.csv`.


---

## Quantitative analysis layer (added 18 November 2026)

```
06_Insight_Analysis/
  coded_dataset.csv          50 studies x 30+ hand-coded variables, every value traceable
  CODEBOOK.csv               definition and coding rule for every variable
  statistical_results.txt    full statistical output
  ANALYSIS_REPORT.md         the five findings that carry the paper, with limitations
  Tables/                    T01-T13, manuscript-ready
  Analysis_Pipeline/         the scripts; re-running them reproduces everything exactly
  TABLE_CAPTIONS.md          caption text for T01-T13
07_Figures/                  Figures 01-14 at 300 dpi, plus vector_pdf/ for submission
  FIGURE_CAPTIONS.md         caption text for Figures 1-14
08_Paper_Drafts/             outline, results scaffold, and both caption files
```

### The five findings

1. **A reporting ceiling.** Only 27 of 50 studies report a commensurable accuracy; median 99.03%, 52% report >= 99%, 89% report >= 95%. Strongly left-skewed (skewness -1.46), non-normal (Shapiro-Wilk p = 6.3e-05).
2. **Rigour does not predict a more conservative claim — a null result.** Accuracy is uncorrelated with the Evidential Rigour Index (rho = -0.097, p = 0.631) and with the appraisal score (rho = -0.099, p = 0.623). All Holm-adjusted p = 1.000. Reported as a null, not spun.
3. **Reporting collapses past the first metric.** 82% report a baseline; 18% report MCC or AUC; **6% report any dispersion on their headline number**; 6% report model size.
4. **A deployment cliff.** 39/50 never leave offline public-dataset evaluation. Two validate on named constrained hardware. One uses real multi-site clinical data.
5. **Benchmark monoculture.** CICIoMT2024 in 11/50, WUSTL-EHMS-2020 in 10/50; 20 studies name no public benchmark. Accuracy does not differ across benchmark strata (Kruskal-Wallis p = 0.870).

### Figure inventory

| Figure | Content |
|---|---|
| 01 | PRISMA 2020 flow |
| 02 | Performance ceiling — raincloud and ECDF |
| 03 | Rigour-performance decoupling with bootstrap bands |
| 04 | Reporting-practice forest plot with Wilson intervals |
| 05 | UpSet plot of metric-reporting combinations |
| 06 | Alluvial: theme to learning topology to deployment readiness |
| 07 | Study-by-benchmark incidence matrix |
| 08 | Quality-appraisal heatmap with Ward clustering |
| 09 | Technique co-occurrence chord diagram |
| 10 | The deployment cliff — waffle and survival |
| 11 | Country co-authorship network |
| 12 | 2025 vs 2026 reporting-practice slopegraph |
| 13 | Evidence-practice radar by theme |
| 14 | Metric-space map: why the literature cannot be pooled |

### Table inventory

T01 comparison of related reviews · T02 characteristics of the 50 · T03 benchmark usage and verified sizes ·
T04 technique family by theme · T05 performance by task · T06 accuracy by stratum · T07 evidential rigour by theme ·
T08 deployment readiness with evidence · T09 threat classes · T10 appraisal item profile ·
T11 reporting-practice indicators · T12 research gaps with supporting study IDs · T13 worked appraisal example

### Figure convention

The figure files carry **no embedded title, subtitle, caption or explanatory note** — only data, axes, tick
labels and legend, which is what journals require and what keeps the artwork from reading as machine-generated.
Every piece of explanatory text that would otherwise sit inside a panel has been moved into
`07_Figures/FIGURE_CAPTIONS.md` in journal caption form: statistics, sample sizes, coding rules, the identity of
the named studies in Figure 10, and the provenance caveats. Paste the caption beneath its figure in the
manuscript. `06_Insight_Analysis/TABLE_CAPTIONS.md` does the same for T01-T13. Panel letters (a), (b) remain in
the artwork because they are referenced from the caption. Axis, tick and legend type is set at 11-12.5 pt at the
figure's native size, so it stays legible at single-column width.

### A caution that belongs in the Methods section

All analysis variables are coded from the **abstract-level record for all 50 studies**, including the four whose
full text was obtained, so the corpus stays internally comparable. Indicators therefore measure what is
*identifiable from the retrievable record*; the absence of an indicator is not proof that a study omitted it.
`n_datasets` counts **named public benchmarks**, not whether a study used data at all — twenty studies score zero
because they use simulated, crafted, proprietary or unnamed data.
