# Figure captions

Captions are kept out of the artwork so that each figure file contains only data, axes and legend,
as journals require. Paste these into the manuscript beneath the corresponding figure.

---

**Figure 1.** PRISMA 2020 flow diagram for the review. Of 690 records identified across fourteen
pre-specified search strings, 594 remained after de-duplication, 242 passed title screening, 153 were
retained after venue eligibility, 112 were assessed at abstract level, 83 met the quality-appraisal
threshold of 75/100, and 50 were included. Exclusion reasons and counts are given at each stage.

**Figure 2.** Distribution of reported detection accuracy across the 27 of 50 included studies that
report an overall accuracy for a commensurable detection task. (a) Kernel density estimate, box plot
and individual studies, coloured by research theme; the shaded band marks the region at or above 99%.
(b) Empirical cumulative distribution with readouts at the 95%, 98% and 99% thresholds. Median 99.03%
(95% bootstrap confidence interval 98.00–99.47, 10,000 resamples); interquartile range 98.00–99.68;
skewness −1.46; Shapiro–Wilk p = 6.3 × 10⁻⁵. Studies whose primary metric is F1, macro-F1 or PR-AUC,
those measuring a different task, and those reporting relative improvements only are excluded as
non-commensurable (n = 23).

**Figure 3.** Relationship between methodological rigour and reported detection accuracy (n = 27).
(a) Accuracy against the Evidential Rigour Index, defined as the sum of four binary indicators:
baseline comparison, robustness or ablation testing, use of two or more named benchmarks, and
reporting of a metric beyond accuracy. The dashed line is an ordinary least-squares fit; the shaded
band is a 2,000-sample bootstrap 95% interval. Bars above the panel give the number of studies at each
index value. (b) Accuracy stratified by each indicator separately, shown as median and interquartile
range. No association is detected: Spearman ρ = −0.097, p = 0.631, and no individual indicator reaches
significance (Mann–Whitney p = 0.161 to 0.903; all Holm-adjusted p = 1.000).

**Figure 4.** Reporting-practice indicators across all 50 included studies, ordered by prevalence.
Points are proportions, bars are 95% Wilson score intervals, and counts are given at the right. The
dashed line marks half the corpus. Indicators are coded from each study's retrievable record; absence
of an indicator means it is not identifiable from that record rather than necessarily absent from the
full text.

**Figure 5.** Combinations of performance metrics reported across the 50 included studies, shown as an
UpSet plot. Columns are the thirteen most common combinations, ordered by frequency; filled dots mark
the metrics present in each combination and the bars above give the number of studies. Horizontal bars
at the left give each metric's total. The modal pattern is accuracy reported with precision, recall and
F1 but without any threshold-free or imbalance-robust measure; seven studies report no numeric metric
at all.

**Figure 6.** Alluvial diagram tracing all 50 included studies from research theme, through learning
topology, to the strongest deployment evidence identifiable in the retrievable record. Ribbon width is
the number of studies. Deployment levels are L0, offline evaluation on public datasets only; L1, own,
simulated or crafted data generation; L2, named constrained hardware or explicit on-device deployment;
L3, real multi-site clinical data.

**Figure 7.** Study-by-benchmark incidence matrix for the 50 included studies. A dot marks a benchmark
named in a study's retrievable record; dot colour denotes research theme. Studies are ordered by the
number of named benchmarks, given in the bars above; benchmark totals are given in the bars at the
right. Benchmarks used by a single study are collapsed into one row. Twenty studies name no public
benchmark, using simulated, crafted, proprietary or unnamed data instead.

**Figure 8.** Item-level quality-appraisal scores for the 50 included studies. Rows are studies,
ordered by Ward hierarchical clustering on the Euclidean distance between their ten-item score vectors;
the dendrogram at the left shows the clustering. Bars above give each item's mean score across the
corpus, coloured by level. The colour strip at the right denotes research theme. Scores derive from the
ten-item instrument adapted from the NIH Quality Assessment Tool and Zeng et al. (2015); the
publication-bias item is scored on an abstract-level proxy and requires full-text verification.

**Figure 9.** Co-occurrence of technique families across the 50 included studies. Arc length is the
number of studies using a family; ribbon thickness is the number of studies using both families.
Families are coded by keyword matching on the method and title of each study's retrievable record and
are not mutually exclusive, so a study combining a CNN-LSTM detector with explainable AI inside a
federated framework contributes to four families. The most frequent pairings are graph neural networks
with federated learning (7 studies), CNN with LSTM or GRU (6), and federated learning with differential
privacy (5).

**Figure 10.** Deployment readiness of the included evidence base. (a) Every included study placed on
the pre-specified four-level scale, one square per study. (b) The number of studies surviving at each
successive level of evidence, with losses marked. The two studies validated on named constrained
hardware are P10, a CNN-LSTM intrusion detector deployed on a Raspberry Pi fog node, and P29, a hybrid
anomaly detector tuned and run on a Raspberry Pi IoMT testbed. The single study grounded in real
multi-site clinical data is P42, a federated cardiac CT model trained across eight hospitals (n = 8,104
patients).

**Figure 11.** Co-authorship network of author-affiliation countries across the 50 included studies.
Node size is the number of studies with an author in that country; edge width is the number of studies
jointly authored by the two countries. Node colour denotes region, with Türkiye counted as European.
The European and North American share of this review follows from a pre-specified selection rule
applied among studies that had already met the quality threshold, and is not a property of the
underlying literature.

**Figure 12.** Reporting-practice indicators in the 25 included studies published in 2025 compared
with the 25 published in 2026. Lines connect the proportion in each year; green denotes an increase and
red a decrease. Significance is from Fisher exact tests on 2 × 2 counts, uncorrected for multiple
comparisons and reported as exploratory. The 2026 stratum is incomplete, the search having been run on
17 November 2026.

**Figure 13.** Evidence-practice profile by research theme. Each polar panel gives the proportion of
studies in that theme satisfying each reporting indicator; the dashed grey outline is the corpus-wide
profile across all 50 studies. Blockchain healthcare IoT (n = 3) and medical image security (n = 6) are
small strata and their profiles are descriptive rather than stable estimates.

**Figure 14.** The headline result of every one of the 50 included studies, positioned by the task it
measures and coloured by the metric used. Rows are different quantities and values are not comparable
across them. Attack-efficacy values are adversarial success rates, for which a lower number denotes a
better defence; system-efficiency studies report relative improvements only and appear in the no-value
column. Eleven studies report no numeric headline value. Only the first row forms the commensurable
subset analysed in Figures 2 and 3.
