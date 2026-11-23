import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
INK='#15202b'; MUTE='#5d6b77'; RULE='#ccd4da'
NAVY='#1f3b63'; TEAL='#2f7f8f'; SKY='#6fa8c7'; PALE='#c3d9e6'
AMBER='#d08b2c'; RUST='#b4553a'; MOSS='#4f7a52'; PLUM='#7a5577'
SEQ=[NAVY,TEAL,SKY,PALE]
THEME_C={'T1_IDS_IOMT':NAVY,'T2_FEDERATED_SECURITY':TEAL,'T3_IMAGE_SECURITY':AMBER,'T4_BLOCKCHAIN_HEALTHIOT':RUST}
THEME_L={'T1_IDS_IOMT':'IDS in Medical IoT','T2_FEDERATED_SECURITY':'Federated security',
         'T3_IMAGE_SECURITY':'Medical image security','T4_BLOCKCHAIN_HEALTHIOT':'Blockchain healthcare IoT'}
def setup():
    plt.rcParams.update({
      'font.family':'DejaVu Sans','font.size':11.5,'axes.labelsize':12.5,'axes.titlesize':13,
      'xtick.labelsize':11,'ytick.labelsize':11,'legend.fontsize':11,
      'axes.edgecolor':RULE,'axes.linewidth':1.0,'axes.labelcolor':INK,
      'text.color':INK,'xtick.color':MUTE,'ytick.color':MUTE,
      'xtick.major.size':4,'ytick.major.size':4,'xtick.major.width':1.0,'ytick.major.width':1.0,
      'axes.spines.top':False,'axes.spines.right':False,
      'figure.facecolor':'white','axes.facecolor':'white','savefig.facecolor':'white',
      'legend.frameon':False,'figure.dpi':110})
def panel(ax,letter,dx=-0.085,dy=1.045):
    ax.text(dx,dy,f'({letter})',transform=ax.transAxes,fontsize=14,fontweight='bold',
            color=INK,va='top',ha='left')
def save(fig,name):
    fig.savefig(f'analysis/figures/{name}.png',dpi=300,bbox_inches='tight',facecolor='white')
    fig.savefig(f'analysis/figures/{name}.pdf',bbox_inches='tight',facecolor='white')
    plt.close(fig); print('  ->',name)
