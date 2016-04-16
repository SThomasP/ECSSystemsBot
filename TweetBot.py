#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys, urllib.request, requests, datetime

def getIssues():
    #opens up the status page
    for line in urllib.request.urlopen('https://secure.ecs.soton.ac.uk/status/'):
        line = line.decode('utf-8')  # Decoding the binary data to text.
        if 'Core Priority Devices' in line:  #look for 'Core Priority Devices' To find the line of text with the list of issues
            #split the text for different priorities, 1 for core, 2 for standard, then split by table rows
            linesIWant = line.split('Priority Devices')[1].split("<tr")
            #pops the top and bottom line as these are useless
            linesIWant.pop()
            linesIWant.pop(0)
            #combines the two lists of lines
            issues=[]
    for f in linesIWant:
        #if its not one of the border cells analyse the code
        if  not 'border: 0px' in f:
            #if the row is classed as a machine, run this script
            if 'machine' in f:
                #find the machine name as its the only one in bold tags
                machineName=f.split('<b>')[1].split('</b>')[0]
                if 'state_2' in f:
                    #if the machine itself has an issue, get the service name and the problem
                    service=f.split('<td>')[2].split('</td>')[0]
                    problem=f.split('<td>')[3].split('</td>')[0]
                    #add the issue to the list
                    issues.append(service+','+machineName+','+problem)
            elif 'state_2' in f:
                #if its not a machine but has an issue log get the service name, and problem type, the machine will be the last machine to be iterated through
                service=f.split('<td>')[1].split('</td>')[0]
                problem=f.split('<td>')[2].split('</td>')[0]
                issues.append(service+','+machineName+','+problem)
    return issues

def intersection(a,b):
    #return the a list of the items in a intersection of two other lists
    return list(set(a) & set(b))

def union(a,b):
    #returns the union of two lists
    return list(set(a) | set(b))

def addToTweetLog(logdata):
    #create the text to be logged, the tweet followed by the time it was tweeted
    tobelogged='{'+logdata+'}'+str(datetime.datetime.now())
    #open the log file in append mode
    logfile=open('TweetLog.txt','a')
    #write the log to the log file, with a new line character
    logfile.write(tobelogged+'\n')
    #close the log file
    logfile.close()
    #print the log data
    print(tobelogged)

def statusPageTweet(down):
    #if page is down, down==0, if not down==1
    if down==0:
        returnTweet='Status Page unaccessable, secure.ecs is most likley down.\U0001F63F'
        #\U0001F63F is the crying cat face emoji
    elif down==0:
        returnTweet='Can access status page again, will tweet soon about any new developments.\U0001F638'
        #\U0001F638 is the grinning cat face emoji

def ComposeTweet(service, machine, problem, fixed):
    #writes the tweets themselves based on a very formualic
    if fixed==1:
        #fixed = 1 means the issue has not been fixed
        if service=='Machine':
            issue='Machine '
        else:
            issue='Service '+service+' on '
        issue=issue+machine;
        if problem=='DOWN':
            issue=issue+' has gone down.'
        elif problem=='ERROR':
            issue=issue+' has an error, see status page for more detail.'
    #fixed = 0 means the issue has been fixed
    elif fixed==0:
        if service=='Machine':
            issue='Machine '
        else:
            issue='Service '+service+' on '
        issue=issue+machine;
        if problem=='DOWN':
            issue=issue+' is now back up.'
        elif problem=='ERROR':
            issue=issue+' is now error free.'
    #returns the completed tweet
    return issue

def tweet(api, theTweet):
    api.update_status(theTweet)
    #log the tweet
    addToTweetLog(theTweet)
    #waits 30 seconds after tweeting
    time.sleep(30)
    
def checkPageUp():
    #users the requests library to check if the page is up
    resp=requests.head('https://secure.ecs.soton.ac.uk/status/')
    #if the page is up the status code is 200, if the page is down its 404
    return not(resp.status_code==200)

def connectToTwitter():
    #open the file containing the consumer tokens
    TokensFile=open('ConsumerTokens','r')
    temp = TokensFile.read().splitlines()
    TokensFile.close()
    #store the consumer tokens in their variables
    cToken=temp[0]
    cTokenS=temp[1]
    #does the same now with the access tokens
    TokensFile=open('AccessTokens','r')
    temp = TokensFile.read().splitlines()
    TokensFile.close()
    aToken=temp[0]
    aTokenS=temp[1]
    #sets up the auth variable
    auth = tweepy.OAuthHandler(cToken, cTokenS)
    #does the same with the access tokens
    auth.set_access_token(aToken, aTokenS)
    api=tweepy.API(auth)
    return api

def getIssueLog():
    logFile=open('IssueLog.txt','r')
    issues=logFile.read().splitlines()
    logFile.close()
    return issues

def saveToLog(issues):
    logFile=open('IssueLog.txt','w')
    for f in issues:
        logFile.write(f+'\n')
    logFile.close()

api=connectToTwitter()
#sets up the connection to twitter
loggedIssues=getIssueLog()
#loads the issue log from the previous sessions
siteDown=False
#defaults the logged issues and if the page is down
while True:
    #iterate forever
    siteNowDown=checkPageUp()
    #if the site has gone down since the last scan, or if it has come back up
    if not siteDown==siteNowDown:
        #if the site has gone down, tweet about it
        if siteNowDown:
            tweet(api,statusPageTweet(0))
        else:
        #if the site has come back up, tweet about it
            tweet(api,statusPageTweet(1))
        siteDown=siteNowDown
    if not siteDown:
        issues=getIssues()
        theUnion=union(loggedIssues,issues)
        theIntersection=intersection(loggedIssues,issues)
        for f in theUnion:
            problem=f.split(',')
            if ((f in loggedIssues) and (not f in theIntersection)):
                #tweet that the problem has arisen 
                tweet(api,ComposeTweet(problem[0],problem[1],problem[2],0))
            elif ((f in issues) and (not f in theIntersection)):
                #tweet that the problem has been fixed
                tweet(api,ComposeTweet(problem[0],problem[1],problem[2],1))
        loggedIssues=issues
        saveToLog(loggedIssues)
    #sleep for 30 minutes before running the script again 
    time.sleep(1800)

    

    
