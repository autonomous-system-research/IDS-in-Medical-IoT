# -*- coding: utf-8 -*-
"""Verification suite for the quantitative analysis layer.
Writes 06_Insight_Analysis/ANALYSIS_VERIFICATION.csv.
"""
import json, csv, io, os, re, subprocess, collections
B='SLR_IDS_MedicalIoT'
R=json.load(open('analysis/coded_dataset.json'))
ext={r['paper_id']:r for r in csv.DictReader(io.open(B+'/05_Data_Extraction/01_metadata_extraction_all50.csv',encoding='utf-8'))}
res=[]
def ck(name,cond,detail=''):
    res.append((name,'PASS' if cond else 'FAIL',str(detail)))

def dss(r):
    return [x for x in (r['datasets'] if isinstance(r['datasets'],list) else str(r['datasets']).split(';')) if x]

ck('Coded dataset has 50 studies',len(R)==50,len(R))
ck('Every study has a headline_task',all(r['headline_task'] for r in R))
ck('Every study retains its verbatim source metric string',all(r['source_metric_string'] is not None for r in R))
# pre-specified rule in 20_code.py: acc_ids only where the accuracy belongs to a
# network intrusion / anomaly / malware detection task
DET={'ids_detection','malware_detection','anomaly_detection'}
ck('acc_ids only populated for detection tasks',
   all((r['acc_ids'] in (None,'')) or r['headline_task'] in DET for r in R),
   sorted({r['headline_task'] for r in R if r['acc_ids'] not in (None,'')})) 
ck('acc_ids values within 0-100',all(0<=float(r['acc_ids'])<=100 for r in R if r['acc_ids'] not in (None,'')))
ck('headline_value within 0-100 where present',
   all(0<=float(r['headline_value'])<=100 for r in R if r['headline_value'] not in (None,'')))
ck('evidential_rigour equals its four components',
   all(r['evidential_rigour']==sum([int(bool(r['baseline'])),int(bool(r['robustness'])),
       int(len(dss(r))>=2),int(bool(r['beyond_accuracy']))]) for r in R))
ck('deployment_level in 0-3',all(r['deployment_level'] in (0,1,2,3) for r in R))
ck('every deployment level has an evidence string',all(r['deployment_evidence'] for r in R))
dc=collections.Counter(r['deployment_level'] for r in R)
ck('deployment counts reconcile 39/8/2/1',[dc[0],dc[1],dc[2],dc[3]]==[39,8,2,1],dict(dc))
ck('uncertainty_reported count is 3',sum(1 for r in R if r['uncertainty_reported'])==3)
ck('beyond_accuracy count is 9',sum(1 for r in R if r['beyond_accuracy'])==9)
ck('acc_ids subset size is 27',sum(1 for r in R if r['acc_ids'] not in (None,''))==27)
ck('paper ids P01-P50 unique',sorted(r['paper_id'] for r in R)==[f'P{i:02d}' for i in range(1,51)])
ck('DOIs unique',len({r['doi'] for r in R})==50)

# benchmark coding
norm=lambda s: re.sub(r'[^a-z0-9]','',str(s).lower())
blob={p:norm(' '.join(str(v) for v in r.values())) for p,r in ext.items()}
SHORT={'WUSTL-EHMS-2020':['wustl'],'CICIoT2023':['ciciot23','cicio t23'],'CSE-CIC-IDS2018':['cicids2018'],
       'CICIDS2017':['cicids'],'Edge-IIoTset':['edgeiiot'],'UNSW-NB15':['unsw'],'ToN-IoT':['toniot'],
       'IQ-OTH/NCCD':['iqoth'],'CICIoMT2024':['ciciomt']}
unev=[(r['paper_id'],d) for r in R for d in dss(r)
      if not any(k in blob[r['paper_id']] for k in [norm(d)]+[norm(x) for x in SHORT.get(d,[])])]
ck('every coded benchmark is evidenced in the metadata extraction',not unev,unev)
ck('CICIDS2017 is not credited to CSE-CIC-IDS2018 studies',
   all(not({'CICIDS2017','CSE-CIC-IDS2018'}<=set(dss(r))) for r in R))
cnt=collections.Counter(d for r in R for d in set(dss(r)))
usage={r['dataset']:int(r['n_studies_of_50']) for r in
       csv.DictReader(io.open(B+'/06_Insight_Analysis/01_dataset_usage_frequency.csv',encoding='utf-8'))}
ck('usage table agrees with the coded dataset',all(usage.get(k)==v for k,v in cnt.items()),
   [(k,v,usage.get(k)) for k,v in cnt.items() if usage.get(k)!=v])
ck('20 studies name no public benchmark',sum(1 for r in R if not dss(r))==20)
ck('n_datasets equals the length of the benchmark list',all(r['n_datasets']==len(dss(r)) for r in R))

# deliverables
T=B+'/06_Insight_Analysis'
ck('13 manuscript tables present',len([f for f in os.listdir(T+'/Tables') if f.endswith('.csv')])==13,13)
ck('14 figures present',len([f for f in os.listdir(B+'/07_Figures') if f.endswith('.png')])==14,14)
ck('vector PDFs present',len([f for f in os.listdir(B+'/07_Figures/vector_pdf') if f.endswith('.pdf')])==14)
ck('figure captions present',os.path.exists(B+'/07_Figures/FIGURE_CAPTIONS.md'))
ck('table captions present',os.path.exists(T+'/TABLE_CAPTIONS.md'))
ck('codebook present',os.path.exists(T+'/CODEBOOK.csv'))
ck('analysis report present',os.path.exists(T+'/ANALYSIS_REPORT.md'))
ck('pipeline scripts present',len([f for f in os.listdir(T+'/Analysis_Pipeline') if f.endswith('.py')])>=11)
t02=list(csv.DictReader(io.open(T+'/Tables/T02_characteristics_of_included_studies.csv',encoding='utf-8')))
t02d=[r for r in t02 if (list(r.values())[0] or '').startswith('P')]
ck('T02 covers 50 studies',len(t02d)==50,len(t02d))
ck('no figure embeds a caption or title helper',
   not any('def title(' in io.open('scripts/fig_style.py',encoding='utf-8').read() for _ in [0]))
out=subprocess.run(['python3','scripts/16_verify.py'],capture_output=True,text=True).stdout
m=re.search(r'(\d+)/(\d+) checks passed',out)
ck('package checks still pass',bool(m) and m.group(1)==m.group(2),m.group(0) if m else out[-120:])

with io.open(T+'/ANALYSIS_VERIFICATION.csv','w',encoding='utf-8',newline='') as f:
    w=csv.writer(f); w.writerow(['check','result','detail']); w.writerows(res)
npass=sum(1 for _,r,_ in res if r=='PASS')
print(f'{npass}/{len(res)} analysis checks passed')
for n,r,d in res:
    if r=='FAIL': print('  FAIL:',n,'::',d)
