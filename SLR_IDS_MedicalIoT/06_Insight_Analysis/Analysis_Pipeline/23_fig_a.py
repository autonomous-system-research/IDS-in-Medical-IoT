# -*- coding: utf-8 -*-
import json, sys, numpy as np, collections
sys.path.insert(0,'scripts')
from fig_style import *
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy import stats
setup()
R=json.load(open('analysis/coded_dataset.json'))
rng=np.random.default_rng(7)
acc=[r for r in R if r['acc_ids'] is not None]
A=np.array([r['acc_ids'] for r in acc]); TH=[r['theme'] for r in acc]

# ---------------- FIGURE 2 ----------------
fig=plt.figure(figsize=(13.0,6.0))
gs=fig.add_gridspec(1,2,width_ratios=[1.5,1],wspace=0.20,left=0.045,right=0.99,top=0.93,bottom=0.21)
ax=fig.add_subplot(gs[0,0])
ax.add_patch(Rectangle((99,-0.62),1.8,1.34,color=RUST,alpha=0.07,zorder=0))
ax.text(99.72,0.665,'≥ 99%',ha='center',va='top',fontsize=11,color=RUST)
kde=stats.gaussian_kde(A,bw_method=0.42); xs=np.linspace(A.min()-1.2,100.0,400)  # accuracy is bounded above by 100%
d=kde(xs); d=d/d.max()*0.42
ax.fill_between(xs,0.06,0.06+d,color=SKY,alpha=0.55,lw=0,zorder=2)
ax.plot(xs,0.06+d,color=NAVY,lw=1.4,zorder=3)
ax.boxplot(A,orientation='horizontal',positions=[-0.03],widths=0.10,patch_artist=True,showfliers=False,zorder=4,
   medianprops=dict(color=INK,lw=2.0),boxprops=dict(facecolor='white',edgecolor=INK,lw=1.1),
   whiskerprops=dict(color=INK,lw=1.1),capprops=dict(color=INK,lw=1.1))
jit=-0.22-rng.random(len(A))*0.26
for x,y,t in zip(A,jit,TH):
    ax.scatter(x,y,s=50,color=THEME_C[t],alpha=0.88,edgecolor='white',lw=0.8,zorder=5)
med=float(np.median(A))
ax.axvline(med,color=INK,ls=':',lw=1.3,zorder=1)
ax.set_xlim(92.3,100.9); ax.set_ylim(-0.66,0.74); ax.set_yticks([])
ax.set_xlabel('Reported overall detection accuracy (%)'); ax.spines['left'].set_visible(False)
ax.text(0.015,0.97,f'n = 27\nmedian {med:.2f}%\nIQR {np.percentile(A,25):.2f}–{np.percentile(A,75):.2f}',
        transform=ax.transAxes,va='top',fontsize=11,color=INK,
        bbox=dict(boxstyle='round,pad=0.55',fc='white',ec=RULE,lw=0.9))
h=[plt.Line2D([],[],marker='o',ls='',color=THEME_C[k],label=THEME_L[k],ms=9) for k in THEME_C if k in TH]
ax.legend(handles=h,loc='upper left',bbox_to_anchor=(0.0,-0.155),ncol=2,handletextpad=0.4,columnspacing=1.6)

ax2=fig.add_subplot(gs[0,1])
xs2=np.sort(A); ys=np.arange(1,len(xs2)+1)/len(xs2)
ax2.step(np.concatenate([[92.3],xs2]),np.concatenate([[0],ys]),where='post',color=NAVY,lw=2.2)
for t,c in [(95,MOSS),(98,AMBER),(99,RUST)]:
    p=(A>=t).mean()
    ax2.plot([92.3,t],[1-p,1-p],color=c,lw=1.1,ls='--',alpha=0.9)
    ax2.plot([t,t],[0,1-p],color=c,lw=1.1,ls='--',alpha=0.9)
    ax2.scatter([t],[1-p],s=55,color=c,zorder=5,edgecolor='white',lw=1.0)
    ax2.text(92.6,1-p+0.022,f'{p*100:.0f}% ≥ {t}%',fontsize=11,color=c)
ax2.set_xlim(92.3,100.6); ax2.set_ylim(0,1.04)
ax2.set_xlabel('Reported overall detection accuracy (%)'); ax2.set_ylabel('Cumulative proportion of studies')
ax2.grid(axis='y',color=RULE,lw=0.6,alpha=0.6); ax2.set_axisbelow(True)
fig.text(0.012,0.975,'(a)',fontsize=15,fontweight='bold',color=INK,va='top')
fig.text(0.615,0.975,'(b)',fontsize=15,fontweight='bold',color=INK,va='top')
save(fig,'Figure_02_performance_ceiling')

