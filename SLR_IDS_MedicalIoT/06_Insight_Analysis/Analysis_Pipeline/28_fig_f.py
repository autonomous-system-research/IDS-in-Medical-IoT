# -*- coding: utf-8 -*-
import json, sys, numpy as np, collections
sys.path.insert(0,'scripts')
from fig_style import *
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy import stats
setup()
R=json.load(open('analysis/coded_dataset.json'))
TH_ORDER=['T1_IDS_IOMT','T2_FEDERATED_SECURITY','T3_IMAGE_SECURITY','T4_BLOCKCHAIN_HEALTHIOT']

# ---------------- FIGURE 12 ----------------
IND=[('Two or more named benchmarks',lambda r:r['n_datasets']>=2),
     ('Robustness or ablation testing',lambda r:r['robustness']),
     ('Baseline comparison',lambda r:r['baseline']),
     ('Metric beyond accuracy',lambda r:r['beyond_accuracy']),
     ('Threat class named',lambda r:r['n_threat_classes']>0),
     ('Latency reported',lambda r:r['rep_latency']),
     ('Evaluation beyond public datasets',lambda r:r['deployment_level']>=1),
     ('Dispersion on headline metric',lambda r:r['uncertainty_reported'])]
a=[r for r in R if r['year']==2025]; b=[r for r in R if r['year']==2026]
rows=[]
for nm,f in IND:
    k1=sum(1 for r in a if f(r)); k2=sum(1 for r in b if f(r))
    _,pv=stats.fisher_exact([[k1,len(a)-k1],[k2,len(b)-k2]])
    rows.append((nm,k1/len(a)*100,k2/len(b)*100,pv))
rows.sort(key=lambda x:-(x[2]-x[1]))
def decollide(v,minsep=6.4):
    idx=sorted(range(len(v)),key=lambda i:-v[i]); out=list(v)
    for k in range(1,len(idx)):
        if out[idx[k-1]]-out[idx[k]]<minsep: out[idx[k]]=out[idx[k-1]]-minsep
    return out
L=decollide([r[1] for r in rows]); Rg=decollide([r[2] for r in rows])
fig,ax=plt.subplots(figsize=(13.0,7.0)); fig.subplots_adjust(left=0.345,right=0.845,top=0.955,bottom=0.115)
for i,(nm,p1,p2,pv) in enumerate(rows):
    d=p2-p1; c=MOSS if d>0 else (RUST if d<0 else MUTE)
    ax.plot([0,1],[p1,p2],color=c,lw=2.6,alpha=0.88,zorder=3,solid_capstyle='round')
    ax.scatter([0,1],[p1,p2],s=85,color=c,zorder=4,edgecolor='white',lw=1.3)
    star='**' if pv<0.01 else ('*' if pv<0.05 else '')
    if abs(L[i]-p1)>0.8: ax.plot([-0.035,-0.008],[L[i],p1],color=RULE,lw=0.9)
    if abs(Rg[i]-p2)>0.8: ax.plot([1.008,1.035],[p2,Rg[i]],color=RULE,lw=0.9)
    ax.text(-0.048,L[i],f'{nm}   {p1:.0f}%',ha='right',va='center',fontsize=12,color=INK)
    ax.text(1.048,Rg[i],f'{p2:.0f}%{star}',ha='left',va='center',fontsize=12,color=c)
ax.set_xlim(-0.02,1.02); ax.set_ylim(-6,103)
ax.set_xticks([0,1]); ax.set_xticklabels(['2025  (n = 25)','2026  (n = 25)'],fontsize=13,color=INK)
ax.set_yticks([]); ax.tick_params(axis='x',length=0)
ax.spines['bottom'].set_visible(False); ax.spines['left'].set_visible(False)
ax.text(0.5,-0.095,'*  p < 0.05      **  p < 0.01',ha='center',fontsize=11,color=MUTE,transform=ax.transAxes)
save(fig,'Figure_12_temporal_slopegraph')

# ---------------- FIGURE 13 ----------------
AX=[('Baseline\ncompared',lambda r:r['baseline']),('Robustness\ntested',lambda r:r['robustness']),
    ('≥ 2\nbenchmarks',lambda r:r['n_datasets']>=2),('Metric beyond\naccuracy',lambda r:r['beyond_accuracy']),
    ('Latency\nreported',lambda r:r['rep_latency']),('Threat class\nnamed',lambda r:r['n_threat_classes']>0),
    ('Beyond public\ndatasets',lambda r:r['deployment_level']>=1)]
