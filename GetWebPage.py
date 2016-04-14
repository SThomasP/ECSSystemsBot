from urllib.request import urlopen
for line in urlopen('https://secure.ecs.soton.ac.uk/status/'):
    line = line.decode('utf-8')  # Decoding the binary data to text.
    if 'Core Priority Devices' in line:  #look for 'Core Priority Devices' To find the line of text with the list of issues
        lineIWant = line
    
