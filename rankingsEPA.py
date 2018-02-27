## Ben Kite

weeks = 16

from playByPlay import pullPlaybyPlay, preparePlaybyPlay 
from profootballReferenceScrape import findTables, pullTable
import pandas, numpy, re
import os
import numpy as np
from pylab import *

## Get current team info

passingid = findTables("https://www.pro-football-reference.com/years/2017/passing.htm")
passersDat = pullTable("https://www.pro-football-reference.com/years/2017/passing.htm", passingid)
passersDat = pandas.DataFrame(passersDat.iloc[:,[1, 2]])
passersDat.columns = ["Passer", "Team"]

replacement = []

for i in range(0, len(passersDat["Passer"])):
    p = passersDat.loc[i]["Passer"]
    xx = re.sub("[#@*&^%$!+]", "", p)
    replacement.append(xx)

passersDat["Passer"] = replacement                


skillid = findTables("https://www.pro-football-reference.com/years/2017/receiving.htm")
skillDat = pullTable("https://www.pro-football-reference.com/years/2017/receiving.htm", skillid[0])
skillDat = pandas.DataFrame(skillDat.iloc[:,[1, 2]])
skillDat.columns = [["Intended Target", "Team"]]

replacement2 = []

for i in range(0, len(skillDat["Intended Target"])):
    p = skillDat.loc[i]["Intended Target"]
    xx = re.sub("[#@*&^%$!+]", "", p)
    replacement2.append(xx)

skillDat["Intended Target"] = replacement2 


skillid2 = findTables("https://www.pro-football-reference.com/years/2017/rushing.htm")
skillDat2 = pullTable("https://www.pro-football-reference.com/years/2017/rushing.htm", skillid2[0], header = False)
skillDat2 = pandas.DataFrame(skillDat2.iloc[:,[1, 2]])
skillDat2.columns = [["Rusher", "Team"]]

replacement3 = []

for i in range(0, len(skillDat2["Rusher"])):
    p = skillDat2.loc[i]["Rusher"]
    xx = re.sub("[#@*&^%$!+]", "", p)
    replacement3.append(xx)

skillDat2["Rusher"] = replacement3 


def ranker(s):
    rawfile = "raw_" + str(s) + ".csv"
    processedfile = "play_by_play_" + str(s) + ".csv"
    if os.path.isfile(rawfile):
        tmpdat = pandas.read_csv(rawfile)
    else:
        tmpdat = pullPlaybyPlay(s)
        tmpdat.to_csv(rawfile)
        
    #if os.path.isfile(processedfile):
    #    dat = pandas.read_csv(processedfile)
    #else:
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
        pstats.append([p, mv, mv2, len(tmpdat)])
        
    pstats = pandas.DataFrame(pstats)
    pstats.columns = ["Passer", "sortme", "Average EPA", "Attempts"]
    pstats = pstats.sort_values("sortme", ascending = False)
    pstats = pstats.loc[pstats["Attempts"] > 20 * weeks]
    pstats["Rank"] = range(1, len(pstats) + 1)
    mean = pstats["sortme"].mean()
    sd = pstats["sortme"].std()
    z = (pstats["sortme"] - mean) /sd
    pstats["Z-score"] = numpy.round(z, 3)
    pstats = pstats[["Rank", "Passer", "Average EPA", "Z-score", "Attempts"]]
    fancynames = []
    for p in pstats["Passer"]:
        fancynames.append(re.sub("_", " ", p))
    pstats["Passer"] = fancynames
    pstats = pandas.merge(pstats, passersDat, 'left', on = "Passer")
    pstats = pstats[["Rank", "Passer", "Team", "Average EPA", "Z-score", "Attempts"]]
    pstats.columns = ["Rank", "Passer", "Team", "Average EPA", "Z-score", "Attempts (min = " + str(20 * weeks) + ")"]
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
        rstats.append([r, mv, mv2, len(tmpdat)])
        
    wrstats = pandas.DataFrame(rstats[1:])
    wrstats.columns = ["Intended Target", "sortme", "Average EPA", "Targets"]
    wrstats = wrstats.sort_values("sortme", ascending = False)
    wrstats = wrstats.loc[wrstats["Targets"] > 4 * weeks]
    wrstats["Rank"] = range(1, len(wrstats) + 1)
    wrstats = wrstats[["Rank", "Intended Target", "Average EPA", "Targets"]]
    wrstats = wrstats[0:30]
    fancynames = []
    for p in wrstats["Intended Target"]:
        fancynames.append(re.sub("_", " ", p))
    wrstats["Intended Target"] = fancynames
    wrstats = pandas.merge(wrstats, skillDat, 'left', on = "Intended Target")
    wrstats = wrstats[["Rank", "Intended Target", "Team", "Average EPA", "Targets"]]
    wrstats.columns = [["Rank", "Intended Target", "Team", "Average EPA", "Targets (min = " + str(4 * weeks) + ")"]]
    wrstats = wrstats.drop_duplicates(subset=["Intended Target"], keep="first")
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
        rstats.append([r, mv, mv2, len(tmpdat)])
    
    rstats = pandas.DataFrame(rstats)
    rstats.columns = ["Rusher", "sortme", "Average EPA", "Attempts"]
    rstats = rstats.sort_values("sortme", ascending = False)
    rstats = rstats.loc[rstats["Attempts"] > 10 * weeks]
    rstats["Rank"] = range(1, len(rstats) + 1)
    rstats = rstats[["Rank", "Rusher", "Average EPA", "Attempts"]]
    rstats = rstats[0:30]
    fancynames = []
    for p in rstats["Rusher"]:
        fancynames.append(re.sub("_", " ", p))
    rstats["Rusher"] = fancynames
    rstats = pandas.merge(rstats, skillDat2, 'left', on = "Rusher")
    rstats = rstats[["Rank", "Rusher", "Team", "Average EPA", "Attempts"]]
    rstats.columns = [["Rank", "Rusher", "Team", "Average EPA", "Attempts (min = " + str(10 * weeks) + ")"]]
    rstats = rstats.drop_duplicates(subset=["Rusher"], keep="first")
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
        
