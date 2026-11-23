"""Figure 1 - PRISMA 2020 flow diagram.
Regenerated with enlarged type and no embedded title or caption; the caption
text lives in analysis/FIGURE_CAPTIONS.md.
"""
import os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

B='SLR_IDS_MedicalIoT'; F='analysis/figures'
os.makedirs(F,exist_ok=True); os.makedirs(B+'/04_PRISMA_Flow',exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','figure.facecolor':'white','pdf.fonttype':42,'ps.fonttype':42})

fig,ax=plt.subplots(figsize=(13.6,13.4)); ax.set_xlim(0,11); ax.set_ylim(1.1,15.3); ax.axis('off')
C_MAIN='#1f3b63'; C_EX='#8d2f2f'; C_FILL='#eef3fa'; C_EXF='#fdeeee'

def box(x,y,w,h,text,fill,edge,fs=11.0,bold=False):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.08,rounding_size=0.12",
                 linewidth=1.5,edgecolor=edge,facecolor=fill))
    ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=fs,color='#17202a',
            fontweight=('bold' if bold else 'normal'),linespacing=1.5)

def arrow(x1,y1,x2,y2):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=18,lw=1.5,color=C_MAIN))

LX,LW = 0.75,5.75          # left (flow) column
RX,RW = 7.05,3.90          # right (exclusion) column
CX     = LX+LW/2

for yy,lab in [(13.95,'Identification'),(10.3,'Screening'),(6.1,'Eligibility'),(2.3,'Included')]:
    ax.text(0.08,yy,lab,rotation=90,fontsize=13.5,fontweight='bold',color=C_MAIN,va='center',ha='center')

box(LX,14.0,LW,0.95,'Records identified through database searching\nOpenAlex, 14 pre-specified search strings, 17 Nov 2026\n(n = 690)',C_FILL,C_MAIN)
box(RX,14.0,RW,0.95,'Duplicate records removed\nidentical DOI (n = 93)\nsame title / version (n = 3)',C_EXF,C_EX)
arrow(LX+LW,14.47,RX,14.47)

box(LX,12.5,LW,0.85,'Unique records screened by title\n(n = 594)',C_FILL,C_MAIN)
arrow(CX,14.0,CX,13.35)
box(RX,11.22,RW,2.24,'Records excluded at title screening (n = 352)\n\n'
    'out of scope (health / security)            214\n'
    'review, survey or taxonomy                   89\n'
    'preprint, Zenodo, thesis, report             30\n'
    'no resolvable DOI                            14\n'
    'no security focus                             4\n'
    'reviewer override                             1',C_EXF,C_EX,fs=9.8)
arrow(LX+LW,12.92,RX,12.38)

box(LX,11.0,LW,0.85,'Reports sought for retrieval\n(n = 242)',C_FILL,C_MAIN)
arrow(CX,12.5,CX,11.85)
box(RX,9.85,RW,1.15,'Reports not retrieved (n = 89)\n\nvenue not indexed in Scopus, Web of\nScience, IEEE Xplore or PubMed',C_EXF,C_EX,fs=10.2)
arrow(LX+LW,11.42,RX,10.43)

box(LX,9.0,LW,0.9,'Reports assessed for eligibility\nat abstract level (n = 153)',C_FILL,C_MAIN)
arrow(CX,11.0,CX,9.9)
box(RX,7.55,RW,1.75,'Reports excluded (n = 41)\n\n'
    'conference paper or book chapter   16\n'
    'abstract not retrievable           22\n'
    'review confirmed at abstract        2\n'
    'position paper or teaching case     1',C_EXF,C_EX,fs=9.8)
arrow(LX+LW,9.45,RX,8.43)

box(LX,7.3,LW,0.95,'Studies appraised with the ten-item\nquality rubric (n = 112)',C_FILL,C_MAIN)
arrow(CX,9.0,CX,8.25)
box(RX,6.05,RW,1.05,'Studies excluded (n = 29)\n\nquality-appraisal score below 75 / 100',C_EXF,C_EX,fs=10.2)
arrow(LX+LW,7.78,RX,6.58)

box(LX,5.4,LW,0.95,'Studies meeting the quality threshold\n(score ≥ 75 / 100)   (n = 83)',C_FILL,C_MAIN)
arrow(CX,7.3,CX,6.35)
box(RX,4.20,RW,1.05,'Studies not selected (n = 33)\n\nthematic and geographic\nallocation rule',C_EXF,C_EX,fs=10.2)
arrow(LX+LW,5.88,RX,4.73)

box(LX,3.05,LW,1.35,'STUDIES INCLUDED IN THE REVIEW\n(n = 50)\n\nIDS in Medical IoT 31  ·  Federated security 10\nMedical image security 6  ·  Blockchain healthcare IoT 3',
    '#e3f0e6','#2d6a3f',fs=11.0,bold=True)
arrow(CX,5.4,CX,4.4)

box(LX,1.45,10.2,1.25,'Characteristics of the 50 included studies\n'
    '2025: 25   ·   2026: 25        European or North American affiliation: 31 (62%)        '
    'Quality-appraisal score: 75–92 (mean 82.0)','#f6f6f6','#777777',fs=10.4)
arrow(CX,3.05,CX,2.70)

fig.savefig(F+'/Figure_01_PRISMA_flow.png',dpi=300,bbox_inches='tight',facecolor='white')
fig.savefig(F+'/Figure_01_PRISMA_flow.pdf',bbox_inches='tight',facecolor='white')
fig.savefig(B+'/04_PRISMA_Flow/02_prisma_flow_diagram.png',dpi=300,bbox_inches='tight',facecolor='white')
fig.savefig(B+'/04_PRISMA_Flow/02_prisma_flow_diagram.svg',bbox_inches='tight',facecolor='white')
plt.close(fig)
print('Figure 1 regenerated')
