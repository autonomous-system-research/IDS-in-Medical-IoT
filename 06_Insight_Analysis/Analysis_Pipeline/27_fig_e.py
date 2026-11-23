# -*- coding: utf-8 -*-
import json, sys, numpy as np, collections, itertools
sys.path.insert(0,'scripts')
from fig_style import *
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import networkx as nx
setup()
R=json.load(open('analysis/coded_dataset.json'))
sel={r['paper_id']:r for r in json.load(open('work/sel_keys.json'))}
TH_ORDER=['T1_IDS_IOMT','T2_FEDERATED_SECURITY','T3_IMAGE_SECURITY','T4_BLOCKCHAIN_HEALTHIOT']

# ---------------- FIGURE 10 ----------------
LV={0:('L0','Public datasets only','#c2c8ce'),1:('L1','Own or simulated data',SKY),
    2:('L2','Constrained hardware',AMBER),3:('L3','Multi-site clinical data',MOSS)}
order=sorted(R,key=lambda r:(r['deployment_level'],r['theme'],int(r['paper_id'][1:])))
fig=plt.figure(figsize=(14.0,6.6))
gs=fig.add_gridspec(1,2,width_ratios=[1.35,1],wspace=0.14,left=0.035,right=0.985,top=0.96,bottom=0.215)
ax=fig.add_subplot(gs[0,0]); ax.set_aspect('equal'); ax.axis('off')
COLS=10
for i,r in enumerate(order):
    c=i%COLS; row=i//COLS; lv=r['deployment_level']
    ax.add_patch(Rectangle((c,-row),0.86,0.86,color=LV[lv][2],lw=0))
    ax.text(c+0.43,-row+0.43,r['paper_id'],ha='center',va='center',fontsize=9.2,
            color='white' if lv>0 else '#54606b')
