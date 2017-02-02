## Ben Kite
## 2017-02-02

import pandas, numpy
import requests, bs4
import re

def SeasonFinder (stat, year):
    url = "http://www.pro-football-reference.com/years/" + str(year) + "/" + stat + ".htm"
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text)
    if stat == "rushing":
        stat = "rushing_and_receiving"
    tables = soup.findAll('table', id = stat)
    data_rows = tables[0].findAll('tr')  
    game_data = [[td.getText() for td in data_rows[i].findAll('td')]
        for i in range(len(data_rows))
        ]
    dat = pandas.DataFrame(game_data)
    dat = dat[dat[0].notnull()]
    try:
        header = [[th.getText() for th in data_rows[0].findAll('th')]]
        header = header[0][1:len(header[0])]
        dat.columns = header
    except ValueError:
        pass
    dat = dat.reset_index(drop = True)
    names = dat.columns
    for c in range(0, len(names)):
        replacement = []
        if type (dat.loc[0][c]) == str:
            k = names[c]
            for i in range(0, len(dat[k])):
                p = dat.loc[i][c]
                xx = re.sub("[#@*&^%$!+]", "", p)
                xx = xx.replace("\xa0", "_")
                xx = xx.replace(" ", "_")
                replacement.append(xx)
            dat[k] = replacement
    dat.to_csv("../data/" + str(stat) + "_" + str(year) + ".csv")
    return(dat)


## example of use
tables = ["passing", "rushing", "receiving"]
years = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
         2009, 2010, 2011, 2012, 2013, 2014, 2015]
for y in years:
    for t in tables:
        SeasonFinder(t, y)
    
    

def GameFinder (date, homeTeam):
    url = "http://www.pro-football-reference.com/boxscores/" +  str(date) + homeTeam + ".htm#all_player_offense"
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text)
    tables = soup.findAll('div', id = "all_player_offense")
    data_rows = tables[0].findAll('tr')  
    game_data = [[td.getText() for td in data_rows[i].findAll('td')]
        for i in range(len(data_rows))
        ]
    dat = pandas.DataFrame(game_data)
    dat = dat[dat[0].notnull()]
    try:
        header = [[th.getText() for th in data_rows[0].findAll('th')]]
        header = header[0][1:len(header[0])]
        dat.columns = header
    except ValueError:
        pass
    dat = dat.reset_index(drop = True)
    names = dat.columns
    return(dat)

    
