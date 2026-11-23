# -*- coding: utf-8 -*-
"""
PIPELINE STAGE 1 — Construction of the coded analysis dataset.

Every judgement variable below is hand-coded by the reviewer against the verbatim
string captured from the study's retrievable record (title, abstract, bibliographic
metadata).  No value is inferred from the reviewer's prior knowledge of a paper.

IMPORTANT METHODOLOGICAL DECISION
All variables are coded from the ABSTRACT-LEVEL record for all 50 studies, even for
the four studies whose full text was obtained (P02, P18, P34, P39).  This keeps the
evidence base internally comparable across the corpus.  Full-text evidence is held
separately and is used only to validate the abstract-level coding, never to upgrade
a single study's variables.
"""
import json, csv, re

sel={r['paper_id']:r for r in json.load(open('work/sel_keys.json'))}

# ---------------------------------------------------------------------------
# A. HEADLINE PERFORMANCE  (rule, pre-specified, after Adarbah et al. Sensors 2026 §2.4)
#    "the single value the original authors identify as their primary result;
#     overall classification accuracy where reported, otherwise the task-appropriate
#     primary metric."  Multi-dataset studies: the value on the healthcare/IoMT
#     dataset is taken as primary, this being an IoMT-focused review.
#    acc_ids is populated ONLY where the accuracy belongs to a network
#    intrusion / anomaly / malware detection task, so that values are commensurable.
# ---------------------------------------------------------------------------
# paper: (headline_value, headline_metric, headline_task, acc_ids, note)
HEAD = {
'P01': (97.80,'weighted F1','ids_detection', None,'in-domain weighted F1 0.978; no accuracy reported'),
'P02': (91.40,'F1','ids_detection', None,'F1 0.914 on WUSTL (IoMT dataset) taken as primary over UNSW 0.968'),
'P03': (99.03,'accuracy','ids_detection', 99.03,'binary task listed first in abstract'),
'P04': (99.61,'accuracy','ids_detection', 99.61,''),
'P05': (95.60,'PR-AUC','ids_detection', None,'feature-selection study; PR-AUC 0.956 is the headline detection metric'),
'P06': (99.43,'macro score (metric name truncated in abstract)','ids_detection', None,'CICIoMT2024; metric name not recoverable - flagged ambiguous'),
'P07': (99.87,'F1','ids_detection', None,'best configuration RF with RUS+SMOTE'),
'P08': (98.00,'accuracy','ids_detection', 98.00,'simulated WBAN'),
'P09': (99.89,'accuracy','ids_detection', 99.89,'0.9989 binary (2-class) taken as primary'),
'P10': (99.92,'accuracy','ids_detection', 99.92,''),
'P11': (99.13,'accuracy','ids_detection', 99.13,'CICIoMT2024 (medical) taken over EdgeIIoTset (industrial)'),
'P12': (94.30,'F1','ids_detection', None,'average F1 94.3% for anomaly detection; the 96.1% accuracy is for access decisions, a different task'),
'P13': (99.85,'F1','ids_detection', None,'IoMT-Traffic-Data (real traffic) taken over Crafted IoMT 100%; Slow DoS 83.08% is the worst case'),
'P14': (95.00,'accuracy','ids_detection', 95.00,''),
'P15': (98.30,'F1','ids_detection', None,'binary F1 0.983; abstract states accuracy value not recoverable'),
'P16': (98.55,'macro-F1','ids_detection', None,'RT-IoT2022'),
'P17': (98.00,'accuracy','ids_detection', 98.00,'CNN+autoencoder configuration'),
'P18': (99.75,'accuracy','ids_detection', 99.75,'CICIoMT2024 6-class'),
'P19': (99.22,'accuracy','ids_detection', 99.22,'WUSTL-EHMS-2020'),
'P20': (99.10,'accuracy','ids_detection', 99.10,'binary 0.991'),
'P21': (None,'none reported','ids_detection', None,'abstract states metrics improved but gives no values'),
'P22': (99.92,'accuracy','ids_detection', 99.92,'binary anomaly detection; multiclass categorisation 87.96%'),
'P23': (98.00,'accuracy','ids_detection', 98.00,'19-class'),
'P24': (None,'relative only','ids_detection', None,'reports accuracy loss under 1% and energy saving over 60%; no absolute value'),
'P25': (98.00,'accuracy','ids_detection', 98.00,'abstract says "up to 98%" - upper bound, flagged'),
'P26': (99.80,'accuracy','ids_detection', 99.80,''),
'P27': (97.00,'accuracy','ids_detection', 97.00,'0.97'),
'P28': (99.79,'accuracy','ids_detection', 99.79,''),
'P29': (None,'none reported','ids_detection', None,'only CPU usage below 1% reported; no detection performance in abstract'),
'P30': (98.30,'accuracy','ids_detection', 98.30,'IoT-IDS2021'),
'P31': (None,'none reported','adversarial_detection', None,'qualitative claims only'),
'P32': (None,'relative only','clinical_utility', None,'accuracy improvement 4-9% IID over baselines; no absolute value'),
'P33': (99.47,'accuracy','ids_detection', 99.47,'federated, no DP; 98.52% at eps=3.0'),
'P34': (94.60,'accuracy','ids_detection', 94.60,'federated, Local SMOTE at eps=3.0'),
'P35': (97.50,'accuracy','ids_detection', 97.50,'federated WBAN'),
'P36': (96.80,'diagnostic accuracy','clinical_utility', None,'utility metric of a privacy framework, not a detection metric'),
'P37': (93.17,'accuracy','ids_detection', 93.17,'IoT-Flock; 89.84% on CICIoT2023'),
'P38': (99.38,'validation accuracy','ids_detection', 99.38,'federated, IID setting, first of four datasets'),
'P39': (93.50,'accuracy','ids_detection', 93.50,'federated WUSTL; MCC 0.673'),
'P40': (98.90,'accuracy','malware_detection', 98.90,'federated, by round 20'),
'P41': (99.95,'accuracy','ids_detection', 99.95,'split federated'),
'P42': (None,'none reported','clinical_utility', None,'no numeric performance in abstract'),
'P43': (None,'attack efficacy','attack_efficacy', None,'reports attack success (AUC 0.92-0.99 FedMIA) and defence effect, not detection performance'),
'P44': (96.00,'clean accuracy','image_classification', None,'brain tumour MRI; not commensurable with network IDS accuracy'),
'P45': (78.05,'clean accuracy','image_classification', None,'histopathology; not commensurable with network IDS accuracy'),
'P46': (None,'attack efficacy','attack_efficacy', None,'label inference attack accuracy 0-68%; lower is better'),
'P47': (None,'none reported','image_classification', None,'no numeric values in abstract'),
'P48': (98.98,'accuracy','ids_detection', 98.98,''),
'P49': (None,'relative only','system_efficiency', None,'IDR +40%, DI +30%, TCR +15.29%, ART -39.66%; no absolute detection value'),
'P50': (None,'relative only','system_efficiency', None,'relative improvements only'),
}

