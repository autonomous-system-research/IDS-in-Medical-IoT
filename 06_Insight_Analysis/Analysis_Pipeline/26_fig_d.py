# -*- coding: utf-8 -*-
import json, sys, numpy as np, collections, re
sys.path.insert(0,'scripts')
from fig_style import *
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, PathPatch, Wedge
from matplotlib.path import Path
from matplotlib.colors import LinearSegmentedColormap
from scipy.cluster import hierarchy
from scipy.spatial.distance import pdist
setup()
R=json.load(open('analysis/coded_dataset.json'))
sel={r['paper_id']:r for r in json.load(open('work/sel_keys.json'))}
qa={r['record_id']:r for r in json.load(open('work/qa_rows.json'))['rows']}
TH_ORDER=['T1_IDS_IOMT','T2_FEDERATED_SECURITY','T3_IMAGE_SECURITY','T4_BLOCKCHAIN_HEALTHIOT']

# ---------------- FIGURE 8 ----------------
SHORT=['Focused\nquestion','Eligibility\ncriteria','Search\nstrategy','Dual\nreview','Independent\nappraisal',
       'Results\nreported','Publication\nbias','Heterogeneity','Primary data\nstored','Literature\nconsistency']
M=np.array([qa[r['record_id']]['qa_scores'] for r in R],float)
th=[r['theme'] for r in R]
Z=hierarchy.linkage(pdist(M,'euclidean'),method='ward')
order=hierarchy.dendrogram(Z,no_plot=True)['leaves']
Ms=M[order]; ths=[th[i] for i in order]
cmap=LinearSegmentedColormap.from_list('qa',['#fdf0e6','#f6d0ae','#9fc3d6','#2f6d99','#1b3f5e'])
fig=plt.figure(figsize=(13.4,7.2))
gs=fig.add_gridspec(2,3,width_ratios=[0.10,1,0.045],height_ratios=[0.11,1],
                    wspace=0.02,hspace=0.03,left=0.045,right=0.895,top=0.955,bottom=0.145)
axd=fig.add_subplot(gs[1,0])
hierarchy.dendrogram(Z,orientation='left',ax=axd,color_threshold=0,above_threshold_color=MUTE,no_labels=True)
axd.invert_yaxis(); axd.axis('off')
ax=fig.add_subplot(gs[1,1])
im=ax.imshow(Ms,aspect='auto',cmap=cmap,vmin=5,vmax=10,interpolation='nearest')
ax.set_xticks(range(10)); ax.set_xticklabels(SHORT,fontsize=10.5,color=INK)
ax.set_yticks([]); ax.tick_params(length=0)

for sp in ax.spines.values(): sp.set_visible(False)
for i in range(len(Ms)+1): ax.axhline(i-0.5,color='white',lw=0.6)
for j in range(11): ax.axvline(j-0.5,color='white',lw=0.6)
axt=fig.add_subplot(gs[0,1])
mean=Ms.mean(axis=0)
axt.bar(range(10),mean,width=0.78,color=[RUST if m<7 else (AMBER if m<8.5 else NAVY) for m in mean],lw=0)
for j,m in enumerate(mean): axt.text(j,m+0.25,f'{m:.1f}',ha='center',fontsize=10.5,color=INK)
axt.set_xlim(-0.5,9.5); axt.set_ylim(0,11.8); axt.axis('off')
axr=fig.add_subplot(gs[1,2])
for i,t_ in enumerate(ths): axr.add_patch(Rectangle((0,i-0.5),1,1,color=THEME_C[t_],lw=0))
axr.set_xlim(0,1); axr.set_ylim(len(ths)-0.5,-0.5); axr.axis('off')
cax=fig.add_axes([0.912,0.30,0.014,0.42])
cb=fig.colorbar(im,cax=cax); cb.set_label('Item score',fontsize=12); cb.ax.tick_params(labelsize=10.5)
cb.outline.set_visible(False)
h=[plt.Line2D([],[],marker='s',ls='',color=THEME_C[k],label=THEME_L[k],ms=10) for k in TH_ORDER]
fig.legend(handles=h,loc='lower center',bbox_to_anchor=(0.47,0.015),ncol=4,handletextpad=0.4,columnspacing=2.0)
save(fig,'Figure_08_quality_profile_heatmap')