ax.set_xlim(-0.3,COLS+0.1); ax.set_ylim(-(len(order)//COLS)-0.35,1.0)
h=[plt.Line2D([],[],marker='s',ls='',color=LV[k][2],label=f'{LV[k][0]}  {LV[k][1]}  ({sum(1 for r in R if r["deployment_level"]==k)})',ms=13) for k in [0,1,2,3]]
ax.legend(handles=h,loc='upper left',bbox_to_anchor=(-0.02,-0.02),ncol=2,handletextpad=0.6,
          labelspacing=0.7,columnspacing=1.6)
ax2=fig.add_subplot(gs[0,1])
cum=[50,sum(1 for r in R if r['deployment_level']>=1),sum(1 for r in R if r['deployment_level']>=2),
     sum(1 for r in R if r['deployment_level']>=3)]
labs=['All studies','Beyond public\ndatasets','Constrained\nhardware','Multi-site\nclinical data']
x=np.arange(4)
ax2.bar(x,cum,width=0.56,color=['#aeb7bf',SKY,AMBER,MOSS],lw=0)
for i,v in enumerate(cum): ax2.text(i,v+1.4,f'{v}',ha='center',fontsize=14,fontweight='bold',color=INK)
for i in range(3):
    ax2.annotate('',xy=(i+1,cum[i+1]+0.6),xytext=(i,cum[i]-0.6),
                 arrowprops=dict(arrowstyle='-|>',color=RUST,lw=1.5,alpha=0.85,connectionstyle='arc3,rad=-0.22'))
    ax2.text(i+0.52,(cum[i]+cum[i+1])/2+4.0,f'−{cum[i]-cum[i+1]}',ha='center',fontsize=12.5,color=RUST,fontweight='bold')
ax2.set_xticks(x); ax2.set_xticklabels(labs,fontsize=11.5,color=INK)
ax2.set_ylim(0,60); ax2.set_ylabel('Studies'); ax2.tick_params(axis='x',length=0)
ax2.grid(axis='y',color=RULE,lw=0.6,alpha=0.6); ax2.set_axisbelow(True)
fig.text(0.012,0.985,'(a)',fontsize=15,fontweight='bold',color=INK,va='top')
fig.text(0.600,0.985,'(b)',fontsize=15,fontweight='bold',color=INK,va='top')
save(fig,'Figure_10_deployment_cliff')

# ---------------- FIGURE 11 ----------------
EU={'AL','AD','AT','BY','BE','BA','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IS','IE','IT','XK','LV','LI','LT','LU','MT','MD','MC','ME','NL','MK','NO','PL','PT','RO','RU','SM','RS','SK','SI','ES','SE','CH','UA','GB','VA','TR'}
NA={'US','CA','MX'}
NAME={'SA':'Saudi Arabia','IN':'India','US':'United States','GB':'United Kingdom','PK':'Pakistan',
 'CN':'China','TR':'T\u00fcrkiye','NO':'Norway','KR':'South Korea','IT':'Italy','BD':'Bangladesh',
 'CA':'Canada','EG':'Egypt','YE':'Yemen','DE':'Germany','UG':'Uganda','SE':'Sweden','TN':'Tunisia',
 'DZ':'Algeria','AE':'United Arab Emirates','FI':'Finland','CZ':'Czechia','FR':'France','MA':'Morocco',
 'PT':'Portugal','AU':'Australia','JO':'Jordan','LR':'Liberia','TW':'Taiwan','MY':'Malaysia',
 'ID':'Indonesia','SK':'Slovakia','LB':'Lebanon','VN':'Vietnam','ET':'Ethiopia'}
OTH='#c08a3e'
def reg(c): return 'EU' if c in EU else ('NA' if c in NA else 'OT')
RC={'EU':NAVY,'NA':TEAL,'OT':OTH}

cc=collections.Counter(); E=collections.Counter()
for r in R:
    cs=[c.strip().upper() for c in (sel[r['paper_id']]['countries'] or '').split(';')
        if c.strip() and c.strip()!='NONE']
    for c in set(cs): cc[c]+=1
    for a,b in itertools.combinations(sorted(set(cs)),2): E[(a,b)]+=1

fig=plt.figure(figsize=(15.2,7.8))
gs=fig.add_gridspec(1,2,width_ratios=[1,1.52],wspace=0.03,
                    left=0.135,right=0.995,top=0.875,bottom=0.095)

# (a) ranked bars for countries appearing in two or more studies
ax=fig.add_subplot(gs[0,0])
top=[(c,n) for c,n in cc.most_common() if n>=2][::-1]
y=np.arange(len(top))
ax.barh(y,[n for _,n in top],height=0.68,color=[RC[reg(c)] for c,_ in top],lw=0)
for i,(c,n) in enumerate(top):
    ax.text(n+0.28,i,str(n),va='center',fontsize=11.5,color=INK,fontweight='bold')
ax.set_yticks(y); ax.set_yticklabels([NAME.get(c,c) for c,_ in top],fontsize=11.5)
ax.set_xlim(0,21); ax.set_ylim(-0.75,len(top)-0.25)
ax.set_xlabel('Studies')
ax.grid(axis='x',color=RULE,lw=0.6,alpha=0.6); ax.set_axisbelow(True)
ax.tick_params(axis='y',length=0)
for sp in ('top','right','left'): ax.spines[sp].set_visible(False)

# (b) collaboration network on a region-ordered ring
ax2=fig.add_subplot(gs[0,1]); ax2.set_aspect('equal'); ax2.axis('off')
groups={'EU':[],'NA':[],'OT':[]}
for c,n in cc.most_common(): groups[reg(c)].append(c)
order=[]; spans={}
GAP=np.deg2rad(9.0); N=len(cc)
free=2*np.pi-3*GAP; th=np.pi/2
for g in ('EU','NA','OT'):
    k=len(groups[g]); span=free*k/N
    spans[g]=(th,th-span)
    for i,c in enumerate(groups[g]):
        order.append((c,th-span*(i+0.5)/k))
    th-=span+GAP
ANG=dict(order)
P={c:(np.cos(a),np.sin(a)) for c,a in ANG.items()}

from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch, Arc
for (a,b),w in sorted(E.items(),key=lambda x:x[1]):
    x1,y1=P[a]; x2,y2=P[b]
    ctrl=(0.30*(x1+x2)/2,0.30*(y1+y2)/2)
    pp=PathPatch(MPath([(x1,y1),ctrl,(x2,y2)],[MPath.MOVETO,MPath.CURVE3,MPath.CURVE3]),
                 fc='none',ec=MUTE if w<3 else RUST,lw=0.7+0.95*w,
                 alpha=0.26 if w<3 else 0.55,zorder=1,capstyle='round')
    ax2.add_patch(pp)
for g,(a0,a1) in spans.items():
    ax2.add_patch(Arc((0,0),2.62,2.62,theta1=np.rad2deg(a1),theta2=np.rad2deg(a0),
                      lw=7,color=RC[g],alpha=0.9,zorder=2))
for c,a in ANG.items():
    x,y=P[c]
    ax2.scatter(x,y,s=70+cc[c]*48,color=RC[reg(c)],zorder=4,edgecolor='white',lw=1.6)
    d=np.rad2deg(a); rot=d if -90<=d<=90 else d+180
    ha='left' if -90<=d<=90 else 'right'
    ax2.text(1.10*np.cos(a),1.10*np.sin(a),c,rotation=rot,rotation_mode='anchor',
             ha=ha,va='center',fontsize=12.0,color=INK,fontweight='bold',zorder=5)
ax2.set_xlim(-1.45,1.45); ax2.set_ylim(-1.45,1.45)

h=[plt.Line2D([],[],marker='o',ls='',color=RC[k],label=l,ms=13) for k,l in
   [('EU','Europe'),('NA','North America'),('OT','Other regions')]]
h+= [plt.Line2D([],[],color=MUTE,lw=2.0,alpha=0.5,label='1-2 joint studies'),
     plt.Line2D([],[],color=RUST,lw=3.6,alpha=0.7,label='3 or more joint studies')]
fig.legend(handles=h,loc='upper center',bbox_to_anchor=(0.55,1.002),ncol=5,
           handletextpad=0.6,columnspacing=2.0,frameon=False)
fig.text(0.012,0.942,'(a)',fontsize=15,fontweight='bold',color=INK,va='top')
fig.text(0.408,0.942,'(b)',fontsize=15,fontweight='bold',color=INK,va='top')
save(fig,'Figure_11_country_network')
