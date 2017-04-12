## Ben Kite

import profootballReferenceScrape as pf
import pandas, numpy, re
import numpy as np, numpy
from pylab import *
from matplotlib.backends.backend_pdf import PdfPages
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression

seasons = [2012, 2013, 2014, 2015, 2016]
datdict = dict()
for s in seasons:
    rawfile = "raw_" + str(s) + ".csv"
    processedfile = "play_by_play_" + str(s) + ".csv"
    if os.path.isfile(rawfile):
        if os.path.isfile(processedfile):
            None
        else:
            tmpdat = pandas.read_csv(rawfile)
    else:
        tmpdat = pullPlaybyPlay(s)
        
    if os.path.isfile(processedfile):
        datdict[s] = pandas.read_csv(processedfile)
    else:
        datdict[s] = preparePlaybyPlay(tmpdat)
        
dat = pandas.concat(datdict)

dat = dat.loc[dat["Down"] == dat["Down"]]
dat = dat.loc[dat["Possession"] == dat["Possession"]]
dat = dat.loc[dat["distFromGoal"] == dat["distFromGoal"]]
dat = dat.loc[dat["TimeRemaining"] == dat["TimeRemaining"]]
dat = dat.loc[dat["knee"] == False]
dat = dat.loc[dat["xp"] == False]
dat = dat.loc[dat["kickoff"] == False]
#dat = dat.loc[dat["punt"] == False]
#dat = dat.loc[(dat["Quarter"] == "1") | (dat["Quarter"] == "3")]
dat = dat.loc[dat["distFromGoal"] > 0]

dat = dat.reset_index(drop = True)

dat["Int"] = 1

def trfuc(tmp):
    t = tmp["TimeRemaining"]
    if t <= 2:
        return(1)
    else: 
        return(0)
        
dat["twoMinute"] = dat.apply(trfuc, 1)

dat["interaction"] = dat["TimeRemaining"] * dat["twoMinute"]
dat["secondDown"] = numpy.where(dat["Down"] == 2, 1, 0)
dat["thirdDown"] = numpy.where(dat["Down"] == 3, 1, 0)
dat["forthDown"] = numpy.where(dat["Down"] == 4, 1, 0)

for i in range(0, len(dat)):
    tmp = dat.loc[i]
    
preds = ["Int", "secondDown", "thirdDown", "forthDown", "ToGo", "distFromGoal", "TimeRemaining", "twoMinute", "interaction"]


## Next TD
dv = "nextTD"
clf = LogisticRegression(fit_intercept = False)
clf.fit(dat[preds], dat[dv])
clf.coef_
predictions = clf.predict_proba(dat[preds])
dat["PnextTD"] = predictions[:,1]
def predictor(down, distance, fromGoal, time):
    if time <= 2:
        twomin = 1
    else:
        twomin = 0
    twomin 
    interact = twomin*time
    second = numpy.where(down == 2, 1, 0)
    third = numpy.where(down == 3, 1, 0)
    forth = numpy.where(down == 4, 1, 0)
    x = clf.predict_proba([1, second, third, forth, distance, fromGoal, time, twomin, interact])
    return(x)
    
predictor(2, 10, 60, 4)
time = [0, 1, 2, 3, 4, 5, 6, 7, 8]
vv = []
for t in time:
    val1 = predictor(1, 10, 75, t)[:,1][0]
    val2 = predictor(2, 10, 75, t)[:,1][0]
    val3 = predictor(3, 10, 75, t)[:,1][0]
    val4 = predictor(4, 10, 75, t)[:,1][0]
    vv.append([t, val1, val2, val3, val4])
vv = pandas.DataFrame(vv)
vv.columns = ["Minutes Remaining", "First", "Second", "Third", "Forth"]
vv = vv.sort("Minutes Remaining", ascending = False)
plt.figure()
line1, = plt.plot(vv["Minutes Remaining"], vv["First"], color = 'b', label = "First Down")
line2, = plt.plot(vv["Minutes Remaining"], vv["Second"], color = 'purple', label = "Second Down")
line3, = plt.plot(vv["Minutes Remaining"], vv["Third"], color = 'r', label = "Third Down")
line4, = plt.plot(vv["Minutes Remaining"], vv["Forth"], color = 'black', label = "Forth Down")
plt.title("Probability of Possessor Scoring TD Next")        
plt.ylim(0, 1)        
plt.xlim(8, 0)        
plt.xlabel("Time Remaining in Minutes")        
plt.ylabel("Probability Next Score is a Possessor TD")
plt.legend(handles = [line1, line2, line3, line4], loc = 1)
plt.savefig('nextTD.png')


## Next Points
dv = "nextPoints"
clf = LogisticRegression(fit_intercept = False)
clf.fit(dat[preds], dat[dv])
clf.coef_
predictions = clf.predict_proba(dat[preds])
dat["PnextPoints"] = predictions[:,1]
def predictor(down, distance, fromGoal, time):
    if time <= 2:
        twomin = 1
    else:
        twomin = 0
    twomin 
    interact = twomin*time
    second = numpy.where(down == 2, 1, 0)
    third = numpy.where(down == 3, 1, 0)
    forth = numpy.where(down == 4, 1, 0)
    x = clf.predict_proba([1, second, third, forth, distance, fromGoal, time, twomin, interact])
    return(x)
predictor(2, 10, 60, 4)
time = [0.1, 1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1]
vv = []
for t in time:
    val1 = predictor(1, 10, 75, t)[:,1][0]
    val2 = predictor(2, 10, 75, t)[:,1][0]
    val3 = predictor(3, 10, 75, t)[:,1][0]
    val4 = predictor(4, 10, 75, t)[:,1][0]
    vv.append([t, val1, val2, val3, val4])
vv = pandas.DataFrame(vv)
vv.columns = ["Minutes Remaining", "First", "Second", "Third", "Forth"]
vv = vv.sort("Minutes Remaining", ascending = False)
plt.figure()
line1, = plt.plot(vv["Minutes Remaining"], vv["First"], color = 'b', label = "First Down")
line2, = plt.plot(vv["Minutes Remaining"], vv["Second"], color = 'purple', label = "Second Down")
line3, = plt.plot(vv["Minutes Remaining"], vv["Third"], color = 'r', label = "Third Down")
line4, = plt.plot(vv["Minutes Remaining"], vv["Forth"], color = 'black', label = "Forth Down")
plt.title("Probability of Possessor Scoring Next")        
plt.ylim(0, 1)        
plt.xlim(8, 0)        
plt.xlabel("Time Remaining in Minutes")        
plt.ylabel("Probability Next Score is a Possessor TD")
plt.legend(handles = [line1, line2, line3, line4], loc = 1)
plt.savefig('nextPoints.png')