# ---------------- FIGURE 9 ----------------
FAM=[('CNN',r'cnn|convolution'),('LSTM/GRU',r'lstm|gru'),('Transformer',r'transformer|attention|mamba|state.space'),
 ('Graph NN',r'graph|gnn|gat'),('Tree ensemble',r'random forest|xgboost|gradient.boost|lightgbm|catboost|adaboost|decision tree|c4\.5'),
 ('Autoencoder',r'autoencoder|\bvae\b'),('Federated',r'federat'),('Differential\nprivacy',r'differential privacy|dp-sgd'),
 ('Blockchain',r'blockchain|smart contract|pbft|ipfs'),('Explainable AI',r'shap|lime|explainab'),
 ('Metaheuristic',r'optimiz|swarm|dragonfly|zebra|grey wolf|whale|firefly|boruta|genetic'),
 ('Imbalance\nhandling',r'smote|adasyn|undersampl|oversampl|focal loss|imbalance')]
names=[f[0] for f in FAM]; n=len(names)
Mb=np.zeros((50,n),int)
for i,r in enumerate(R):
    blob=((sel[r['paper_id']]['method'] or '')+' '+(sel[r['paper_id']]['title'] or '')).lower()
    for j,(_,pat) in enumerate(FAM):
        if re.search(pat,blob): Mb[i,j]=1
C=Mb.T@Mb; tot=np.diag(C).copy()
fig,ax=plt.subplots(figsize=(10.4,10.0)); fig.subplots_adjust(left=0.02,right=0.98,top=0.98,bottom=0.02)
ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-1.40,1.40); ax.set_ylim(-1.40,1.40)
gap=np.deg2rad(2.6); total=tot.sum(); span=(2*np.pi-n*gap); ang={}; a0=np.pi/2
PAL=[NAVY,TEAL,SKY,PLUM,MOSS,'#8a9aa6',AMBER,'#c58b5a',RUST,'#5e8ca8','#9c7fa0','#7fa28c']
for j in range(n):
    w=span*tot[j]/total; ang[j]=(a0-w,a0); a0-=w+gap
for j in range(n):
    a,b=ang[j]; ax.add_patch(Wedge((0,0),1.0,np.rad2deg(a),np.rad2deg(b),width=0.075,facecolor=PAL[j],lw=0))
    mid=(a+b)/2
    ax.text(1.115*np.cos(mid),1.115*np.sin(mid),f'{names[j]}\n{tot[j]}',ha='center',va='center',
            fontsize=11.5,color=INK,linespacing=1.25)
cur={j:ang[j][0] for j in range(n)}
pairs=sorted([(i,j,C[i,j]) for i in range(n) for j in range(i+1,n) if C[i,j]>0],key=lambda x:x[2])
for i,j,w in pairs:
    wa=span*w/total; a1,a2=cur[i],cur[i]+wa; b1,b2=cur[j],cur[j]+wa; cur[i]+=wa; cur[j]+=wa
    P=lambda t:(0.925*np.cos(t),0.925*np.sin(t))
    v=[P(a1),(0,0),P(b2),P(b1),(0,0),P(a2),P(a1)]
    c=[Path.MOVETO,Path.CURVE3,Path.CURVE3,Path.LINETO,Path.CURVE3,Path.CURVE3,Path.CLOSEPOLY]
    ax.add_patch(PathPatch(Path(v,c),facecolor=PAL[i],edgecolor='none',alpha=0.30+0.06*min(w,5),zorder=1))
save(fig,'Figure_09_technique_chord')
