from urllib.request import urlopen

def ComposeTweet(service, machine, problem):
    if service=='Machine':
        issue='Machine '
    else:
        issue='Service '+service+' on '
    issue=issue+machine;
    if problem=='DOWN':
        issue=issue+' has gone down.'
    elif problem=='ERROR':
        issue=issue+' has an error, see status page for more detail.'
    print(issue)
    return issue

for line in urlopen('https://secure.ecs.soton.ac.uk/status/'):
    line = line.decode('utf-8')  # Decoding the binary data to text.
    if 'Core Priority Devices' in line:  #look for 'Core Priority Devices' To find the line of text with the list of issues
        linesIWant = line.split('Priority Devices')[2].split("</tr>")
        linesIWant.pop()
        linesIWant.pop(0)
for f in linesIWant:
    if  not 'border: 0px' in f:
        if 'machine' in f:
            machineName=f.split('<b>')[1].split('</b>')[0]
            if 'state_2' in f:
                service=f.split('<td>')[2].split('</td>')[0]
                problem=f.split('<td>')[3].split('</td>')[0]
                ComposeTweet(service,machineName,problem)
        elif 'state_2' in f:
            service=f.split('<td>')[1].split('</td>')[0]
            problem=f.split('<td>')[2].split('</td>')[0]
            ComposeTweet(service,machineName,problem)

