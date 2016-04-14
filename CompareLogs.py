def intersection(a,b):
    return list(set(a) & set(b))

def union(a,b):
    return list(set(a) | set(b))

def ComposeTweet(service, machine, problem, fixed):
    if fixed==1:
        if service=='Machine':
            issue='Machine '
        else:
            issue='Service '+service+' on '
        issue=issue+machine;
        if problem=='DOWN':
            issue=issue+' has gone down.'
        elif problem=='ERROR':
            issue=issue+' has an error, see status page for more detail.'
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
    return issue

temp=open('oldlog.txt','r')
oldlog=temp.read().splitlines()
temp.close()
temp=open('newlog.txt','r')
newlog=temp.read().splitlines()
temp.close()
theUnion=union(oldlog,newlog)
theIntersection=intersection(oldlog,newlog)
for f in theUnion:
    problem=f.split(',')
    if ((f in oldlog) and (not f in theIntersection)):
        ComposeTweet(problem[0],problem[1],problem[2],0)
    elif ((f in newlog) and (not f in theIntersection)):
        ComposeTweet(problem[0],problem[1],problem[2],1)
