# -*- coding: utf-8 -*-
import json, sys, numpy as np, collections
sys.path.insert(0,'scripts')
from fig_style import *
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, PathPatch
from matplotlib.path import Path
setup()
R=json.load(open('analysis/coded_dataset.json'))
TH_ORDER=['T1_IDS_IOMT','T2_FEDERATED_SECURITY','T3_IMAGE_SECURITY','T4_BLOCKCHAIN_HEALTHIOT']

def ribbon(ax,x0,x1,y0a,y0b,y1a,y1b,color,alpha=0.42):
    dx=(x1-x0)*0.42
    v=[(x0,y0a),(x0+dx,y0a),(x1-dx,y1a),(x1,y1a),(x1,y1b),(x1-dx,y1b),(x0+dx,y0b),(x0,y0b),(x0,y0a)]
    c=[Path.MOVETO,Path.CURVE4,Path.CURVE4,Path.CURVE4,Path.LINETO,Path.CURVE4,Path.CURVE4,Path.CURVE4,Path.CLOSEPOLY]
    ax.add_patch(PathPatch(Path(v,c),facecolor=color,edgecolor='none',alpha=alpha,zorder=2))

# ---------------- FIGURE 6 ----------------
TOPO=['centralised','edge/fog','federated','split federated']
DEP={0:'L0  Public datasets only',1:'L1  Own or simulated data',
     2:'L2  Constrained hardware',3:'L3  Multi-site clinical data'}
fig,ax=plt.subplots(figsize=(14.2,7.4))
fig.subplots_adjust(left=0.015,right=0.985,top=0.955,bottom=0.03)
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(-4,60)
GAP=2.6
def layout(c,order):
    pos={}; y=55.0
    for k in order:
        n=c.get(k,0)
        if n: pos[k]=(y-n,y); y-=n+GAP
    return pos
c1=collections.Counter(r['theme'] for r in R); c2=collections.Counter(r['learning_topology'] for r in R)
c3=collections.Counter(r['deployment_level'] for r in R)
p1=layout(c1,TH_ORDER); p2=layout(c2,TOPO); p3=layout(c3,[0,1,2,3])
X=[1.45,4.8,8.05]; Wd=0.44
for k,(a,b) in p1.items():
    ax.add_patch(Rectangle((X[0]-Wd,a),Wd*2,b-a,color=THEME_C[k],lw=0,zorder=4))
    ax.text(X[0]-Wd-0.26,(a+b)/2,f'{THEME_L[k]}\n{c1[k]}',ha='right',va='center',fontsize=12,color=INK)
for k,(a,b) in p2.items():
    ax.add_patch(Rectangle((X[1]-Wd,a),Wd*2,b-a,color=MUTE,lw=0,alpha=0.85,zorder=4))
    ax.text(X[1],b+1.7,f'{k}  {c2[k]}',ha='center',va='bottom',fontsize=11.5,color=INK)
DEPC={0:'#c2c8ce',1:SKY,2:AMBER,3:MOSS}
ly={}
for k,(a,b) in p3.items():
    ax.add_patch(Rectangle((X[2]-Wd,a),Wd*2,b-a,color=DEPC[k],lw=0,zorder=4)); ly[k]=(a+b)/2
ks=sorted(ly,key=lambda k:-ly[k]); MIN=8.0
for i in range(1,len(ks)):
    if ly[ks[i-1]]-ly[ks[i]]<MIN: ly[ks[i]]=ly[ks[i-1]]-MIN
for k in ks:
    a,b=p3[k]; my=(a+b)/2
    if abs(ly[k]-my)>0.4: ax.plot([X[2]+Wd,X[2]+Wd+0.3],[my,ly[k]],color=MUTE,lw=0.9,zorder=5)
    ax.text(X[2]+Wd+0.36,ly[k],f'{DEP[k]}\n{c3[k]}',ha='left',va='center',fontsize=12,color=INK)
cur1={k:v[0] for k,v in p1.items()}; cur2a={k:v[0] for k,v in p2.items()}
f12=collections.Counter((r['theme'],r['learning_topology']) for r in R)
for th in TH_ORDER:
    for tp in TOPO:
        n=f12.get((th,tp),0)
        if not n: continue
        ribbon(ax,X[0]+Wd,X[1]-Wd,cur1[th],cur1[th]+n,cur2a[tp],cur2a[tp]+n,THEME_C[th]); cur1[th]+=n; cur2a[tp]+=n
