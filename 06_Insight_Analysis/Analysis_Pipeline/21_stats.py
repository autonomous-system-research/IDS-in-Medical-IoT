# -*- coding: utf-8 -*-
"""PIPELINE STAGE 2 — Inferential and descriptive statistics."""
import json, numpy as np, csv
from scipy import stats
rng=np.random.default_rng(20261117)
R=json.load(open('analysis/coded_dataset.json'))
out=[]
def log(s=''):
    print(s); out.append(str(s))

def boot_ci(x, fn=np.median, B=10000):
    x=np.asarray(x,float); bs=[fn(rng.choice(x,size=len(x),replace=True)) for _ in range(B)]
    return float(np.percentile(bs,2.5)), float(np.percentile(bs,97.5))

def wilson(k,n,z=1.96):
    if n==0: return (0,0)
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return (max(0,c-h), min(1,c+h))

def cliffs_delta(a,b):
    a,b=np.asarray(a,float),np.asarray(b,float)
    gt=sum((x>y) for x in a for y in b); lt=sum((x<y) for x in a for y in b)
    return (gt-lt)/(len(a)*len(b))

acc=[r for r in R if r['acc_ids'] is not None]
A=np.array([r['acc_ids'] for r in acc],float)

log("="*78); log("1. REPORTED DETECTION ACCURACY  (commensurable subset)"); log("="*78)
log(f"n = {len(A)} of 50 studies report an overall accuracy for a network intrusion,")
log("anomaly or malware detection task. The remaining 23 report a non-commensurable")
log("primary metric (F1, macro-F1, PR-AUC), a different task (image classification,")
log("clinical utility, attack efficacy), relative improvements only, or no value.")
lo,hi=boot_ci(A)
log(f"median = {np.median(A):.2f}%   95% bootstrap CI [{lo:.2f}, {hi:.2f}]   (10,000 resamples)")
log(f"mean   = {A.mean():.2f}%   SD = {A.std(ddof=1):.2f}   IQR = [{np.percentile(A,25):.2f}, {np.percentile(A,75):.2f}]")
log(f"range  = {A.min():.2f}% - {A.max():.2f}%")
for t in (99,98,95):
    k=int((A>=t).sum()); l,h=wilson(k,len(A))
    log(f"  >= {t}% accuracy: {k}/{len(A)} = {k/len(A)*100:.1f}%   95% Wilson CI [{l*100:.1f}, {h*100:.1f}]")
sk=stats.skew(A); log(f"skewness = {sk:.3f}  (strong left skew: the distribution is compressed against the ceiling)")
sw=stats.shapiro(A); log(f"Shapiro-Wilk W = {sw.statistic:.4f}, p = {sw.pvalue:.2e}  -> non-normal; non-parametric tests used throughout")

log(); log("="*78); log("2. DOES METHODOLOGICAL RIGOUR PREDICT LOWER CLAIMED ACCURACY?"); log("="*78)
log("Evidential Rigour Index (0-4) = baseline comparison + robustness/ablation testing")
log("+ two or more named datasets + a metric beyond accuracy (MCC or AUC).")
tests=[]
for name,key in [('Evidential Rigour Index','evidential_rigour'),
                 ('Quality-appraisal score','qa_total'),
                 ('Number of named datasets','n_datasets'),
                 ('Citations to date','citations')]:
    x=np.array([r[key] for r in acc],float)
    rho,p=stats.spearmanr(x,A)
    bs=[stats.spearmanr(*zip(*[(x[i],A[i]) for i in rng.integers(0,len(A),len(A))]))[0] for _ in range(4000)]
    bs=[b for b in bs if not np.isnan(b)]
    log(f"  accuracy vs {name:<28} rho = {rho:+.3f}  p = {p:.4f}  "
        f"95% CI [{np.percentile(bs,2.5):+.3f}, {np.percentile(bs,97.5):+.3f}]")
    tests.append((f"accuracy~{name}",p))

log(); log("Group comparisons on reported accuracy (Mann-Whitney U, two-sided):")
for name,key in [('baseline comparison reported','baseline'),
                 ('robustness/ablation testing reported','robustness'),
                 ('metric beyond accuracy reported','beyond_accuracy'),
                 ('two or more datasets used','n_datasets')]:
    if key=='n_datasets':
        g1=[r['acc_ids'] for r in acc if r[key]>=2]; g0=[r['acc_ids'] for r in acc if r[key]<2]
    else:
        g1=[r['acc_ids'] for r in acc if r[key]==1]; g0=[r['acc_ids'] for r in acc if r[key]==0]
    if len(g1)<3 or len(g0)<3:
        log(f"  {name:<38} n too small (yes={len(g1)}, no={len(g0)}) - not tested"); continue
    u,p=stats.mannwhitneyu(g1,g0,alternative='two-sided')
    d=cliffs_delta(g1,g0)
    log(f"  {name:<38} yes n={len(g1)} med={np.median(g1):.2f}% | no n={len(g0)} med={np.median(g0):.2f}% "
        f"| U={u:.1f} p={p:.4f} Cliff's d={d:+.3f}")
    tests.append((name,p))

ps=[p for _,p in tests]; order=np.argsort(ps); m=len(ps); adj=[0]*m; run=0
for i,idx in enumerate(order):
    v=(m-i)*ps[idx]; run=max(run,v); adj[idx]=min(1.0,run)
log(); log("Holm-Bonferroni adjusted p-values across the 7 tests in this section:")
for (nm,p),a in zip(tests,adj): log(f"  {nm:<45} p={p:.4f}  p_adj={a:.4f}  {'significant' if a<0.05 else 'not significant'}")

