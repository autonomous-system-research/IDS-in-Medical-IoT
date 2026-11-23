# Statistical Analysis Report

**Review:** Intrusion detection and AI-driven security for the Internet of Medical Things, medical image data and federated healthcare settings (2025–2026)
**Analysis date:** 18 November 2026 · **n = 50 included studies**

---

## How to read this analysis

Every number below traces to a verbatim string captured from a study's retrievable record. The coded dataset
(`coded_dataset.csv`), its codebook (`CODEBOOK.csv`) and the scripts that produced every figure and table
(`Analysis_Pipeline/`) are all in this folder. Re-running `20_code.py → 21_stats.py → 22_tables.py → 23…28_fig_*.py`
reproduces the entire analysis exactly; all random procedures are seeded.

**One methodological decision governs everything.** All variables are coded from the abstract-level record for
all 50 studies, including the four whose full text was obtained. Mixing full-text depth for four studies with
abstract-level depth for forty-six would make the corpus internally incomparable. Full-text evidence is held
separately and used only to validate the abstract-level coding.

---

## The five findings that carry the paper

### 1. There is a reporting ceiling, and it is the central problem

Of the 50 included studies, only **27 report an overall accuracy for a commensurable detection task**. Within
that subset the median is **99.03%** (95% bootstrap CI 98.00–99.47), the distribution is strongly left-skewed
(skewness −1.46) and non-normal (Shapiro–Wilk p = 6.3 × 10⁻⁵). **52% report ≥99%; 89% report ≥95%.**

A literature in which nine studies in ten clear 95% on the same two benchmarks is not a literature that can
discriminate between methods. This is the finding to lead with. → **Figure 2**

### 2. Methodological rigour does not predict a more conservative claim — a null result

Reported accuracy is uncorrelated with the Evidential Rigour Index (Spearman ρ = −0.097, p = 0.631), with the
quality-appraisal score (ρ = −0.099, p = 0.623), and with the number of named benchmarks (ρ = −0.004, p = 0.985).
No individual indicator shifts the reported figure: baseline comparison (p = 0.161), robustness testing (p = 0.903),
metric beyond accuracy (p = 0.884), two or more benchmarks (p = 0.610). **All Holm-adjusted p = 1.000.**

This is reported as a null result, not spun as one. The most defensible reading is that finding 1 explains it:
with the distribution compressed against the ceiling there is almost no variance left for rigour to explain.
→ **Figure 3**

### 3. Reporting practice collapses past the first metric

Baseline comparison is near-universal (41/50, 82%). Everything that would let a reader judge a claim is not:

| Indicator | n / 50 | % | 95% Wilson CI |
|---|---|---|---|
| Reports a baseline comparison | 41 | 82% | 69–90 |
| Reports robustness / ablation / cross-dataset testing | 29 | 58% | 44–71 |
| Uses two or more named public benchmarks | 20 | 40% | 28–54 |
| Names at least one threat class in the record | 18 | 36% | 24–50 |
| Reports latency | 11 | 22% | 13–35 |
| Reports a metric beyond accuracy (MCC or AUC) | 9 | 18% | 10–31 |
| Reports energy consumption | 4 | 8% | 3–19 |
| **Reports dispersion on the headline metric (SD or CI)** | **3** | **6%** | **2–16** |
| Reports model size or parameter count | 3 | 6% | 2–16 |

Three studies in fifty report a standard deviation or confidence interval on their headline number. → **Figures 4, 5**

### 4. The deployment cliff

Against the pre-specified four-level scale: **39/50 (78%) never leave offline evaluation on public datasets.**
Eight generate their own, simulated or crafted data. **Two validate on named constrained hardware** — P10
(CNN-LSTM IDS on a Raspberry Pi fog node) and P29 (hybrid anomaly IDS on a Raspberry Pi IoMT testbed).
**One uses real multi-site clinical data** — P42 (federated cardiac CT across eight hospitals, n = 8,104 patients).

A field that proposes to defend implanted and bedside devices has produced, in two years, one study grounded in
real multi-institutional patient data. → **Figures 6, 10**

### 5. Benchmark monoculture

CICIoMT2024 appears in 11 of 50 studies and WUSTL-EHMS-2020 in 10; Edge-IIoTset in five, UNSW-NB15 and ToN-IoT in four
each. Twenty studies name no public benchmark at all. Reported accuracy does not differ significantly across
benchmark strata (Kruskal–Wallis H = 0.713, p = 0.870), which is itself the point: the benchmark is not what
separates these results. → **Figures 7, 14**

---

## Secondary findings

**Federated designs report slightly lower accuracy, not significantly so.** Federated median 98.20% (n = 8) against
non-federated 99.10% (n = 19); Mann–Whitney p = 0.211, Cliff's δ = −0.316. The 0.90-point gap is the direction the
privacy–utility literature predicts, but this corpus cannot establish it.

**Reporting practice is improving.** 2026 studies use significantly more named benchmarks than 2025 studies
(median 2 against 0, p = 0.007), score higher on the appraisal rubric (median 87 against 81, p = 0.031) and on the
Evidential Rigour Index (p = 0.004). Reported accuracy is unchanged (p = 0.961), and dispersion reporting does not
move at all. Improvement is real but confined to breadth, not to honesty about uncertainty. → **Figure 12**

