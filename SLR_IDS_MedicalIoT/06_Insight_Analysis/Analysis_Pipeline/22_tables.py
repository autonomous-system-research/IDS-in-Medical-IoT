# -*- coding: utf-8 -*-
"""PIPELINE STAGE 3 — Manuscript tables built from the coded extraction."""
import json, csv, numpy as np, re, collections
from scipy import stats
R=json.load(open('analysis/coded_dataset.json'))
sel={r['paper_id']:r for r in json.load(open('work/sel_keys.json'))}
ext={r['paper_id']:r for r in json.load(open('work/extraction.json'))}
qa={r['record_id']:r for r in json.load(open('work/qa_rows.json'))['rows']}
ITEMS=json.load(open('work/qa_rows.json'))['items']
T='analysis/tables/'
def W(name,hdr,rows,note=''):
    with open(T+name,'w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(hdr); w.writerows(rows)
        if note: w.writerow([]); w.writerow(['NOTE',note])
    print(f'{name:<52} {len(rows):>3} rows')

THEME={'T1_IDS_IOMT':'IDS in Medical IoT','T2_FEDERATED_SECURITY':'Federated security',
       'T3_IMAGE_SECURITY':'Medical image security','T4_BLOCKCHAIN_HEALTHIOT':'Blockchain healthcare IoT'}
def first_author(a): return (a.split(';')[0].strip() if a else 'Anon').split()[-1]

# ---- T2 Characteristics of the 50 included studies -------------------------
rows=[]
for r in sorted(R,key=lambda x:int(x['paper_id'][1:])):
    s=sel[r['paper_id']]
    rows.append([r['paper_id'], f"{first_author(s['authors'])} et al., {r['year']}", r['journal'],
      s['countries'], r['region'], THEME[r['theme']], r['learning_topology'],
      r['datasets'] or 'none named in record', r['n_datasets'],
      f"{r['headline_value']:.2f}" if r['headline_value'] is not None else 'not reported',
      r['headline_metric'], 'yes' if r['baseline'] else 'no', 'yes' if r['robustness'] else 'no',
      f"L{r['deployment_level']}", r['qa_total'], r['doi']])
W('T02_characteristics_of_included_studies.csv',
  ['Paper ID','Study','Journal','Author-affiliation countries','Region','Theme','Learning topology',
   'Named public benchmarks','n benchmarks','Headline value','Headline metric','Baseline',
   'Robustness testing','Deployment level','QA /100','DOI'], rows,
  'Headline metric selected by the pre-specified rule: overall accuracy where reported, otherwise the task-appropriate primary metric. Deployment levels: L0 offline public datasets only; L1 own/simulated/crafted data; L2 named constrained hardware; L3 real multi-site clinical data.')

# ---- T3 Benchmark usage ----------------------------------------------------
cnt=collections.Counter()
for r in R:
    for d in (r['datasets'].split(';') if r['datasets'] else []): cnt[d]+=1
VSIZE={'CICIoMT2024':('approx. 4.89 million flow records in the Wi-Fi/MQTT partition (approx. 377k train / 98k test); 45 features; 40 devices (25 real, 15 simulated); 6-class and 19-class tasks','Verified from the full text of P18'),
 'WUSTL-EHMS-2020':('16,318 records (14,272 normal; 2,046 attack = 1,124 spoofing + 922 data alteration); 44 attributes (35 network-flow + 8 biometric + label)','Verified independently from the full texts of P02 and P39'),
 'Edge-IIoTset':('ML-ready partition 157,800 samples (training partition 94,680, 84.6% attack); 52 features; 14 attack types','Verified from the full text of P02'),
 'UNSW-NB15':('2,540,000+ flow records (training partition 1,524,028); 43 features after cleaning; nine attack categories','Partially verified from the full text of P02'),
 'Gotham2025':('496,191 samples; 8 categories','Stated in the abstract of P33')}
rows=[]
for d,n in cnt.most_common():
    sz,prov=VSIZE.get(d,('not verified within this review','named by included studies; size not stated in their retrievable records'))
    ids=';'.join(sorted([r['paper_id'] for r in R if d in (r['datasets'] or '')], key=lambda x:int(x[1:])))
    rows.append([d,n,f'{n*2}%',sz,prov,ids])
W('T03_benchmark_usage_and_verified_sizes.csv',
  ['Benchmark','n studies','% of 50','Size / data amount','Provenance of the size figure','Studies'],rows,
  'Size figures are reported only where verified within this corpus. No size is taken from the reviewers prior knowledge.')

# ---- T4 Technique family x theme ------------------------------------------
FAM=[('CNN',r'cnn|convolution'),('LSTM / BiLSTM',r'lstm'),('GRU / BiGRU',r'gru'),
 ('Transformer / attention',r'transformer|attention|mamba|state.space'),('Graph neural network',r'graph|gnn|gat'),
 ('Autoencoder / VAE',r'autoencoder|\bvae\b'),('Tree ensemble (RF/XGB/boosting)',r'random forest|xgboost|gradient.boost|lightgbm|catboost|adaboost|decision tree|c4\.5'),
 ('Stacking / voting ensemble',r'ensemble|stack|voting'),('Reinforcement learning',r'reinforcement|\bdqn\b|\bppo\b|q-learning'),
 ('Federated learning',r'federat'),('Differential privacy',r'differential privacy|dp-sgd'),
 ('Homomorphic / secure aggregation',r'homomorphic|secure aggregation|secagg|\bhe\b'),
 ('Blockchain / DLT',r'blockchain|smart contract|pbft|ipfs|proof-of-authority|proof of authority'),
 ('Explainable AI (SHAP / LIME)',r'shap|lime|explainab'),('GAN / generative',r'\bgan\b|generative adversarial|diffusion'),
 ('Quantum / post-quantum',r'quantum|kyber|bb84'),('Metaheuristic optimisation',r'optimiz|swarm|dragonfly|zebra|grey wolf|whale|firefly|boruta|genetic'),
 ('Class-imbalance handling',r'smote|adasyn|undersampl|oversampl|focal loss|class.weight|imbalance')]
order=['T1_IDS_IOMT','T2_FEDERATED_SECURITY','T3_IMAGE_SECURITY','T4_BLOCKCHAIN_HEALTHIOT']
rows=[]
for nm,pat in FAM:
    per={t:0 for t in order}; tot=0; ids=[]
    for r in R:
        blob=((sel[r['paper_id']]['method'] or '')+' '+(sel[r['paper_id']]['title'] or '')).lower()
        if re.search(pat,blob): per[r['theme']]+=1; tot+=1; ids.append(r['paper_id'])
    if tot: rows.append([nm,tot,f'{tot*2}%']+[per[t] for t in order]+[';'.join(sorted(ids,key=lambda x:int(x[1:])))])
rows.sort(key=lambda x:-x[1])
W('T04_technique_family_by_theme.csv',
  ['Technique family','n studies','% of 50']+[THEME[t] for t in order]+['Studies'],rows,
  'Families are not mutually exclusive; a study using a CNN-LSTM hybrid inside a federated framework counts in three rows.')

# ---- T5 Reported performance by task and metric ---------------------------
rows=[]
for task in ['ids_detection','malware_detection','image_classification','clinical_utility','attack_efficacy','system_efficiency','adversarial_detection']:
    g=[r for r in R if r['headline_task']==task]
    if not g: continue
    v=[r['headline_value'] for r in g if r['headline_value'] is not None]
    mets=collections.Counter(r['headline_metric'] for r in g)
    rows.append([task.replace('_',' '),len(g),len(v),
      f"{np.median(v):.2f}" if v else 'n/a',
      f"{min(v):.2f}-{max(v):.2f}" if v else 'n/a',
      '; '.join(f'{k} ({n})' for k,n in mets.most_common())])
W('T05_reported_performance_by_task.csv',
  ['Primary task','n studies','n with a numeric value','Median headline value','Range','Headline metrics used'],rows,
  'Values are NOT pooled across tasks: accuracy on a network IDS task and clean accuracy on a medical image classifier are not commensurable.')

acc=[r for r in R if r['acc_ids'] is not None]
rows=[]
for key,lab in [('CICIoMT2024','CICIoMT2024'),('WUSTL-EHMS-2020','WUSTL-EHMS-2020')]:
    g=[r['acc_ids'] for r in acc if key in (r['datasets'] or '')]
    if len(g)>=2: rows.append([lab,len(g),f'{np.median(g):.2f}',f'{np.percentile(g,25):.2f}-{np.percentile(g,75):.2f}',f'{min(g):.2f}-{max(g):.2f}'])
g=[r['acc_ids'] for r in acc if r['n_datasets']==0]
rows.append(['No named public benchmark',len(g),f'{np.median(g):.2f}',f'{np.percentile(g,25):.2f}-{np.percentile(g,75):.2f}',f'{min(g):.2f}-{max(g):.2f}'])
g=[r['acc_ids'] for r in acc if r['n_datasets']>=2]
rows.append(['Two or more named benchmarks',len(g),f'{np.median(g):.2f}',f'{np.percentile(g,25):.2f}-{np.percentile(g,75):.2f}',f'{min(g):.2f}-{max(g):.2f}'])
fed=[r['acc_ids'] for r in acc if 'federated' in r['learning_topology']]
cen=[r['acc_ids'] for r in acc if 'federated' not in r['learning_topology']]
rows.append(['Federated designs',len(fed),f'{np.median(fed):.2f}',f'{np.percentile(fed,25):.2f}-{np.percentile(fed,75):.2f}',f'{min(fed):.2f}-{max(fed):.2f}'])
rows.append(['Centralised / edge designs',len(cen),f'{np.median(cen):.2f}',f'{np.percentile(cen,25):.2f}-{np.percentile(cen,75):.2f}',f'{min(cen):.2f}-{max(cen):.2f}'])
W('T06_detection_accuracy_by_stratum.csv',
  ['Stratum','n','Median accuracy (%)','IQR (%)','Range (%)'],rows,
  'Commensurable subset only: n = 27 studies reporting an overall accuracy for a network intrusion, anomaly or malware detection task. Strata overlap.')

# ---- T7 Evidential rigour by theme ----------------------------------------
rows=[]
for t in order:
    g=[r for r in R if r['theme']==t]
    rows.append([THEME[t],len(g),
      f"{sum(r['baseline'] for r in g)}/{len(g)}", f"{sum(r['robustness'] for r in g)}/{len(g)}",
      f"{sum(1 for r in g if r['n_datasets']>=2)}/{len(g)}", f"{sum(r['beyond_accuracy'] for r in g)}/{len(g)}",
      f"{sum(r['uncertainty_reported'] for r in g)}/{len(g)}",
      f"{np.mean([r['evidential_rigour'] for r in g]):.2f}", f"{np.median([r['qa_total'] for r in g]):.1f}"])
g=R
rows.append(['ALL STUDIES',50,f"{sum(r['baseline'] for r in g)}/50",f"{sum(r['robustness'] for r in g)}/50",
  f"{sum(1 for r in g if r['n_datasets']>=2)}/50",f"{sum(r['beyond_accuracy'] for r in g)}/50",
  f"{sum(r['uncertainty_reported'] for r in g)}/50",
  f"{np.mean([r['evidential_rigour'] for r in g]):.2f}",f"{np.median([r['qa_total'] for r in g]):.1f}"])
W('T07_evidential_rigour_by_theme.csv',
  ['Theme','n','Baseline compared','Robustness tested','>=2 named benchmarks','Metric beyond accuracy',
   'Dispersion reported','Mean Evidential Rigour Index (0-4)','Median QA /100'],rows,
  'Evidential Rigour Index = baseline + robustness + two or more named benchmarks + a metric beyond accuracy.')

# ---- T8 Deployment readiness ----------------------------------------------
LAB={0:'L0  Offline evaluation on public dataset(s) only',1:'L1  Own, simulated or crafted data generation',
     2:'L2  Named constrained hardware / on-device deployment',3:'L3  Real multi-site clinical data'}
rows=[]
for lv in [3,2,1,0]:
    g=[r for r in R if r['deployment_level']==lv]
    if lv==0:
        rows.append([LAB[lv],len(g),f'{len(g)*2}%','—',';'.join(sorted([r['paper_id'] for r in g],key=lambda x:int(x[1:])))])
    else:
        for r in sorted(g,key=lambda x:int(x['paper_id'][1:])):
            rows.append([LAB[lv],'','',r['deployment_evidence'],r['paper_id']])
        rows.append([LAB[lv]+'  (subtotal)',len(g),f'{len(g)*2}%','',''])
W('T08_deployment_readiness.csv',['Deployment level','n','% of 50','Evidence in the retrievable record','Studies'],rows,
  'Coded only on explicit evidence in the retrievable record. A full-text pass would be expected to reclassify some L0 studies upward.')

# ---- T9 Threat classes -----------------------------------------------------
tc=collections.Counter()
for r in R:
    for t in (r['threat_classes'].split(';') if r['threat_classes'] else []): tc[t]+=1
rows=[[t,n,f'{n*2}%',';'.join(sorted([r['paper_id'] for r in R if t in (r['threat_classes'] or '')],key=lambda x:int(x[1:])))]
      for t,n in tc.most_common()]
rows.append(['No threat class identifiable from the record',50-sum(1 for r in R if r['n_threat_classes']>0),
             f'{(50-sum(1 for r in R if r["n_threat_classes"]>0))*2}%',
             ';'.join(sorted([r['paper_id'] for r in R if r['n_threat_classes']==0],key=lambda x:int(x[1:])))])
W('T09_threat_classes_identifiable.csv',['Threat class','n studies','% of 50','Studies'],rows,
  'Measures reporting visibility at abstract level. It is NOT a claim that a study lacks a threat model in its full text.')

# ---- T10 QA item profile ---------------------------------------------------
M=np.array([qa[r['record_id']]['qa_scores'] for r in R],float)
rows=[[f'Q{i+1}',ITEMS[i],f'{M[:,i].mean():.2f}',f'{M[:,i].std(ddof=1):.2f}',int(M[:,i].min()),int(M[:,i].max()),
       int((M[:,i]>=9).sum()),int((M[:,i]<=6).sum())] for i in range(10)]
rows.append(['TOTAL','Total quality-appraisal score (/100)',f'{M.sum(axis=1).mean():.2f}',f'{M.sum(axis=1).std(ddof=1):.2f}',
             int(M.sum(axis=1).min()),int(M.sum(axis=1).max()),'',''])
W('T10_quality_appraisal_item_profile.csv',
  ['Item','Question (as in the review teams template)','Mean','SD','Min','Max','n scoring >=9','n scoring <=6'],rows)

# ---- T11 Reporting-practice indicators -------------------------------------
def wilson(k,n,z=1.96):
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return max(0,c-h),min(1,c+h)
IND=[('Reports a baseline comparison',lambda r:r['baseline']),
 ('Reports robustness, ablation or cross-dataset testing',lambda r:r['robustness']),
 ('Uses two or more named public benchmarks',lambda r:r['n_datasets']>=2),
 ('Reports a metric beyond accuracy (MCC or AUC)',lambda r:r['beyond_accuracy']),
 ('Reports latency',lambda r:r['rep_latency']),
 ('Names at least one threat class in the record',lambda r:r['n_threat_classes']>0),
 ('Reports energy consumption',lambda r:r['rep_energy']),
 ('Reports dispersion on the headline metric (SD or CI)',lambda r:r['uncertainty_reported']),
 ('Reports model size or parameter count',lambda r:r['rep_model_size']),
 ('Evaluates beyond offline public datasets (L1 or above)',lambda r:r['deployment_level']>=1),
 ('Validates on named constrained hardware (L2 or above)',lambda r:r['deployment_level']>=2)]
rows=[]
for nm,f in IND:
    k=sum(1 for r in R if f(r)); lo,hi=wilson(k,50)
    rows.append([nm,k,f'{k*2}%',f'[{lo*100:.0f}, {hi*100:.0f}]'])
rows.sort(key=lambda x:-x[1])
W('T11_reporting_practice_indicators.csv',['Indicator','n of 50','%','95% Wilson CI'],rows)

# ---- T12 Research gaps -----------------------------------------------------
GAPS=[('No dispersion reported on the headline metric',lambda r:not r['uncertainty_reported']),
 ('No metric beyond accuracy (no MCC, no AUC)',lambda r:not r['beyond_accuracy']),
 ('No model size or parameter count',lambda r:not r['rep_model_size']),
 ('No evaluation beyond offline public datasets',lambda r:r['deployment_level']==0),
 ('No threat class identifiable from the record',lambda r:r['n_threat_classes']==0),
 ('Fewer than two named public benchmarks',lambda r:r['n_datasets']<2),
 ('No latency reported',lambda r:not r['rep_latency']),
 ('No robustness, ablation or cross-dataset testing',lambda r:not r['robustness']),
 ('No explainability component',lambda r:not re.search(r'shap|lime|explainab',(sel[r['paper_id']]['method'] or '').lower())),
 ('No baseline comparison',lambda r:not r['baseline'])]
rows=[]
for nm,f in GAPS:
    ids=[r['paper_id'] for r in R if f(r)]
    rows.append([nm,len(ids),f'{len(ids)*2}%',';'.join(sorted(ids,key=lambda x:int(x[1:])))])
rows.sort(key=lambda x:-x[1])
W('T12_research_gaps_with_supporting_studies.csv',['Gap','n of 50','%','Studies exhibiting the gap'],rows)

# ---- T13 Worked QA example -------------------------------------------------
ex=max(R,key=lambda r:(r['qa_total'],r['paper_id']=='P02'))
exq=qa[ex['record_id']]
rows=[[i+1,ITEMS[i],'Yes' if exq['qa_scores'][i]>=8 else '','No' if exq['qa_scores'][i]<6 else '',
       'Other' if 6<=exq['qa_scores'][i]<8 else '',exq['qa_scores'][i],exq['qa_evidence'][i]] for i in range(10)]
rows.append(['Total','','','','',exq['qa_total'],f"Quality rating: {exq['qa_rating']} (threshold >= 75)"])
W('T13_worked_quality_assessment_example.csv',
  ['No','Quality assessment criterion','Yes','No','Other','Score /10','Evidence used'],rows,
  f"Worked example: {ex['paper_id']} - {sel[ex['paper_id']]['title']} (DOI {ex['doi']}).")
print('\nAll tables written to analysis/tables/')