fig=plt.figure(figsize=(14.6,5.4)); fig.subplots_adjust(left=0.025,right=0.975,top=0.80,bottom=0.115,wspace=0.34)
k=len(AX); angles=np.linspace(0,2*np.pi,k,endpoint=False)
allv=[sum(1 for r in R if f(r))/50 for _,f in AX]
for q,th in enumerate(TH_ORDER):
    axp=fig.add_subplot(1,4,q+1,polar=True)
    g=[r for r in R if r['theme']==th]
    v=[sum(1 for r in g if f(r))/len(g) for _,f in AX]
    aa=np.concatenate([angles,[angles[0]]])
    axp.plot(aa,np.concatenate([allv,[allv[0]]]),color=MUTE,lw=1.4,ls='--',alpha=0.8,zorder=2)
    axp.plot(aa,np.concatenate([v,[v[0]]]),color=THEME_C[th],lw=2.6,zorder=3)
    axp.fill(aa,np.concatenate([v,[v[0]]]),color=THEME_C[th],alpha=0.22,zorder=1)
    axp.set_xticks(angles); axp.set_xticklabels([x[0] for x in AX],fontsize=9.5,color=INK)
    axp.set_ylim(0,1); axp.set_yticks([0.5,1.0]); axp.set_yticklabels([])
    for rv,lb in [(0.5,'50'),(1.0,'100%')]:
        axp.text(np.deg2rad(22.5),rv,lb,fontsize=10,color=MUTE,ha='center',va='center',
                 zorder=40,bbox=dict(boxstyle='round,pad=0.18',fc='white',ec='none',alpha=0.95))
    axp.tick_params(pad=3.5); axp.grid(color=RULE,lw=0.7); axp.spines['polar'].set_color(RULE)
    axp.set_title(f'{THEME_L[th]}   n = {len(g)}',fontsize=12.5,color=THEME_C[th],fontweight='bold',pad=22)
h=[plt.Line2D([],[],color=MUTE,ls='--',lw=1.6,label='All 50 included studies')]
fig.legend(handles=h,loc='lower center',bbox_to_anchor=(0.5,0.01),handletextpad=0.6)
save(fig,'Figure_13_evidence_radar_by_theme')

# ---------------- FIGURE 14 ----------------
MET_C={'accuracy':NAVY,'validation accuracy':NAVY,'clean accuracy':AMBER,'diagnostic accuracy':MOSS,
 'F1':TEAL,'weighted F1':TEAL,'macro-F1':TEAL,'macro score (metric name truncated in abstract)':'#9fb3c0','PR-AUC':PLUM}
TASK=['ids_detection','malware_detection','image_classification','clinical_utility','adversarial_detection','attack_efficacy','system_efficiency']
LAB={'ids_detection':'Intrusion / anomaly\ndetection','malware_detection':'Malware\ndetection',
 'image_classification':'Medical image\nclassification','clinical_utility':'Clinical\nutility',
 'adversarial_detection':'Adversarial\ndetection','attack_efficacy':'Attack efficacy','system_efficiency':'System\nefficiency'}
fig,ax=plt.subplots(figsize=(13.4,6.4)); fig.subplots_adjust(left=0.165,right=0.985,top=0.955,bottom=0.215)
rng=np.random.default_rng(3)
yy={t:len(TASK)-1-i for i,t in enumerate(TASK)}
for t in TASK:
    if yy[t]%2==0: ax.add_patch(Rectangle((74.6,yy[t]-0.5),28,1,color='#f2f5f7',lw=0,zorder=0))
ax.axvspan(74.6,77.2,color='#e8ecef',lw=0,zorder=1)
for r in R:
    y=yy[r['headline_task']]+rng.normal(0,0.10)
    if r['headline_value'] is None:
        ax.scatter(75.9,y,s=58,marker='x',color='#97a3ac',zorder=3,lw=1.8); continue
    ax.scatter(r['headline_value'],y,s=78,color=MET_C.get(r['headline_metric'],'#8a9aa6'),
               alpha=0.9,zorder=4,edgecolor='white',lw=0.9)
ax.text(75.9,len(TASK)-0.30,'No value',ha='center',fontsize=11,color=MUTE)
ax.set_yticks(list(yy.values())); ax.set_yticklabels([LAB[t] for t in TASK],fontsize=12,color=INK)
ax.set_xlim(74.6,101.5); ax.set_ylim(-0.75,len(TASK)-0.2)
ax.set_xlabel('Headline value as reported (%)')
ax.grid(axis='x',color=RULE,lw=0.6,alpha=0.6); ax.set_axisbelow(True)
ax.tick_params(axis='y',length=0); ax.spines['left'].set_visible(False)
h=[plt.Line2D([],[],marker='o',ls='',color=NAVY,label='Accuracy',ms=10),
   plt.Line2D([],[],marker='o',ls='',color=TEAL,label='F1 / macro-F1',ms=10),
   plt.Line2D([],[],marker='o',ls='',color=AMBER,label='Clean accuracy',ms=10),
   plt.Line2D([],[],marker='o',ls='',color=MOSS,label='Diagnostic accuracy',ms=10),
   plt.Line2D([],[],marker='o',ls='',color=PLUM,label='PR-AUC',ms=10),
   plt.Line2D([],[],marker='x',ls='',color='#97a3ac',label='No numeric value',ms=9)]
ax.legend(handles=h,loc='upper left',bbox_to_anchor=(-0.195,-0.115),ncol=6,handletextpad=0.4,columnspacing=1.5)
save(fig,'Figure_14_metric_space_map')