# ---------------------------------------------------------------------------
# B. LEARNING TOPOLOGY  (coded from the method string)
# ---------------------------------------------------------------------------
TOPO = {
'P01':'centralised','P02':'centralised','P03':'centralised','P04':'centralised','P05':'centralised',
'P06':'centralised','P07':'centralised','P08':'centralised','P09':'centralised','P10':'edge/fog',
'P11':'centralised','P12':'edge/fog','P13':'centralised','P14':'centralised','P15':'centralised',
'P16':'centralised','P17':'centralised','P18':'centralised','P19':'centralised','P20':'centralised',
'P21':'centralised','P22':'centralised','P23':'centralised','P24':'centralised','P25':'centralised',
'P26':'edge/fog','P27':'centralised','P28':'centralised','P29':'edge/fog','P30':'centralised',
'P31':'centralised','P32':'federated','P33':'federated','P34':'federated','P35':'federated',
'P36':'federated','P37':'federated','P38':'federated','P39':'federated','P40':'federated',
'P41':'split federated','P42':'federated','P43':'federated','P44':'centralised','P45':'centralised',
'P46':'split federated','P47':'centralised','P48':'edge/fog','P49':'edge/fog','P50':'centralised',
}

# ---------------------------------------------------------------------------
# C. DEPLOYMENT-READINESS LEVEL  (pre-specified 4-level scale, after Sensors 2026 RQ2)
#    L0 offline evaluation on public dataset(s) only, no own data, no hardware
#    L1 own data generation: self-generated, crafted, simulated or proprietary data
#    L2 named constrained hardware or explicit on-device deployment
#    L3 real clinical or multi-institution patient data
#    Coded only on explicit evidence in the retrievable record.
# ---------------------------------------------------------------------------
DEPLOY = {
'P08':(1,'simulated WBAN, 50 nodes in a 20x20 m2 area'),
'P10':(2,'deployed on Raspberry Pi using fog computing'),
'P12':(1,'proprietary physiological signals alongside benchmarks'),
'P13':(1,'Crafted IoMT traffic generated by the authors'),
'P21':(1,'healthcare-specific dataset derived by the authors, 253,680 records'),
'P26':(1,'50 fog-predicted events in simulation'),
'P29':(2,'hyperparameter tuning and deployment on a Raspberry Pi IoT/IoMT testbed, self-generated dataset'),
'P36':(1,'simulated WBAN data for 200 virtual patients, cardiologist-validated ground truth'),
'P42':(3,'cardiac CT scans from eight hospitals, n = 8,104 real patients'),
'P48':(1,'simulated node configurations of 195, 585 and 1171 nodes'),
'P49':(1,'iFogSim simulation, 50 IoT devices and 10 fog nodes'),
}

