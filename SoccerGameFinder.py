import requests
import urllib.request
import time
from datetime import datetime
import pytz
from bs4 import BeautifulSoup


def getscores(link):
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    url='https://us.soccerway.com'+link
    score=0
    response=requests.get(url, headers=agent)
    soup=BeautifulSoup(response.text,"html.parser")
    team1name=soup.find("div",class_="content-column")
    team2name=team1name.find("div",class_="container right")
    team2name=team2name.find("h3")
    team2name=team2name.get_text()
    team1name=team1name.find("div",class_="container left")
    team1name=team1name.find("h3")
    team1name=team1name.get_text()
    table=soup.find_all("tbody")
    scoreodds=0
    scoreevens=0
    for t in table:
        standings=t.find("tr", class_="odd team_rank")
        if(standings!=None):
            teamspotodd=t.find_all("tr",class_="odd highlight team_rank")
            teamspoteven=t.find_all("tr",class_="even highlight team_rank")
            for rank in teamspotodd:
                standing=rank.find("td",class_="rank")
                standing=standing.get_text()
                scoreodds=int(standing)
                if(scoreodds<4):
                    score+=scoreodds
                else:
                    break
            for rank in teamspoteven:
                standing=rank.find("td",class_="rank")
                standing=standing.get_text()
                scoreevens=int(standing)
                if(scoreevens<4):
                    score+=scoreevens
                else:
                    break
    if(scoreodds<4 and scoreevens <4):
        print(team1name[1:-1]," vs. ",team2name[1:-1]," Score = ",score)



def maingamescores(mainGames):
    for game in mainGames:
        link=game.find("td",class_="score-time score")
        a=link.find_all("a")
        #print(a)
        link=a[0].get('href')
        getscores(link)


def liveLeaguescores(liveLeagues):
    Rome = pytz.timezone('Europe/Rome')
    Rome_date_and_Time = datetime.now(Rome)
    current=Rome_date_and_Time
    #print(Rome_date_and_Time.strftime("%Y:%m:%d %H:%M"))
    for comp in liveLeagues:
        a=comp.find_all("a")
        league="http://int.soccerway.com"+a[0].get('href')
        agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
        response=requests.get(league, headers=agent)
        leaguesoup=BeautifulSoup(response.text, "html.parser")
        leaguename=leaguesoup.find("div", class_="yui-t6")
        leaguename=leaguename.find(id="bd")
        leaguename=leaguename.find(id="subheading")
        leaguename=leaguename.find("h1")
        matches=leaguesoup.find_all('tbody')
        allgames=[]
        for table in matches:
            t=table.find("tr", class_="even expanded match no-date-repetition")
            if(t!=None):
                allgames.append(table)
        for games in allgames:
                scores=games.find_all("td", class_="score-time status")
                if(scores!=[]):
                            #print("scores:\n\n\n\n\n",scores)
                    for i in range(0,len(scores)):
                        if((scores[i].get_text())[35:39]=="PSTP" or scores[i].get_text()[35:39]=="CANC"):
                            continue
                        else:
                            a=scores[i].find_all("a")
                                    #print(a)
                            link=a[0].get('href')
                            gameyear=link[9:13]
                            gamemonth=link[14:16]
                            gameday=link[17:19]
                            gametime=scores[i].get_text()
                            gametime=gametime[2:4]+gametime[5]+gametime[7:9]
                            gamehour=gametime[0:2]
                            gameminute=gametime[3:5]
                            current=str(current)
                            curyear=current[0:4]
                            curmonth=current[5:7]
                            curday=current[8:10]
                            curhour=current[11:13]
                            curminute=current[14:16]
                            #if game is still going
                            if(gameyear>curyear):
                                break
                            elif(gamemonth>curmonth):
                                break
                            elif(gameday>curday):
                                break
                            elif(gamehour>curhour):
                                break
                            elif(gamehour==curhour and gameminute>curminute):
                                break
                            else:
                                getscores(link)
                


def main():
    url = 'https://int.soccerway.com/'
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    response = requests.get(url, headers=agent)
    soup = BeautifulSoup(response.text, "html.parser")
    games=soup.find('tbody')
    #game section of website secured
    liveLeagues=games.find_all("tr", class_="group-head clickable live")
    liveLeaguescores(liveLeagues)
    evenFirst=games.find_all("tr", class_= "even highlight expanded first match no-date-repetition")
    evenLast=games.find_all("tr", class_= "even highlight expanded last match no-date-repetition")
    oddFirst=games.find_all("tr", class_= "odd highlight expanded first match no-date-repetition")
    oddLast=games.find_all("tr", class_= "odd highlight expanded last match no-date-repetition")
    odd=games.find_all("tr",class_="odd highlight expanded match no-date-repetition")
    even=games.find_all("tr",class_="even highlight expanded match no-date-repetition")
    loners=games.find_all("tr", class_="even highlight expanded first last match no-date-repetition")
    #live main games selected
    mainGames=evenFirst+evenLast+oddFirst+oddLast+odd+even+loners
    #get scores for the main games that are live
    maingamescores(mainGames)

main()