cur2b={k:v[0] for k,v in p2.items()}; cur3={k:v[0] for k,v in p3.items()}
f23=collections.Counter((r['learning_topology'],r['deployment_level']) for r in R)
for tp in TOPO:
    for dp in [0,1,2,3]:
        n=f23.get((tp,dp),0)
        if not n: continue
        ribbon(ax,X[1]+Wd,X[2]-Wd,cur2b[tp],cur2b[tp]+n,cur3[dp],cur3[dp]+n,DEPC[dp],alpha=0.55); cur2b[tp]+=n; cur3[dp]+=n
for x,lab in zip(X,['Research theme','Learning topology','Deployment readiness']):
    ax.text(x,58.6,lab,ha='center',fontsize=13.5,fontweight='bold',color=INK)
save(fig,'Figure_06_alluvial_deployment')

# ---------------- FIGURE 7 ----------------
cnt=collections.Counter()
for r in R:
    for d in (r['datasets'].split(';') if r['datasets'] else []): cnt[d]+=1
ds=[d for d,_ in cnt.most_common() if cnt[d]>=2]; others=[d for d in cnt if cnt[d]==1]
rows=ds+['Other single-use','None named']
studies=sorted(R,key=lambda r:(-r['n_datasets'],r['theme'],int(r['paper_id'][1:])))
fig=plt.figure(figsize=(16.4,7.8))
gs=fig.add_gridspec(2,2,width_ratios=[1,0.13],height_ratios=[0.19,1],wspace=0.015,hspace=0.025,
                    left=0.135,right=0.985,top=0.965,bottom=0.155)
ax=fig.add_subplot(gs[1,0]); axt=fig.add_subplot(gs[0,0]); axr=fig.add_subplot(gs[1,1])
yy=np.arange(len(rows))[::-1]
for j in range(len(rows)):
    if j%2==0: ax.add_patch(Rectangle((-0.6,yy[j]-0.5),len(studies)+0.2,1,color='#f2f5f7',lw=0,zorder=0))
for i,r in enumerate(studies):
    mine=set(r['datasets'].split(';')) if r['datasets'] else set()
    for j,d in enumerate(rows):
        on=(d in mine) if d in ds else (bool(mine & set(others)) if d=='Other single-use' else (not mine))
        if on: ax.scatter(i,yy[j],s=62,color=THEME_C[r['theme']],zorder=3,edgecolor='none')
ax.set_yticks(yy); ax.set_yticklabels(rows,fontsize=12,color=INK)
ax.set_xticks(range(len(studies)))
ax.set_xticklabels([r['paper_id'] for r in studies],fontsize=8.6,rotation=90,color=MUTE)
ax.set_xlim(-0.7,len(studies)-0.3); ax.set_ylim(-0.7,len(rows)-0.4)
ax.tick_params(length=0); ax.spines['left'].set_visible(False); ax.spines['bottom'].set_visible(False)
for i,r in enumerate(studies): axt.bar(i,r['n_datasets'],width=0.6,color=SKY,alpha=0.92,lw=0)
axt.set_xlim(-0.7,len(studies)-0.3); axt.set_ylim(0,7); axt.set_xticks([]); axt.set_yticks([0,3,6])
axt.set_ylabel('Benchmarks',fontsize=11.5)
axt.spines['bottom'].set_visible(False); axt.grid(axis='y',color=RULE,lw=0.6,alpha=0.6); axt.set_axisbelow(True)
tot=[cnt[d] for d in ds]+[len(others),sum(1 for r in R if not r['datasets'])]
for j,v in enumerate(tot):
    axr.barh(yy[j],v,height=0.5,color=NAVY if j<len(ds) else '#b2bcc4',alpha=0.92,lw=0)
    axr.text(v+0.6,yy[j],str(v),fontsize=11,color=MUTE,va='center')
axr.set_xlim(0,27); axr.set_ylim(-0.7,len(rows)-0.4); axr.set_yticks([]); axr.set_xticks([])
for sp in ['left','top','right','bottom']: axr.spines[sp].set_visible(False)
axr.set_xlabel('Studies',fontsize=11.5)
h=[plt.Line2D([],[],marker='o',ls='',color=THEME_C[k],label=THEME_L[k],ms=10) for k in TH_ORDER]
ax.legend(handles=h,loc='upper left',bbox_to_anchor=(-0.155,-0.115),ncol=4,handletextpad=0.4,columnspacing=2.0)
save(fig,'Figure_07_benchmark_matrix')