**The appraisal instrument localises the weakness.** Across the 50 included studies the weakest items are Q7
publication bias (mean 6.20), Q5 independent quality rating (7.48) and Q8 heterogeneity (7.70); the strongest are
Q1 focused question (10.00) and Q9 primary data (9.34). The corpus is uniform where reporting is cheap and
uniformly weak where it is costly. → **Figure 8**

---

## Limitations of this analysis

1. **Abstract-level coding.** Full text was obtainable for four of fifty studies. Indicators measure what is
   identifiable from the retrievable record; absence of an indicator is not proof a study omitted it. This is
   stated in every figure caption that depends on it.
2. **n = 27 for the accuracy analysis.** Rank correlations on 27 observations have wide confidence intervals;
   the bootstrap bands in Figure 3 show this honestly rather than hiding it.
3. **Deployment levels are conservative.** Absence of hardware evidence is coded L0. A full-text pass would be
   expected to move some studies upward; the direction of that bias is known and stated.
4. **Threat-class coding measures visibility, not presence.**
5. **Multiple comparisons.** Section 2 is Holm-corrected. The temporal comparisons in Figure 12 are uncorrected
   and labelled exploratory.
6. **Single rater.** A second rater should confirm the appraisal scores before submission; the workbook has
   blank Rater 1 / Rater 2 fields for this.

---

## Full statistical output