log(); log("="*78); log("3. FEDERATED VERSUS CENTRALISED / EDGE PERFORMANCE"); log("="*78)
fed=[r['acc_ids'] for r in acc if 'federated' in r['learning_topology']]
cen=[r['acc_ids'] for r in acc if 'federated' not in r['learning_topology']]
u,p=stats.mannwhitneyu(fed,cen,alternative='two-sided')
log(f"federated n={len(fed)}  median {np.median(fed):.2f}%  IQR [{np.percentile(fed,25):.2f}, {np.percentile(fed,75):.2f}]")
log(f"non-federated n={len(cen)}  median {np.median(cen):.2f}%  IQR [{np.percentile(cen,25):.2f}, {np.percentile(cen,75):.2f}]")
log(f"Mann-Whitney U = {u:.1f}, p = {p:.4f}, Cliff's delta = {cliffs_delta(fed,cen):+.3f}")
log(f"median difference = {np.median(cen)-np.median(fed):+.2f} percentage points in favour of non-federated designs")

log(); log("="*78); log("4. BENCHMARK EFFECTS ON REPORTED ACCURACY"); log("="*78)
grp={}
for r in acc:
    ds=r['datasets'].split(';') if r['datasets'] else ['unnamed / not stated']
    key='CICIoMT2024' if 'CICIoMT2024' in ds else ('WUSTL-EHMS-2020' if 'WUSTL-EHMS-2020' in ds else
         ('unnamed / not stated' if ds==['unnamed / not stated'] else 'other named benchmark'))
    grp.setdefault(key,[]).append(r['acc_ids'])
for k,v in sorted(grp.items(), key=lambda x:-np.median(x[1])):
    log(f"  {k:<26} n={len(v):>2}  median {np.median(v):.2f}%  range {min(v):.2f}-{max(v):.2f}%")
big=[v for v in grp.values() if len(v)>=3]
if len(big)>=3:
    h,p=stats.kruskal(*big); log(f"Kruskal-Wallis across groups with n>=3: H = {h:.3f}, p = {p:.4f}")

log(); log("="*78); log("5. REPORTING PRACTICE ACROSS ALL 50 STUDIES"); log("="*78)
ind=[('Reports a baseline comparison','baseline'),('Reports robustness / ablation / cross-dataset testing','robustness'),
     ('Reports a metric beyond accuracy (MCC or AUC)','beyond_accuracy'),
     ('Reports dispersion on the headline metric (SD or CI)','uncertainty_reported'),
     ('Reports latency','rep_latency'),('Reports energy','rep_energy'),
     ('Reports model size or parameter count','rep_model_size'),
     ('Names at least one threat class in the record','_thr'),
     ('Uses two or more named datasets','_nds'),('Open access','open_access')]
for nm,k in ind:
    if k=='_thr': kk=sum(1 for r in R if r['n_threat_classes']>0)
    elif k=='_nds': kk=sum(1 for r in R if r['n_datasets']>=2)
    else: kk=sum(r[k] for r in R)
    l,h=wilson(kk,50)
    log(f"  {nm:<55} {kk:>2}/50 = {kk*2:>3}%   95% CI [{l*100:.0f}, {h*100:.0f}]")

log(); log("="*78); log("6. QUALITY-APPRAISAL ITEM PROFILE (n = 50 included studies)"); log("="*78)
qa={r['record_id']:r for r in json.load(open('work/qa_rows.json'))['rows']}
items=json.load(open('work/qa_rows.json'))['items']
M=np.array([qa[r['record_id']]['qa_scores'] for r in R],float)
for i in range(10):
    log(f"  Q{i+1:<2} mean {M[:,i].mean():.2f}  SD {M[:,i].std(ddof=1):.2f}  min {M[:,i].min():.0f}  max {M[:,i].max():.0f}  | {items[i][:72]}")
w=np.argsort(M.mean(axis=0))[:3]
log(f"  Weakest items: Q{w[0]+1}, Q{w[1]+1}, Q{w[2]+1}")

log(); log("="*78); log("7. DEPLOYMENT READINESS"); log("="*78)
lab={0:'L0 offline, public datasets only',1:'L1 own/simulated/crafted data',2:'L2 named constrained hardware',3:'L3 real multi-site clinical data'}
import collections
c=collections.Counter(r['deployment_level'] for r in R)
for k in sorted(lab):
    l,h=wilson(c[k],50)
    log(f"  {lab[k]:<40} {c[k]:>2}/50 = {c[k]*2:>3}%  95% CI [{l*100:.0f}, {h*100:.0f}]")

log(); log("="*78); log("8. TEMPORAL COMPARISON 2025 vs 2026"); log("="*78)
for nm,k in [('Evidential Rigour Index','evidential_rigour'),('Quality-appraisal score','qa_total'),('Number of datasets','n_datasets')]:
    a=[r[k] for r in R if r['year']==2025]; b=[r[k] for r in R if r['year']==2026]
    u,p=stats.mannwhitneyu(a,b,alternative='two-sided')
    log(f"  {nm:<26} 2025 median {np.median(a):.1f} (n=25) | 2026 median {np.median(b):.1f} (n=25) | U={u:.1f} p={p:.4f}")
a=[r['acc_ids'] for r in acc if r['year']==2025]; b=[r['acc_ids'] for r in acc if r['year']==2026]
u,p=stats.mannwhitneyu(a,b,alternative='two-sided')
log(f"  {'Reported accuracy':<26} 2025 median {np.median(a):.2f}% (n={len(a)}) | 2026 median {np.median(b):.2f}% (n={len(b)}) | U={u:.1f} p={p:.4f}")

open('analysis/statistical_results.txt','w',encoding='utf-8').write('\n'.join(out))