# ---------------------------------------------------------------------------
# D. THREAT CLASSES IDENTIFIABLE FROM THE RETRIEVABLE RECORD
#    Explicit mentions only.  This measures reporting visibility at abstract level;
#    it is NOT a claim that a study lacks a threat model in its full text.
# ---------------------------------------------------------------------------
THREAT = {
'P02':['spoofing','data alteration','DDoS','ransomware','MITM'],
'P13':['DoS'],
'P20':['spoofing','DoS','Smurf','reconnaissance'],
'P25':['game-theoretic attacker-defender'],
'P31':['adversarial example'],
'P33':['Byzantine / malicious clients'],
'P34':['model inversion','membership inference'],
'P35':['Byzantine / malicious clients'],
'P36':['membership inference'],
'P37':['Byzantine / malicious clients'],
'P40':['data poisoning','inference attack'],
'P43':['gradient leakage','membership inference','data poisoning'],
'P44':['adversarial example'],
'P45':['adversarial example'],
'P46':['label inference'],
'P47':['adversarial example'],
'P48':['wormhole'],
'P50':['unauthorised access'],
}

# ---------------------------------------------------------------------------
# E. CANONICAL DATASET NAMES
# ---------------------------------------------------------------------------
CANON=[('ciciomt','CICIoMT2024'),('cic-iomt','CICIoMT2024'),('cic iomt','CICIoMT2024'),
 ('wustl','WUSTL-EHMS-2020'),('edge-iiot','Edge-IIoTset'),('edgeiiot','Edge-IIoTset'),
 ('unsw','UNSW-NB15'),('ton_iot','ToN-IoT'),('ton-iot','ToN-IoT'),('ton iot','ToN-IoT'),
 ('bot-iot','BoT-IoT'),('cicids2017','CICIDS2017'),('cic-ids2017','CICIDS2017'),
 ('cic ids2017','CICIDS2017'),('cicids','CICIDS2017'),('cic-ids','CICIDS2017'),
 ('cse-cic','CSE-CIC-IDS2018'),('cse cic','CSE-CIC-IDS2018'),('cicids2018','CSE-CIC-IDS2018'),
 ('cic-ids2018','CSE-CIC-IDS2018'),('cic ids2018','CSE-CIC-IDS2018'),
 ('cic-ddos','CIC-DDoS2019'),('nsl-kdd','NSL-KDD'),('iot-23','IoT-23'),('ecu-ioht','ECU-IoHT'),
 ('rt-iot','RT-IoT2022'),('mimic','MIMIC'),('iomt-traffic','IoMT-TrafficData'),('iot-flock','IoT-Flock'),
 ('ciciot2023','CICIoT2023'),('cicio t23','CICIoT2023'),('ciciot23','CICIoT2023'),('gotham','Gotham2025'),
 ('medbiot','MedBIoT'),('luna16','LUNA16'),('iq-oth','IQ-OTH/NCCD'),('drebin','Drebin'),
 ('malgenome','Malgenome'),('kronodroid','Kronodroid'),('tuandromd','TUANDROMD'),('iotid20','IoTID20'),
 ('iot-ids2021','IoT-IDS2021'),('df_iomt','DF_IOMT'),('umas','Umas'),('crafted iomt','Crafted-IoMT'),
 ('slow dos','SlowDoS'),('dos flood','DoS-Flood')]