# ---------------- FIGURE 3 ----------------
fig=plt.figure(figsize=(13.4,6.0))
gs=fig.add_gridspec(2,2,width_ratios=[1.05,0.95],height_ratios=[0.22,1],
                    wspace=0.52,hspace=0.08,left=0.055,right=0.985,top=0.90,bottom=0.175)
axm=fig.add_subplot(gs[0,0]); ax=fig.add_subplot(gs[1,0],sharex=axm)
X=np.array([r['evidential_rigour'] for r in acc],float)
cnt=collections.Counter(X.astype(int))
for k,v in cnt.items():
    axm.bar(k,v,width=0.62,color=SKY,alpha=0.85,lw=0); axm.text(k,v+0.25,str(v),ha='center',fontsize=10.5,color=MUTE)
axm.set_ylim(0,max(cnt.values())+2.0); axm.axis('off')

jx=X+rng.normal(0,0.055,len(X))
for x,y,t in zip(jx,A,TH): ax.scatter(x,y,s=62,color=THEME_C[t],alpha=0.88,edgecolor='white',lw=0.9,zorder=4)
rho,p=stats.spearmanr(X,A); sl,ic=np.polyfit(X,A,1); xx=np.linspace(-0.3,4.3,60)
bs=[]
for _ in range(2000):
    i=rng.integers(0,len(X),len(X))
    if len(set(X[i]))>1: bs.append(np.polyval(np.polyfit(X[i],A[i],1),xx))
bs=np.array(bs)
ax.fill_between(xx,np.percentile(bs,2.5,axis=0),np.percentile(bs,97.5,axis=0),color=MUTE,alpha=0.14,lw=0,zorder=1)
ax.plot(xx,sl*xx+ic,color=INK,lw=1.7,ls='--',zorder=3)
ax.set_xlim(-0.35,4.35); ax.set_xticks(range(5)); ax.set_ylim(92.3,100.8)
ax.set_xlabel('Evidential Rigour Index (0–4)')
ax.set_ylabel('Reported detection accuracy (%)')
ax.grid(axis='y',color=RULE,lw=0.6,alpha=0.6); ax.set_axisbelow(True)
ax.text(0.03,0.065,f'ρ = {rho:+.3f},  p = {p:.3f},  n = 27',transform=ax.transAxes,fontsize=11.5,color=INK,
        bbox=dict(boxstyle='round,pad=0.5',fc='white',ec=RULE,lw=0.9))

axb=fig.add_subplot(gs[:,1])
groups=[('Baseline compared','baseline'),('Robustness tested','robustness'),
        ('≥ 2 named benchmarks','_n'),('Metric beyond accuracy','beyond_accuracy')]
yp=np.arange(len(groups))[::-1].astype(float)
for i,(lab,key) in enumerate(groups):
    y=yp[i]
    if key=='_n':
        g1=[r['acc_ids'] for r in acc if r['n_datasets']>=2]; g0=[r['acc_ids'] for r in acc if r['n_datasets']<2]
    else:
        g1=[r['acc_ids'] for r in acc if r[key]==1]; g0=[r['acc_ids'] for r in acc if r[key]==0]
    for g,off,c,mk in [(g1,0.18,NAVY,'o'),(g0,-0.18,AMBER,'s')]:
        if len(g)<1: continue
        m=np.median(g); q1,q3=np.percentile(g,[25,75])
        axb.plot([q1,q3],[y+off,y+off],color=c,lw=3.4,solid_capstyle='round',alpha=0.45)
        axb.scatter([m],[y+off],s=80,color=c,marker=mk,zorder=5,edgecolor='white',lw=1.0)
        axb.text(q3+0.18,y+off,f'n = {len(g)}',fontsize=10.5,color=c,va='center')
axb.set_yticks(yp); axb.set_yticklabels([g[0] for g in groups],fontsize=12,color=INK)
axb.set_xlim(92.4,101.6); axb.set_ylim(-0.62,len(groups)-0.38)
axb.set_xticks([94,96,98,100])
axb.set_xlabel('Reported detection accuracy (%)')
axb.grid(axis='x',color=RULE,lw=0.6,alpha=0.6); axb.set_axisbelow(True)
axb.spines['left'].set_visible(False); axb.tick_params(axis='y',length=0)
hh=[plt.Line2D([],[],marker='o',ls='',color=NAVY,label='Indicator present',ms=9),
    plt.Line2D([],[],marker='s',ls='',color=AMBER,label='Indicator absent',ms=9)]
axb.legend(handles=hh,loc='lower center',bbox_to_anchor=(0.5,-0.185),ncol=2,handletextpad=0.4,columnspacing=2.0)
fig.text(0.012,0.975,'(a)',fontsize=15,fontweight='bold',color=INK,va='top')
fig.text(0.515,0.975,'(b)',fontsize=15,fontweight='bold',color=INK,va='top')
save(fig,'Figure_03_rigour_decoupling')