```
==============================================================================
1. REPORTED DETECTION ACCURACY  (commensurable subset)
==============================================================================
n = 27 of 50 studies report an overall accuracy for a network intrusion,
anomaly or malware detection task. The remaining 23 report a non-commensurable
primary metric (F1, macro-F1, PR-AUC), a different task (image classification,
clinical utility, attack efficacy), relative improvements only, or no value.
median = 99.03%   95% bootstrap CI [98.00, 99.47]   (10,000 resamples)
mean   = 98.26%   SD = 1.98   IQR = [98.00, 99.68]
range  = 93.17% - 99.95%
  >= 99% accuracy: 14/27 = 51.9%   95% Wilson CI [34.0, 69.3]
  >= 98% accuracy: 21/27 = 77.8%   95% Wilson CI [59.2, 89.4]
  >= 95% accuracy: 24/27 = 88.9%   95% Wilson CI [71.9, 96.1]
skewness = -1.460  (strong left skew: the distribution is compressed against the ceiling)
Shapiro-Wilk W = 0.7801, p = 6.30e-05  -> non-normal; non-parametric tests used throughout

==============================================================================
2. DOES METHODOLOGICAL RIGOUR PREDICT LOWER CLAIMED ACCURACY?
==============================================================================
Evidential Rigour Index (0-4) = baseline comparison + robustness/ablation testing
+ two or more named datasets + a metric beyond accuracy (MCC or AUC).
  accuracy vs Evidential Rigour Index      rho = -0.097  p = 0.6309  95% CI [-0.481, +0.303]
  accuracy vs Quality-appraisal score      rho = -0.099  p = 0.6233  95% CI [-0.460, +0.310]
  accuracy vs Number of named datasets     rho = -0.004  p = 0.9850  95% CI [-0.336, +0.340]
  accuracy vs Citations to date            rho = +0.155  p = 0.4405  95% CI [-0.241, +0.543]

Group comparisons on reported accuracy (Mann-Whitney U, two-sided):
  baseline comparison reported           yes n=21 med=98.98% | no n=6 med=99.46% | U=38.5 p=0.1609 Cliff's d=-0.389
  robustness/ablation testing reported   yes n=12 med=99.08% | no n=15 med=98.98% | U=93.0 p=0.9027 Cliff's d=+0.033
  metric beyond accuracy reported        yes n=6 med=99.41% | no n=21 med=98.98% | U=66.0 p=0.8839 Cliff's d=+0.048
  two or more datasets used              yes n=13 med=99.13% | no n=14 med=98.64% | U=102.0 p=0.6098 Cliff's d=+0.121

Holm-Bonferroni adjusted p-values across the 7 tests in this section:
  accuracy~Evidential Rigour Index              p=0.6309  p_adj=1.0000  not significant
  accuracy~Quality-appraisal score              p=0.6233  p_adj=1.0000  not significant
  accuracy~Number of named datasets             p=0.9850  p_adj=1.0000  not significant
  accuracy~Citations to date                    p=0.4405  p_adj=1.0000  not significant
  baseline comparison reported                  p=0.1609  p_adj=1.0000  not significant
  robustness/ablation testing reported          p=0.9027  p_adj=1.0000  not significant
  metric beyond accuracy reported               p=0.8839  p_adj=1.0000  not significant
  two or more datasets used                     p=0.6098  p_adj=1.0000  not significant

==============================================================================
3. FEDERATED VERSUS CENTRALISED / EDGE PERFORMANCE
==============================================================================
federated n=8  median 98.20%  IQR [94.32, 99.40]
non-federated n=19  median 99.10%  IQR [98.00, 99.77]
Mann-Whitney U = 52.0, p = 0.2113, Cliff's delta = -0.316
median difference = +0.90 percentage points in favour of non-federated designs

==============================================================================
4. BENCHMARK EFFECTS ON REPORTED ACCURACY
==============================================================================
  CICIoMT2024                n= 7  median 99.13%  range 94.60-99.89%
  unnamed / not stated       n= 7  median 99.10%  range 97.00-99.92%
  WUSTL-EHMS-2020            n= 4  median 98.61%  range 93.50-99.61%
  other named benchmark      n= 9  median 98.30%  range 93.17-99.95%
Kruskal-Wallis across groups with n>=3: H = 0.713, p = 0.8701

==============================================================================
5. REPORTING PRACTICE ACROSS ALL 50 STUDIES
==============================================================================
  Reports a baseline comparison                           41/50 =  82%   95% CI [69, 90]
  Reports robustness / ablation / cross-dataset testing   29/50 =  58%   95% CI [44, 71]
  Reports a metric beyond accuracy (MCC or AUC)            9/50 =  18%   95% CI [10, 31]
  Reports dispersion on the headline metric (SD or CI)     3/50 =   6%   95% CI [2, 16]
  Reports latency                                         11/50 =  22%   95% CI [13, 35]
  Reports energy                                           4/50 =   8%   95% CI [3, 19]
  Reports model size or parameter count                    3/50 =   6%   95% CI [2, 16]
  Names at least one threat class in the record           18/50 =  36%   95% CI [24, 50]
  Uses two or more named datasets                         20/50 =  40%   95% CI [28, 54]
  Open access                                             47/50 =  94%   95% CI [84, 98]

==============================================================================
6. QUALITY-APPRAISAL ITEM PROFILE (n = 50 included studies)
==============================================================================
  Q1  mean 10.00  SD 0.00  min 10  max 10  | Is the review based on a focused question that is adequately formulated 
  Q2  mean 9.02  SD 1.06  min 7  max 10  | Were eligibility criteria for included and excluded studies predefined a
  Q3  mean 8.74  SD 0.88  min 7  max 10  | Did the literature search strategy use a comprehensive, systematic appro
  Q4  mean 7.86  SD 1.57  min 5  max 10  | Were titles, abstracts, and full-text articles dually and independently 
  Q5  mean 7.48  SD 1.52  min 5  max 10  | Was the quality of each included study rated independently by two or mor
  Q6  mean 8.74  SD 1.54  min 5  max 10  | Were the included studies listed along with essential characteristics an
  Q7  mean 6.20  SD 0.61  min 6  max 8  | Was the publication bias assessed?
  Q8  mean 7.70  SD 2.13  min 5  max 10  | Was heterogeneity assessed? (This question applies only to meta-analyses
  Q9  mean 9.34  SD 1.21  min 7  max 10  | Were the primary data collected and stored?
  Q10 mean 8.48  SD 0.65  min 8  max 10  | How consistent is the information obtained from one source with informat
  Weakest items: Q7, Q5, Q8

==============================================================================
7. DEPLOYMENT READINESS
==============================================================================
  L0 offline, public datasets only         39/50 =  78%  95% CI [65, 87]
  L1 own/simulated/crafted data             8/50 =  16%  95% CI [8, 29]
  L2 named constrained hardware             2/50 =   4%  95% CI [1, 13]
  L3 real multi-site clinical data          1/50 =   2%  95% CI [0, 10]

==============================================================================
8. TEMPORAL COMPARISON 2025 vs 2026
==============================================================================
  Evidential Rigour Index    2025 median 2.0 (n=25) | 2026 median 2.0 (n=25) | U=172.5 p=0.0044
  Quality-appraisal score    2025 median 81.0 (n=25) | 2026 median 87.0 (n=25) | U=201.0 p=0.0308
  Number of datasets         2025 median 0.0 (n=25) | 2026 median 2.0 (n=25) | U=179.5 p=0.0072
  Reported accuracy          2025 median 99.03% (n=15) | 2026 median 99.22% (n=12) | U=88.5 p=0.9610
```

---

## Correction log

**18 November 2026 — benchmark counts.** A cross-check of the coded benchmark field against
`05_Data_Extraction/01_metadata_extraction_all50.csv` found that the canonicalisation rule in
`20_code.py` matched the substring `cic-ids` inside `CSE-CIC-IDS2018` and `CIC-IDS2018` and so credited
P01 and P35 with CICIDS2017 as well, which is a different dataset. The rule now matches the longest
dataset name first and consumes the matched text. Corrected counts: CICIoMT2024 11 of 50 (was reported
as 14), CICIDS2017 1, CSE-CIC-IDS2018 2, Edge-IIoTset 5. Every benchmark assignment in
`coded_dataset.csv` has since been re-verified against the metadata extraction: 0 unevidenced
assignments. Statistics in section 4 are unaffected in substance (Kruskal-Wallis H = 0.713, p = 0.870).
Figure 7 and Table 3 were regenerated from the corrected coding.
