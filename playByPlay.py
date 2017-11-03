## Ben Kite

import profootballReferenceScrape as pf
import pandas, numpy, re, os
import datetime

## This is the only external function in the script.
## The season argument indicates the season for which data are desired.
## This is still in development, but it does work for the 2016 season.
## Run the script all the way through the end to get all play-by-play data for the 2016 season.
## I should also mention that the variable which indicates the location of the ball 
## relative to the endzone of the defense is showing some errors.
## I am working to improve the location identification process.

def pullPlaybyPlay(season):
    url = "http://www.pro-football-reference.com/years/" + str(season) + "/games.htm"
    sched = pf.pullTable(url, "games")
    today = datetime.date.today()
    today2 = str(today.year) + str(today.month).zfill(2)+ str(today.day).zfill(2) + "0"
    today2n = int(today2)
    if season == 2017:
        teamnames = {"crd":'Arizona Cardinals',
                     "atl":'Atlanta Falcons',
                     "rav":'Baltimore Ravens',
                     "buf":'Buffalo Bills',
                     "car":'Carolina Panthers', 
                     "chi":'Chicago Bears',
                     "cin":'Cincinnati Bengals', 
                     "cle":'Cleveland Browns', 
                     "dal":'Dallas Cowboys',
                     "den":'Denver Broncos', 
                     "det":'Detroit Lions', 
                     "gnb":'Green Bay Packers',
                     "htx":'Houston Texans', 
                     "clt":'Indianapolis Colts', 
                     "jax":'Jacksonville Jaguars',
                     "kan":'Kansas City Chiefs', 
                     "ram":'Los Angeles Rams',
                     "mia":'Miami Dolphins',
                     "min":'Minnesota Vikings', 
                     "nwe":'New England Patriots', 
                     "nor":'New Orleans Saints',
                     "nyg":'New York Giants', 
                     "nyj":'New York Jets', 
                     "rai":'Oakland Raiders',
                     "phi":'Philadelphia Eagles', 
                     "pit":'Pittsburgh Steelers', 
                     "sdg":'Los Angeles Chargers',
                     "sfo":'San Francisco 49ers', 
                     "sea":'Seattle Seahawks', 
                     "tam":'Tampa Bay Buccaneers',
                     "oti":'Tennessee Titans', 
                     "was":'Washington Redskins'}   
    if season in [2015, 2016]:
        teamnames = {"crd":'Arizona Cardinals',
                     "atl":'Atlanta Falcons',
                     "rav":'Baltimore Ravens',
                     "buf":'Buffalo Bills',
                     "car":'Carolina Panthers', 
                     "chi":'Chicago Bears',
                     "cin":'Cincinnati Bengals', 
                     "cle":'Cleveland Browns', 
                     "dal":'Dallas Cowboys',
                     "den":'Denver Broncos', 
                     "det":'Detroit Lions', 
                     "gnb":'Green Bay Packers',
                     "htx":'Houston Texans', 
                     "clt":'Indianapolis Colts', 
                     "jax":'Jacksonville Jaguars',
                     "kan":'Kansas City Chiefs', 
                     "ram":'Los Angeles Rams',
                     "mia":'Miami Dolphins',
                     "min":'Minnesota Vikings', 
                     "nwe":'New England Patriots', 
                     "nor":'New Orleans Saints',
                     "nyg":'New York Giants', 
                     "nyj":'New York Jets', 
                     "rai":'Oakland Raiders',
                     "phi":'Philadelphia Eagles', 
                     "pit":'Pittsburgh Steelers', 
                     "sdg":'San Diego Chargers',
                     "sfo":'San Francisco 49ers', 
                     "sea":'Seattle Seahawks', 
                     "tam":'Tampa Bay Buccaneers',
                     "oti":'Tennessee Titans', 
                     "was":'Washington Redskins'}    
    if season < 2015:
        teamnames = {"crd":'Arizona Cardinals',
                     "atl":'Atlanta Falcons',
                     "rav":'Baltimore Ravens',
                     "buf":'Buffalo Bills',
                     "car":'Carolina Panthers', 
                     "chi":'Chicago Bears',
                     "cin":'Cincinnati Bengals', 
                     "cle":'Cleveland Browns', 
                     "dal":'Dallas Cowboys',
                     "den":'Denver Broncos', 
                     "det":'Detroit Lions', 
                     "gnb":'Green Bay Packers',
                     "htx":'Houston Texans', 
                     "clt":'Indianapolis Colts', 
                     "jax":'Jacksonville Jaguars',
                     "kan":'Kansas City Chiefs', 
                     "ram":'St. Louis Rams',
                     "mia":'Miami Dolphins',
                     "min":'Minnesota Vikings', 
                     "nwe":'New England Patriots', 
                     "nor":'New Orleans Saints',
                     "nyg":'New York Giants', 
                     "nyj":'New York Jets', 
                     "rai":'Oakland Raiders',
                     "phi":'Philadelphia Eagles', 
                     "pit":'Pittsburgh Steelers', 
                     "sdg":'San Diego Chargers',
                     "sfo":'San Francisco 49ers', 
                     "sea":'Seattle Seahawks', 
                     "tam":'Tampa Bay Buccaneers',
                     "oti":'Tennessee Titans', 
                     "was":'Washington Redskins'}                 
    teamnames2 = dict()
    for t in teamnames:
        x = teamnames[t]
        teamnames2[x] = t
    sched = sched.loc[sched["Date"] != "Playoffs"]
    sched = sched.loc[:255]
    sched.reset_index(drop = True, inplace = True)
    dates = sched["Date"]
    ndates = []
    sdates = []
    for d in dates:
        month = d.split(" ")[0]
        day = d.split(" ")[1]
        day = day.zfill(2)
        mapping = {"September": "09", "October": "10", "November": "11", "December": "12", "January": "1", "February": "2"}    
        m = mapping[month]
        m = m.zfill(2)
        if (m == "01") | (m == "02"):
            year = season + 1
        else:
            year = season
        ndates.append(int(str(year) + m + day + "0"))
        sdates.append(str(year) + m + day + "0")
    ndates
    sched["Date2"] = sdates
    sched["Date2n"] = ndates
    pbpdat = dict()
    
    sched = sched.loc[sched.Date2n < today2n]
    for i in range(0 , len(sched)):
        tmp = sched.loc[i]
        date = tmp["Date2"]
        loc = tmp[5]
        if loc == "N":
            ht = "NA"
        else:
            if loc == "@":
                ht = tmp["Loser/tie"]
                at = tmp["Winner/tie"]
            else:
                ht = tmp["Winner/tie"]
                at = tmp["Loser/tie"]
        ht = teamnames2[ht]
        tmpdat = pf.playByPlay(date, ht)
        tmpdat = tmpdat[1:]
        tmpdat = tmpdat.loc[tmpdat["Time"] == tmpdat["Time"]]
        tmpdat = tmpdat.reset_index()
        ht = tmpdat.columns[8]
        at = tmpdat.columns[7]
        tmpdat["awaypoints"] = tmpdat[at]
        tmpdat["homepoints"] = tmpdat[ht]
        firsth = tmpdat.loc[(tmpdat["Quarter"] == '1') | (tmpdat["Quarter"] == '2')]
        firsth = firsth.reset_index(drop = True)
        scores = firsth[["Quarter", at, ht]]
        scores["diff"] = pandas.to_numeric(scores[ht]) - pandas.to_numeric(scores[at])
        holder = []
        holder.append(0)
        for s in range(1, len(scores["diff"])):
            pre = scores["diff"][s - 1]
            post = scores["diff"][s]
            holder.append(post - pre)
        xx = []
        for h in holder:
            xx.append(h)
        tmp = []
        for x in range(0, len(xx)):
            score = xx[x]
            tmp.append(x)
            if numpy.abs(score) > 0:
                for j in tmp:
                    holder[j] = score
                tmp = []
        firsth["nextpoints"] = list(holder)
        
        secondh = tmpdat.loc[(tmpdat["Quarter"] == '3') | (tmpdat["Quarter"] == '4')]
        secondh = secondh.reset_index(drop = True)
        scores = secondh[["Quarter", at, ht]]
        scores["diff"] = pandas.to_numeric(scores[ht]) - pandas.to_numeric(scores[at])
        holder = []
        holder.append(0)
        for s in range(1, len(scores["diff"])):
            pre = scores["diff"][s - 1]
            post = scores["diff"][s]
            holder.append(post - pre)
        xx = []
        for h in holder:
            xx.append(h)
        tmp = []
        for x in range(0, len(xx)):
            score = xx[x]
            tmp.append(x)
            if numpy.abs(score) > 0:
                for j in tmp:
                    holder[j] = score
                tmp = []
        secondh["nextpoints"] = list(holder)
        tmpdat = pandas.concat([firsth, secondh])  
        tmpdat = tmpdat.reset_index(drop = True)
        tmpdat["hometeam"] = ht.upper()
        tmpdat["awayteam"] = at.upper()
        tmpdat["EPA"] = pandas.to_numeric(tmpdat["EPA"])
        tmpdat["EPB"] = pandas.to_numeric(tmpdat["EPB"])    
        change = []
        change.append(False)
        for ch in range(1, len(tmpdat["EPB"])):
            change.append(tmpdat["EPB"][ch] == tmpdat["EPA"][ch - 1] * -1)
        tmpdat["ChangeOfPoss"] = change    
        tmpdat["Date"] = date
        pbpdat[i] = tmpdat
    dat = pandas.concat(pbpdat) 
    dat = dat[["Date", "awayteam", "hometeam", "awaypoints", "homepoints", "Detail", "Down", "ToGo", "Location", "Quarter", "Time", "nextpoints", "EPB", "EPA"]]
    dat["Season"] = season    
    dat = dat.loc[dat["Quarter"] != "End of Overtime"]
    dat = dat.reset_index(drop = True)
    return(dat)   
        
