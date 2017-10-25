## Ben Kite

weeks = 5

from playByPlay import pullPlaybyPlay, preparePlaybyPlay 
import pandas, numpy, re
import os
import numpy as np
from pylab import *

def ranker(s):
    rawfile = "raw_" + str(s) + ".csv"
    processedfile = "play_by_play_" + str(s) + ".csv"
    if os.path.isfile(rawfile):
        tmpdat = pandas.read_csv(rawfile)
    else:
        tmpdat = pullPlaybyPlay(s)
        tmpdat.to_csv(rawfile)
        
    dat = preparePlaybyPlay(tmpdat)
    dat.to_csv(processedfile)
      
    ## Best Passers
    pdat = dat.loc[dat["pass"] == True]
    pdat = pdat.loc[pdat["passer"] == pdat["passer"]]
    passers = numpy.unique(pdat["passer"])
    passers = passers[passers != "Two_Point"]
    
    pstats = []
    for p in passers:
        tmpdat = dat.loc[dat["passer"] == p]
        mv = numpy.mean(tmpdat["EPAchange"]) 
        mv2 = format(mv, ".3f")
        pstats.append([p, numpy.unique(tmpdat.Possession)[0], mv, mv2, len(tmpdat)])
        
    pstats = pandas.DataFrame(pstats)
    pstats.columns = ["Passer", "Team", "sortme", "Average EPA", "Attempts"]
    pstats = pstats.sort_values("sortme", ascending = False)
    pstats = pstats.loc[pstats["Attempts"] > 20 * weeks]
    pstats["Rank"] = range(1, len(pstats) + 1)
    pstats = pstats[["Rank", "Passer", "Team", "Average EPA", "Attempts"]]
    fancynames = []
    for p in pstats["Passer"]:
        fancynames.append(re.sub("_", " ", p))
    pstats["Passer"] = fancynames
    pstats.to_csv("passing_" + str(s) + ".csv", index = False)
    
    
    
    ## All passes to WRs
    wrdat = dat.loc[dat["pass"] == True]
    wrdat = wrdat.loc[wrdat["receiver"] == wrdat["receiver"]]
    wrdat = wrdat.loc[wrdat["Possession"] == wrdat["Possession"]]
    receivers = numpy.unique(wrdat["receiver"])
    rstats = []
    for r in receivers:
        tmpdat = wrdat.loc[dat["receiver"] == r]
        mv = numpy.mean(tmpdat["EPAchange"]) 
        mv2 = format(mv, ".3f")
        rstats.append([r, numpy.unique(tmpdat.Possession)[0], mv, mv2, len(tmpdat)])
        
    wrstats = pandas.DataFrame(rstats[1:])
    wrstats.columns = ["Intended Target", "Team", "sortme", "Average EPA", "Targets"]
    wrstats = wrstats.sort_values("sortme", ascending = False)
    wrstats = wrstats.loc[wrstats["Targets"] > 4 * weeks]
    wrstats["Rank"] = range(1, len(wrstats) + 1)
    wrstats = wrstats[["Rank", "Intended Target", "Team", "Average EPA", "Targets"]]
    wrstats = wrstats[0:30]
    fancynames = []
    for p in wrstats["Intended Target"]:
        fancynames.append(re.sub("_", " ", p))
    wrstats["Intended Target"] = fancynames
    wrstats.to_csv("targets_" + str(s) + ".csv", index = False)
    
    
    ## Running backs
    rdat = dat.loc[dat["run"] == True]
    rdat = rdat.loc[rdat["rusher"] == rdat["rusher"]]
    rdat = rdat.loc[rdat["Possession"] == rdat["Possession"]]
    runners = numpy.unique(rdat["rusher"])
    
    rstats = []
    for r in runners:
        tmpdat = rdat.loc[rdat["rusher"] == r]
        mv = numpy.mean(tmpdat["EPAchange"]) 
        mv2 = format(mv, ".3f")
        rstats.append([r, numpy.unique(tmpdat.Possession)[0], mv, mv2, len(tmpdat)])
    
    rstats = pandas.DataFrame(rstats)
    rstats.columns = ["Rusher", "Team", "sortme", "Average EPA", "Attempts"]
    rstats = rstats.sort_values("sortme", ascending = False)
    rstats = rstats.loc[rstats["Attempts"] > 10 * weeks]
    rstats["Rank"] = range(1, len(rstats) + 1)
    rstats = rstats[["Rank", "Rusher", "Team", "Average EPA", "Attempts"]]
    rstats = rstats[0:30]
    fancynames = []
    for p in rstats["Rusher"]:
        fancynames.append(re.sub("_", " ", p))
    rstats["Rusher"] = fancynames
    rstats.to_csv("rushing_" + str(s) + ".csv", index = False)
    
    
    def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
                         header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                         bbox=[0, 0, 1, 1], header_columns=0,
                         ax=None, **kwargs):
        if ax is None:
            size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
            fig, ax = plt.subplots(figsize=size)
            ax.axis('off')
    
        mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)
    
        mpl_table.auto_set_font_size(False)
        mpl_table.set_fontsize(font_size)
    
        for k, cell in six.iteritems(mpl_table._cells):
            cell.set_edgecolor(edge_color)
            if k[0] == 0 or k[1] < header_columns:
                cell.set_text_props(weight='bold', color='w')
                cell.set_facecolor(header_color)
            else:
                cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
        return ax
    
    tab = render_mpl_table(pstats, header_columns=0, col_width=3.2)
    savefig("passers_" + str(s) + ".png", bbox_inches= 'tight')
    
    tab = render_mpl_table(wrstats, header_columns=0, col_width=3.2)
    savefig("targets_" + str(s) + ".png", bbox_inches= 'tight')
    
    tab = render_mpl_table(rstats, header_columns=0, col_width=3.2)
    savefig("runners_" + str(s) + ".png", bbox_inches= 'tight')

seasons = [2017]

for s in seasons:
    ranker(s)
        
