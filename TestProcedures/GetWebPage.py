from urllib.request import urlopen
for line in urlopen('https://secure.ecs.soton.ac.uk/status/'):
    line = line.decode('utf-8')  # Decoding the binary data to text.
    if 'Core Priority Devices' in line:  #look for 'Core Priority Devices' To find the line of text with the list of issues
        linesIWant = line.split('Priority Devices')[2].split("<tr")
        linesIWant.pop()
        linesIWant.pop(0)
        issues=[]
for f in linesIWant:
    if  not 'border: 0px' in f:
        if 'machine' in f:
            machineName=f.split('<b>')[1].split('</b>')[0]
            if 'state_2' in f:
                service=f.split('<td>')[2].split('</td>')[0]
                problem=f.split('<td>')[3].split('</td>')[0]
                issues.append(service+','+machineName+','+problem+'\n')
        elif 'state_2' in f:
            service=f.split('<td>')[1].split('</td>')[0]
            problem=f.split('<td>')[2].split('</td>')[0]
            issues.append(service+','+machineName+','+problem+'\n')
logfile=open('newlog.txt','w')
logfile.writelines(issues)
logfile.close()
