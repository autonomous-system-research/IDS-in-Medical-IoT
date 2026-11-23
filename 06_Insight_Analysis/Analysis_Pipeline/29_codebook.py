import json, csv
ROWS=[
('paper_id','Stable identifier P01-P50 used across every deliverable','assigned'),
('record_id','Screening-register identifier R001-R594','assigned'),
('doi','Digital Object Identifier','verified individually against the OpenAlex index'),
('year','Publication year','OpenAlex, verified'),
('theme','T1 IDS in Medical IoT / T2 Federated security / T3 Medical image security / T4 Blockchain healthcare IoT','reviewer-coded from domain, method and title'),
('region','EU/NA if any author institution is in Europe (incl. Turkiye) or North America, else OTHER','derived from OpenAlex institution country codes'),
('journal, publisher','Venue and publisher','OpenAlex, verified'),
('open_access','1 if the record is open access','OpenAlex open_access.is_oa'),
('citations','Citation count at extraction (17-18 Nov 2026)','OpenAlex cited_by_count'),
('qa_total','Ten-item quality-appraisal score out of 100','reviewer-scored, threshold >=75'),
('headline_value','The single primary numeric result','PRE-SPECIFIED RULE: overall accuracy where reported, otherwise the task-appropriate primary metric. Multi-dataset studies: the value on the healthcare/IoMT dataset is taken as primary. Hand-coded against the verbatim metric string, which is retained in source_metric_string.'),
('headline_metric','Name of the metric the headline value belongs to','hand-coded'),
('headline_task','ids_detection / malware_detection / image_classification / clinical_utility / adversarial_detection / attack_efficacy / system_efficiency','hand-coded'),
('acc_ids','Overall accuracy, populated ONLY where the accuracy belongs to a network intrusion, anomaly or malware detection task, so that values are commensurable','hand-coded; n=27 of 50'),
('headline_note','Reviewer note recording why that value was selected','hand-written'),
('n_datasets','Number of NAMED PUBLIC BENCHMARKS identifiable from the record. NOT a count of whether the study used data: simulated, crafted, proprietary and unnamed datasets score 0.','regex canonicalisation against a fixed benchmark list'),
('datasets','Canonical benchmark names','regex canonicalisation'),
('learning_topology','centralised / edge-fog / federated / split federated','reviewer-coded from the method string'),
('deployment_level','PRE-SPECIFIED 4-LEVEL SCALE. L0 offline evaluation on public datasets only; L1 own, simulated or crafted data generation; L2 named constrained hardware or explicit on-device deployment; L3 real multi-site clinical data. Coded only on explicit evidence; absence of evidence is coded L0.','reviewer-coded, evidence string retained in deployment_evidence'),
('deployment_evidence','The verbatim evidence supporting the deployment level','hand-written'),
('n_threat_classes, threat_classes','Threat classes EXPLICITLY named in the retrievable record. Measures reporting visibility at abstract level; NOT a claim that a study lacks a threat model in its full text.','hand-coded, explicit mentions only'),
('baseline','1 if the record reports a comparison against baseline or alternative methods','abstract-level extraction'),
('robustness','1 if the record reports ablation, cross-dataset or cross-validation evidence','abstract-level extraction'),
('beyond_accuracy','1 if AUC or MCC is reported','regex on the metric string'),
('multiclass','1 if a multi-class task is reported','regex on the metric string'),
('uncertainty_reported','1 if dispersion (SD, +/- or confidence interval) is reported on the headline metric','regex on the metric string'),
('evidential_rigour','Composite 0-4 = baseline + robustness + (n_datasets>=2) + beyond_accuracy','derived'),
('rep_accuracy ... rep_model_size','Binary flags for each metric family mentioned in the metric string','regex on the metric string'),
('source_metric_string','The verbatim metric string captured from the retrievable record','verbatim; every numeric claim in this analysis traces to it'),
]
with open('analysis/CODEBOOK.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['Variable','Definition','Provenance / coding rule']); w.writerows(ROWS)
    w.writerow([])
    w.writerow(['GLOBAL NOTE','All variables are coded from the ABSTRACT-LEVEL record for all 50 studies, including the four for which full text was obtained (P02, P18, P34, P39), so that the evidence base is internally comparable. Full-text evidence is held separately and used only to validate the abstract-level coding.',''])
    w.writerow(['SEED','All bootstrap and jitter procedures use numpy default_rng(20261117) or default_rng(7) as stated in the scripts; results are exactly reproducible.',''])
print('codebook written:',len(ROWS),'variables')