def datasets_of(s):
    """Canonicalise the benchmark names named in a record.

    Keys are tried longest-first and the matched span is blanked out, so a
    specific name consumes its text before a shorter, more general key can
    match inside it.  Without this, 'cic-ids' matches inside 'CSE-CIC-IDS2018'
    and 'CIC-IDS2018' and credits the study with CICIDS2017 as well, which is a
    different dataset.  Fixed 18 Nov 2026 after a cross-check against
    05_Data_Extraction/01_metadata_extraction_all50.csv.
    """
    sl=(s or '').lower(); found=[]
    for k,v in sorted(CANON,key=lambda kv:-len(kv[0])):
        i=sl.find(k)
        if i<0: continue
        while i>=0:
            sl=sl[:i]+' '*len(k)+sl[i+len(k):]
            i=sl.find(k)
        if v not in found: found.append(v)
    return found

METRIC_PATTERNS={
 'accuracy':r'accurac',
 'precision':r'precision',
 'recall':r'recall|sensitivit',
 'f1':r'\bf1\b|f1-score|f-measure|macro-f1|macro score',
 'auc':r'\bauc\b|roc-auc|pr-auc',
 'mcc':r'\bmcc\b',
 'fpr':r'\bfpr\b|false positive',
 'latency':r'latenc|\bms\b|inference .*s/instance|response time',
 'energy':r'energ|\bmj\b|\bmw\b|\bj vs\b|power',
 'model_size':r'\bmb\b|params|parameter|memory',
}

rows=[]
for pid in sorted(HEAD, key=lambda x:int(x[1:])):
    s=sel[pid]
    hv,hm,ht,acc,note=HEAD[pid]
    mstr=(s['metrics'] or '')
    ds=datasets_of(s['data'])
    dl,dj = DEPLOY.get(pid,(0,'offline evaluation on public dataset(s); no own data collection or hardware evidence in the retrievable record'))
    thr=THREAT.get(pid,[])
    mflags={k:int(bool(re.search(p,mstr,re.I))) for k,p in METRIC_PATTERNS.items()}
    beyond=int(mflags['auc'] or mflags['mcc'])
    base=int((s['baseline'] or '').upper().startswith('Y'))
    rob=int((s['robust'] or '').upper().startswith('Y'))
    multi=int(bool(re.search(r'multi-?class|\d+-class|\bmacro\b',mstr,re.I)))
    unc=int(bool(re.search(r'\+-|±|confidence interval|95% ci',mstr,re.I)))
    rig=base+rob+int(len(ds)>=2)+beyond
    rows.append(dict(
      paper_id=pid, record_id=s['record_id'], doi=s['doi'], year=int(s['year']), theme=s['theme'],
      region=s['region'], journal=s['journal'], publisher=s['publisher'],
      open_access=int(str(s['oa']).lower().startswith(('true','yes','gold','green','hybrid','diamond','bronze'))),
      citations=int(re.sub(r'\D','',str(s['cited'])) or 0),
      qa_total=s['qa_total'],
      headline_value=hv, headline_metric=hm, headline_task=ht, acc_ids=acc, headline_note=note,
      n_datasets=len(ds), datasets=';'.join(ds),
      learning_topology=TOPO[pid],
      deployment_level=dl, deployment_evidence=dj,
      n_threat_classes=len(thr), threat_classes=';'.join(thr),
      baseline=base, robustness=rob, beyond_accuracy=beyond, multiclass=multi, uncertainty_reported=unc,
      evidential_rigour=rig, source_metric_string=mstr, **{f'rep_{k}':v for k,v in mflags.items()}))

cols=list(rows[0].keys())
with open('analysis/coded_dataset.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
json.dump(rows,open('analysis/coded_dataset.json','w'),indent=1)

import collections
print('coded studies:',len(rows))
print('acc_ids available:',sum(1 for r in rows if r['acc_ids'] is not None))
print('headline value available:',sum(1 for r in rows if r['headline_value'] is not None))
print('deployment levels:',dict(collections.Counter(r['deployment_level'] for r in rows)))
print('topology:',dict(collections.Counter(r['learning_topology'] for r in rows)))
print('uncertainty reported:',sum(r['uncertainty_reported'] for r in rows))
print('beyond-accuracy metric:',sum(r['beyond_accuracy'] for r in rows))
print('threat classes named:',sum(1 for r in rows if r['n_threat_classes']>0))
print('evidential rigour dist:',dict(sorted(collections.Counter(r['evidential_rigour'] for r in rows).items())))
