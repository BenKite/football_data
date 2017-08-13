## Ben Kite

import profootballReferenceScrape as pf
import pandas, numpy, re
import numpy as np, numpy
from pylab import *
from matplotlib.backends.backend_pdf import PdfPages
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss
from sklearn.ensemble import RandomForestClassifier

## Scrape the data from the past 6 seasons, 
## but read the files if they already exists
seasons = [2011, 2012, 2013, 2014, 2015, 2016]
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

## Remove missing values and play types I do not want
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

dat.reset_index(drop = True, inplace = True)

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
    
preds = ["Int", "secondDown", "thirdDown", "forthDown", "ToGo", "distFromGoal",
         "TimeRemaining", "twoMinute", "interaction"]

## Make train and testing sets
train = dat.loc[dat["Season"] != 2016]
test = dat.loc[dat["Season"] == 2016]

## Build a basic logistic regression model for predicting who scores next
## Still need to tune the model with cross validations.
dv = "nextPoints"
clf = LogisticRegression(fit_intercept = False)
clf.fit(train[preds], train[dv])
predictions = clf.predict_proba(test[preds])
test["PnextPoints"] = predictions[:,1]

## Log-loss
log_loss(test["nextPoints"], test["PnextPoints"])

## Easier to use function that takes fewer arugments to do the prediction
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


