# -*- coding: utf-8 -*-
import json, sys, numpy as np, collections
sys.path.insert(0,'scripts')
from fig_style import *
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
setup()
R=json.load(open('analysis/coded_dataset.json'))
def wilson(k,n,z=1.96):
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return max(0,c-h),min(1,c+h)

# ---------------- FIGURE 4 ----------------
IND=[('Open access',lambda r:r['open_access'],'context'),
 ('Baseline comparison',lambda r:r['baseline'],'core'),
 ('Robustness or ablation testing',lambda r:r['robustness'],'core'),
 ('Two or more named benchmarks',lambda r:r['n_datasets']>=2,'core'),
 ('Threat class named',lambda r:r['n_threat_classes']>0,'security'),
 ('Latency reported',lambda r:r['rep_latency'],'deployment'),
 ('Evaluation beyond public datasets',lambda r:r['deployment_level']>=1,'deployment'),
 ('Metric beyond accuracy',lambda r:r['beyond_accuracy'],'core'),
 ('Energy reported',lambda r:r['rep_energy'],'deployment'),
 ('Dispersion on headline metric',lambda r:r['uncertainty_reported'],'core'),
 ('Model size reported',lambda r:r['rep_model_size'],'deployment'),
 ('Constrained-hardware validation',lambda r:r['deployment_level']>=2,'deployment')]
CAT={'core':NAVY,'security':PLUM,'deployment':AMBER,'context':MOSS}
rows=sorted([(nm,sum(1 for r in R if f(r)),cat) for nm,f,cat in IND],key=lambda x:-x[1])
fig,ax=plt.subplots(figsize=(12.4,6.6))
fig.subplots_adjust(left=0.295,right=0.955,top=0.965,bottom=0.175)
y=np.arange(len(rows))[::-1]
for i,(nm,k,cat) in enumerate(rows):
    yy=y[i]; c=CAT[cat]; p=k/50; lo,hi=wilson(k,50)
    ax.plot([lo*100,hi*100],[yy,yy],color=c,lw=3.2,solid_capstyle='round',alpha=0.42)
    ax.scatter([p*100],[yy],s=120,color=c,zorder=5,edgecolor='white',lw=1.2)
    ax.text(hi*100+2.2,yy,f'{k}/50',fontsize=11,color=INK,va='center')
ax.axvline(50,color=RULE,lw=1.1,ls='--',zorder=0)
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows],fontsize=12,color=INK)
ax.set_xlim(0,106); ax.set_ylim(-0.7,len(rows)-0.3)
ax.set_xlabel('Studies reporting the indicator (%), with 95% confidence interval')
ax.grid(axis='x',color=RULE,lw=0.6,alpha=0.6); ax.set_axisbelow(True)
ax.spines['left'].set_visible(False); ax.tick_params(axis='y',length=0)
h=[plt.Line2D([],[],marker='o',ls='',color=CAT[k],label=l,ms=10) for k,l in
   [('core','Evidential practice'),('security','Security specification'),('deployment','Deployment reporting'),('context','Access')]]
ax.legend(handles=h,loc='upper left',bbox_to_anchor=(-0.40,-0.105),ncol=4,handletextpad=0.4,columnspacing=1.8)
save(fig,'Figure_04_reporting_practice_forest')

# ---------------- FIGURE 5 ----------------
SETS=[('Accuracy','rep_accuracy'),('Precision','rep_precision'),('Recall','rep_recall'),
      ('F1','rep_f1'),('AUC','rep_auc'),('MCC','rep_mcc'),('Latency','rep_latency'),
      ('Energy','rep_energy'),('Model size','rep_model_size')]
memb={}
for r in R:
    memb.setdefault(tuple(s for s,k in SETS if r[k]),[]).append(r['paper_id'])
combos=sorted(memb.items(), key=lambda x:-len(x[1]))[:13]
fig=plt.figure(figsize=(13.6,7.4))
gs=fig.add_gridspec(2,2,width_ratios=[0.34,1],height_ratios=[1,0.95],wspace=0.17,hspace=0.05,
                    left=0.035,right=0.985,top=0.965,bottom=0.055)
axb=fig.add_subplot(gs[0,1])
for i,(k,v) in enumerate(combos):
    axb.bar(i,len(v),width=0.6,color=NAVY if len(k)>0 else RUST,alpha=0.9,lw=0)
    axb.text(i,len(v)+0.25,str(len(v)),ha='center',fontsize=11,color=INK)
axb.set_ylim(0,max(len(v) for _,v in combos)+2.2); axb.set_xlim(-0.7,len(combos)-0.3)
axb.set_ylabel('Studies'); axb.set_xticks([]); axb.spines['bottom'].set_visible(False)
axb.grid(axis='y',color=RULE,lw=0.6,alpha=0.6); axb.set_axisbelow(True)
axm=fig.add_subplot(gs[1,1])
names=[s for s,_ in SETS]; yy=np.arange(len(names))[::-1]
for j in range(len(names)):
    if j%2==0: axm.add_patch(Rectangle((-0.7,yy[j]-0.5),len(combos)+0.4,1,color='#f2f5f7',lw=0,zorder=0))
for i,(k,v) in enumerate(combos):
    idx=[names.index(s) for s in k]
    for j in range(len(names)):
        axm.scatter(i,yy[j],s=105,color=NAVY if names[j] in k else '#dde4e9',zorder=3,edgecolor='none')
    if idx: axm.plot([i,i],[yy[max(idx)],yy[min(idx)]],color=NAVY,lw=2.4,zorder=2)
    else: axm.text(i,yy[-1]-0.95,'none',ha='center',fontsize=10.5,color=RUST,va='top')
axm.set_xlim(-0.7,len(combos)-0.3); axm.set_ylim(-1.5,len(names)-0.4)
axm.set_yticks([]); axm.set_xticks([])
axm.spines['left'].set_visible(False); axm.spines['bottom'].set_visible(False); axm.tick_params(length=0)
axs=fig.add_subplot(gs[1,0])
tot={s:sum(r[k] for r in R) for s,k in SETS}
for j,n in enumerate(names):
    axs.barh(yy[j],tot[n],height=0.5,color=SKY,alpha=0.92,lw=0)
    axs.text(tot[n]+1.4,yy[j],str(tot[n]),fontsize=11,color=MUTE,va='center')
axs.set_xlim(52,0); axs.set_ylim(-1.5,len(names)-0.4)
axs.set_yticks(yy); axs.yaxis.tick_right(); axs.set_yticklabels(names,fontsize=12,color=INK)
axs.set_xlabel('Studies reporting',fontsize=11.5)
for sp in ['left','bottom','right','top']: axs.spines[sp].set_visible(False)
axs.tick_params(length=0); axs.set_xticks([])
save(fig,'Figure_05_metric_reporting_upset')
