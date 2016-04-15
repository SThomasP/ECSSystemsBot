def getWebPage():
    from urllib.request import urlopen
    #opens up the status page
    for line in urlopen('https://secure.ecs.soton.ac.uk/status/'):
        line = line.decode('utf-8')  # Decoding the binary data to text.
        if 'Core Priority Devices' in line:  #look for 'Core Priority Devices' To find the line of text with the list of issues
            linesIWant = line.split('Priority Devices')[2].split("<tr")
            #pops the top and bottom line as these are useless
            linesIWant.pop()
            linesIWant.pop(0)
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
                    issues.append(service+','+machineName+','+problem+'\n')
            elif 'state_2' in f:
                #if its not a machine but has an issue log get the service name, and problem type, the machine will be the last machine to be iterated through
                service=f.split('<td>')[1].split('</td>')[0]
                problem=f.split('<td>')[2].split('</td>')[0]
                issues.append(service+','+machineName+','+problem+'\n')
    return issues

def intersection(a,b):
    #return the a list of the items in a intersection of two other lists
    return list(set(a) & set(b))

def union(a,b):
    #returns the union of two lists
    return list(set(a) | set(b))

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
            issue=issue+' has gone down.\U0001F63F'
        elif problem=='ERROR':
            issue=issue+' has an error, see status page for more detail.\U0001F63F'
            #\U0001F63F is the crying cat face emoji
    elif fixed==0:
        if service=='Machine':
            issue='Machine '
        else:
            issue='Service '+service+' on '
        issue=issue+machine;
        if problem=='DOWN':
            issue=issue+' is now back up.\U0001F638'
        elif problem=='ERROR':
            issue=issue+' is now error free.\U0001F638'
            #\U0001F638 is the grinning cat face emoji
    #returns the completed tweet
    return issue

def tweet(API, theTweet):
    #sends the tweet to the twitter API
    API.update_status(theTweet)