def preparePlaybyPlay(dat):
    season = dat["Season"][0]    
    dat["challenge"] = dat["Detail"].str.contains("challenged")
    dat["spike"] = dat["Detail"].str.contains("spiked")
    dat["knee"] = dat["Detail"].str.contains("kneel")
    dat["penalty"] = dat["Detail"].str.contains("Penalty")
    dat["timeout"] = dat["Detail"].str.contains("TIMEOUT")
    def penFunc(tmp): 
        if tmp["penalty"]:
            deets = tmp["Detail"].split(" ")
            if ("Penalty" in deets) & ("on" in deets):
                for d in range(0, len(deets)):
                    word = deets[d]
                    if word == "on":
                        start = d
                        break
                x = deets[start + 1] + "_" + deets[start + 2]
                x = re.sub("[.,:]", "", x)
                return(x)
            else:
                return("")
        else:
            return("") 
    dat["penaltyon"] = dat.apply(penFunc, axis = 1)   
    dat["pass"] = ((dat["Detail"].str.contains("pass")) | (dat["Detail"].str.contains("sacked"))) & (dat["challenge"] == False)
    dat["sacked"] = dat["Detail"].str.contains("sacked")
    def passerFunc(tmp):
        if tmp["pass"]:
            return(tmp["Detail"].split(" ")[0] + "_" + tmp["Detail"].split(" ")[1])
        else:
            return("")
    dat["passer"] = dat.apply(passerFunc, axis = 1)
    def recFunc(tmp, caught = False):
        if tmp["pass"]:
            deets = tmp["Detail"].split(" ")
            if ("complete" in deets) & ("to" in deets):
                for d in range(0, len(deets)):
                    word = deets[d]
                    if word == "to":
                        start = d
                        break
                x = deets[start + 1] + "_" + deets[start + 2]
                x = re.sub("[.,]", "", x)
                if caught:
                    return(True)
                else:
                    return(x)
            else:
                if ("intended" in deets) & ("for" in deets):
                    for d in range(0, len(deets)):
                        word = deets[d]
                        if word == "for":
                            start = d
                            break
                    if deets[start + 1] == "":
                        return("")
                    else:
                        x = deets[start + 1] + "_" + deets[start + 2]
                        x = re.sub("[.,]", "", x)
                    if caught:
                        return(False)    
                    else:
                        return(x)
                else:
                    if caught:
                        return(False)
                    else:
                        return("")
        else:
            return("")    
    dat["receiver"] = dat.apply(recFunc, axis = 1)
    dat["caught"] = dat.apply(recFunc, axis = 1, caught = True)
    dat["punt"] = dat["Detail"].str.contains("punt") & (dat["challenge"] == False)
    def puntFunc(tmp):
        if tmp["punt"]:
            return(tmp["Detail"].split(" ")[0] + "_" + tmp["Detail"].split(" ")[1])
        else:
            return("")
    dat["punter"] = dat.apply(puntFunc, 1)
    dat["kickoff"] = dat["Detail"].str.contains("kicks off")
    dat["FG"] = dat["Detail"].str.contains("field goal")
    dat["xp"] = dat["Detail"].str.contains("extra point")
    dat["kick"] = (dat["kickoff"] == True) | (dat["FG"] == True) | (dat["xp"] == True)
    def kickFunc(tmp):
        if (tmp["kick"]):
            return(tmp["Detail"].split(" ")[0] + "_" + tmp["Detail"].split(" ")[1])
        else:
            return("")
    dat["kicker"] = dat.apply(kickFunc, 1)
    dat["to"] = dat["Detail"].str.contains("Timeout")
    dat["nodetail"] = dat["Detail"] == ""
    dat["run"] = (dat["penalty"] == False) & (dat["challenge"] == False) & (dat["spike"] == False) & (dat["pass"] == False) & (dat["punt"] == False) & (dat["kickoff"] == False) & (dat["FG"] == False) & (dat["xp"] == False) & (dat["to"] == False) & (dat["nodetail"] == False) & (dat["timeout"] == False)
    def rushFunc(tmp):
        if tmp["run"]:
            return(tmp["Detail"].split(" ")[0] + "_" + tmp["Detail"].split(" ")[1])
        else:
            return("")
    dat["rusher"] = dat.apply(rushFunc, 1)
    dat["EPA"] = pandas.to_numeric(dat["EPA"])
    dat["EPB"] = pandas.to_numeric(dat["EPB"])
    dat["EPAchange"] = dat["EPA"] - dat["EPB"]
    dat["Possession"] = "NA"
    ## Need list of passers, targets, rushers, punters, and kickers from each team.
    if season > 2016:
        teamnames = {"crd":'Arizona Cardinals',
                     "atl":'Atlanta Falcons',
                     "rav":'Baltimore Ravens',
                     "buf":'Buffalo Bills',
                     "car":'Carolina Panthers', 
                     "chi":'Chicago Bears',
                     "cin":'Cincinnati Bengals', 
                     "cle":'Cleveland Browns', 
                     "dal":'Dallas Cowboys',
                     "den":'Denver Broncos', 
                     "det":'Detroit Lions', 
                     "gnb":'Green Bay Packers',
                     "htx":'Houston Texans', 
                     "clt":'Indianapolis Colts', 
                     "jax":'Jacksonville Jaguars',
                     "kan":'Kansas City Chiefs', 
                     "ram":'Los Angeles Rams',
                     "mia":'Miami Dolphins',
                     "min":'Minnesota Vikings', 
                     "nwe":'New England Patriots', 
                     "nor":'New Orleans Saints',
                     "nyg":'New York Giants', 
                     "nyj":'New York Jets', 
                     "rai":'Oakland Raiders',
                     "phi":'Philadelphia Eagles', 
                     "pit":'Pittsburgh Steelers', 
                     "lac":'Los Angeles Chargers',
                     "sfo":'San Francisco 49ers', 
                     "sea":'Seattle Seahawks', 
                     "tam":'Tampa Bay Buccaneers',
                     "oti":'Tennessee Titans', 
                     "was":'Washington Redskins'}    
        teamabs= {"crd":'ARI',
                  "atl":'ATL',
                  "rav":'BAL',
                  "buf":'BUF',
                  "car":'CAR', 
                  "chi":'CHI',
                  "cin":'CIN', 
                  "cle":'CLE', 
                  "dal":'DAL',
                  "den":'DEN', 
                  "det":'DET', 
                  "gnb":'GNB',
                  "htx":'HOU', 
                  "clt":'IND', 
                  "jax":'JAX',
                  "kan":'KAN', 
                  "ram":'LAR', 
                  "mia":'MIA',
                  "min":'MIN', 
                  "nwe":'NWE', 
                  "nor":'NOR',
                  "nyg":'NYG', 
                  "nyj":'NYJ', 
                  "rai":'OAK',
                  "phi":'PHI', 
                  "pit":'PIT', 
                  "lac":'LAC',
                  "sfo":'SFO', 
                  "sea":'SEA', 
                  "tam":'TAM',
                  "oti":'TEN', 
                  "was":'WAS'} 
    
    if season == 2016:
        teamnames = {"crd":'Arizona Cardinals',
                     "atl":'Atlanta Falcons',
                     "rav":'Baltimore Ravens',
                     "buf":'Buffalo Bills',
                     "car":'Carolina Panthers', 
                     "chi":'Chicago Bears',
                     "cin":'Cincinnati Bengals', 
                     "cle":'Cleveland Browns', 
                     "dal":'Dallas Cowboys',
                     "den":'Denver Broncos', 
                     "det":'Detroit Lions', 
                     "gnb":'Green Bay Packers',
                     "htx":'Houston Texans', 
                     "clt":'Indianapolis Colts', 
                     "jax":'Jacksonville Jaguars',
                     "kan":'Kansas City Chiefs', 
                     "ram":'Los Angeles Rams',
                     "mia":'Miami Dolphins',
                     "min":'Minnesota Vikings', 
                     "nwe":'New England Patriots', 
                     "nor":'New Orleans Saints',
                     "nyg":'New York Giants', 
                     "nyj":'New York Jets', 
                     "rai":'Oakland Raiders',
                     "phi":'Philadelphia Eagles', 
                     "pit":'Pittsburgh Steelers', 
                     "sdg":'San Diego Chargers',
                     "sfo":'San Francisco 49ers', 
                     "sea":'Seattle Seahawks', 
                     "tam":'Tampa Bay Buccaneers',
                     "oti":'Tennessee Titans', 
                     "was":'Washington Redskins'}    
        teamabs= {"crd":'ARI',
                  "atl":'ATL',
                  "rav":'BAL',
                  "buf":'BUF',
                  "car":'CAR', 
                  "chi":'CHI',
                  "cin":'CIN', 
                  "cle":'CLE', 
                  "dal":'DAL',
                  "den":'DEN', 
                  "det":'DET', 
                  "gnb":'GNB',
                  "htx":'HOU', 
                  "clt":'IND', 
                  "jax":'JAX',
                  "kan":'KAN', 
                  "ram":'LAR', 
                  "mia":'MIA',
                  "min":'MIN', 
                  "nwe":'NWE', 
                  "nor":'NOR',
                  "nyg":'NYG', 
                  "nyj":'NYJ', 
                  "rai":'OAK',
                  "phi":'PHI', 
                  "pit":'PIT', 
                  "sdg":'SDG',
                  "sfo":'SFO', 
                  "sea":'SEA', 
                  "tam":'TAM',
                  "oti":'TEN', 
                  "was":'WAS'} 
    if season < 2016:
        teamnames = {"crd":'Arizona Cardinals',
                     "atl":'Atlanta Falcons',
                     "rav":'Baltimore Ravens',
                     "buf":'Buffalo Bills',
                     "car":'Carolina Panthers', 
                     "chi":'Chicago Bears',
                     "cin":'Cincinnati Bengals', 
                     "cle":'Cleveland Browns', 
                     "dal":'Dallas Cowboys',
                     "den":'Denver Broncos', 
                     "det":'Detroit Lions', 
                     "gnb":'Green Bay Packers',
                     "htx":'Houston Texans', 
                     "clt":'Indianapolis Colts', 
                     "jax":'Jacksonville Jaguars',
                     "kan":'Kansas City Chiefs', 
                     "ram":'St. Louis Rams',
                     "mia":'Miami Dolphins',
                     "min":'Minnesota Vikings', 
                     "nwe":'New England Patriots', 
                     "nor":'New Orleans Saints',
                     "nyg":'New York Giants', 
                     "nyj":'New York Jets', 
                     "rai":'Oakland Raiders',
                     "phi":'Philadelphia Eagles', 
                     "pit":'Pittsburgh Steelers', 
                     "sdg":'San Diego Chargers',
                     "sfo":'San Francisco 49ers', 
                     "sea":'Seattle Seahawks', 
                     "tam":'Tampa Bay Buccaneers',
                     "oti":'Tennessee Titans', 
                     "was":'Washington Redskins'}  
        teamabs= {"crd":'ARI',
                  "atl":'ATL',
                  "rav":'BAL',
                  "buf":'BUF',
                  "car":'CAR', 
                  "chi":'CHI',
                  "cin":'CIN', 
                  "cle":'CLE', 
                  "dal":'DAL',
                  "den":'DEN', 
                  "det":'DET', 
                  "gnb":'GNB',
                  "htx":'HOU', 
                  "clt":'IND', 
                  "jax":'JAX',
                  "kan":'KAN', 
                  "ram":'STL', 
                  "mia":'MIA',
                  "min":'MIN', 
                  "nwe":'NWE', 
                  "nor":'NOR',
                  "nyg":'NYG', 
                  "nyj":'NYJ', 
                  "rai":'OAK',
                  "phi":'PHI', 
                  "pit":'PIT', 
                  "sdg":'SDG',
                  "sfo":'SFO', 
                  "sea":'SEA', 
                  "tam":'TAM',
                  "oti":'TEN', 
                  "was":'WAS'} 
    teamnames2 = dict()
    for t in teamnames:
        x = teamnames[t]
        teamnames2[x] = t
    
    passingdict = dict()
    carrierdict = dict()
    kickingdict = dict()
    
    for t in teamnames2:
        team = teamnames2[t]
        url = "http://www.pro-football-reference.com/teams/" + team + "/" + str(season) + ".htm"
        try:
            passing = pf.pullTable(url, "passing")
        except IndexError:
            continue
        colnames = passing.columns
        newnames = []
        for c in colnames:
            newnames.append(re.sub("\xa0", "", c))
        passing.columns = newnames
        passing = passing.loc[passing["No."] != ""]    
        passers = []
        for p in passing["Player"]:
            pp = p.split(" ")[0] + "_" + p.split(" ")[1]
            pp = re.sub("[.,*+]", "", pp)
            passers.append(pp)
            
        passingdict[teamabs[team]] = passers
    
        carry = pf.pullTable(url, "rushing_and_receiving", False)
        carry = carry.loc[carry[0] != ""]
        colnames = carry.loc[1]
        newnames = []
        for c in colnames:
            newnames.append(re.sub("\xa0", "", c))
        carry.columns = newnames
        carry = carry.loc[carry["No."] != "No."]
        carriers = []
        for p in carry["Player"]:
            pp = p.split(" ")[0] + "_" + p.split(" ")[1]
            pp = re.sub("[.,*+]", "", pp)
            carriers.append(pp)
            
        carrierdict[teamabs[team]] = carriers
    
        kick = pf.pullTable(url, "kicking", False)
        kick = kick.loc[kick[0] != ""]
        colnames = kick.loc[1]
        newnames = []
        for c in colnames:
            newnames.append(re.sub("\xa0", "", c))
        kick.columns = newnames
        kick = kick.loc[kick["No."] != "No."]
        kickers = []
        for p in kick["Player"]:
            pp = p.split(" ")[0] + "_" + p.split(" ")[1]
            pp = re.sub("[.,*+]", "", pp)
            kickers.append(pp)
            
        kickingdict[teamabs[team]] = kickers
        
        tmpteam = teamabs[team]
    
    teams = []
    for t in teamnames2:
        team = teamnames2[t]
        teams.append(teamabs[team])
        
    ttt = numpy.sort(teams)
    teams = []
    for t in ttt:
        teams.append(t)
    
        
    def inlist(tmp, passingdict, carrierdict, kickingdict, teams):
        penteam = []        
        for t in teams:
            try:
                x = passingdict[t]
            except KeyError:
                continue                 
            if tmp["penaltyon"] in passingdict[t]:
                penteam.append(t)
                
        pen2team = []        
        for t in teams:
            try:
                x = passingdict[t]
            except KeyError:
                continue 
            if tmp["penaltyon"] in carrierdict[t]:
                pen2team.append(t)
        
        pteam = []
        for t in teams:
            try:
                x = passingdict[t]
            except KeyError:
                continue 
            if tmp["passer"] in passingdict[t]:
                pteam.append(t)

        cteam = []
        for t in teams:
            try:
                x = passingdict[t]
            except KeyError:
                continue 
            if tmp["rusher"] in carrierdict[t]:
                cteam.append(t)
        
        rteam = []
        for t in teams:
            try:
                x = passingdict[t]
            except KeyError:
                continue 
            if tmp["receiver"] in carrierdict[t]:
                rteam.append(t)
        
        kteam = []
        for t in teams:
            try:
                x = passingdict[t]
            except KeyError:
                continue 
            if tmp["kicker"] in kickingdict[t]:
                kteam.append(t)
                
        team = numpy.unique(penteam + pen2team + pteam + cteam + rteam + kteam)
        possible = tmp[["hometeam", "awayteam"]] 
        if possible["hometeam"] in team:
            if possible["awayteam"] in team:
                return("NA")
            else:
                return(possible["hometeam"])
        else:
            if possible["awayteam"] in team:
                return(possible["awayteam"])
            else:
                return("NA")

    dat["Possession"] = dat.apply(inlist, 1, args = (passingdict, carrierdict, kickingdict, teams))
        
    
    def distFunc(tmpr):
        if tmpr["Location"] == tmpr["Location"]:
            info = tmpr["Location"].split(" ")
            if len(info) == 1:
                return(-999)
            else:
                if info[1] == '50':
                    return(int(info[1]))
                else:
                    if tmpr["Possession"] == tmpr["Possession"]:
                        poss = tmpr["Possession"]
                        if poss == teamabs[info[0].lower()]:
                            return(100 - int(info[1]))    
                        else:
                            return(int(info[1]))
                    else:
                        return(-999)
        else:
            return(-999)
    
    dat["distFromGoal"] = dat.apply(distFunc, 1)
    
    def timeFunc(tmpr):
        if tmpr["Time"] == tmpr["Time"]:
            if tmpr["Time"] != "":
                info = tmpr["Time"].split(":")
                minutes = int(info[0])
                seconds = int(info[1])
                remaining = minutes + seconds/60
                if tmpr["Quarter"] in ["1", "3", 1, 3]:
                    remaining = remaining + 15
                return(remaining)
            else:
                return(-999)
        else:
            return(-999)
            
    dat["TimeRemaining"] = dat.apply(timeFunc, 1)
    
    dat["homepoints"] = pandas.to_numeric(dat["homepoints"])    
    dat["awaypoints"] = pandas.to_numeric(dat["awaypoints"])    
    
    def differenceFunc(tmpr):
        if tmpr["hometeam"] == tmpr["Possession"]:
            return(tmpr["homepoints"] - tmpr["awaypoints"])
        else:
            return(tmpr["awaypoints"] - tmpr["homepoints"])
            
    dat["pointdiff"] = dat.apply(differenceFunc, 1)
    
    dat["ishome"] = dat["hometeam"] == dat["Possession"]
    ishome = []
    for d in dat["ishome"]:
        if d:
            ishome.append(1)
        else:
            ishome.append(-1)
    dat["ishome"] = ishome
    dat["scorenext"] = dat["nextpoints"] * dat["ishome"]
    
    ntd = []
    for d in dat["scorenext"]:
        if d > 5:
            ntd.append(1)
        else:
            ntd.append(0)
    dat["nextTD"] = ntd
    
    ntp = []
    for d in dat["scorenext"]:
        if d == 3:
            ntp.append(1)
        else:
            ntp.append(0)
    dat["nextFG"] = ntp
    
    ntdt = []
    for d in dat["scorenext"]:
        if d == -3:
            ntdt.append(1)
        else:
            ntdt.append(0)
    dat["allowNextFG"] = ntdt
    
    ntdt = []
    for d in dat["scorenext"]:
        if d < -5:
            ntdt.append(1)
        else:
            ntdt.append(0)
    dat["allowNextTD"] = ntdt
    
    nps= []
    for d in dat["scorenext"]:
        if d > 0:
            nps.append(1)
        else:
            nps.append(0)
    dat["nextPoints"] = nps
    dat.to_csv("play_by_play_" + str(season) + ".csv")
    return(dat)
    
## These simple lines of code put the two functions to work.
## The work is done in two parts incase internet access is lost.
## This checks to see if the files already exist to ensure existing files are not overwritten.

seasons = [2017]
for s in seasons:
    rawfile = "raw_" + str(s) + ".csv"
    processedfile = "play_by_play_" + str(s) + ".csv"
    if os.path.isfile(rawfile):
        tmpdat = pandas.read_csv(rawfile)
    else:
        tmpdat = pullPlaybyPlay(s)
        tmpdat.to_csv(rawfile)
        
    if os.path.isfile(processedfile):
        None
    else:
        tmpdat = preparePlaybyPlay(tmpdat)
        tmpdat.to_csv(processedfile)


