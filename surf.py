#python2
import os, getpass, urllib, re, time 

os.system('clear')

print('Enter desired times in 24 hour format\nExample: 7am is 0700. 7pm is 1900\nType Done when finished inputting times\n')

input_time = ''
times = []

while input_time != 'Done' and input_time != 'done' and input_time != 'DONE':
	input_time = raw_input('input times: ')
	if input_time.isdigit() and len(input_time) >=3 and len(input_time) <= 4:
		times.append(input_time)	
	else:
		print('Invalid input')

os.system('clear')

print('Enter desired phone numbers with area code\nExample: 401-363-2836 would be 4013632836\nType Done when finished inputting numbers\n')

input_phones = ''
phones = []

while input_phones != 'Done' and input_phones != 'done' and input_phones != 'DONE':
	input_phones = raw_input('Input phone numbers: ')
	if input_phones.isdigit() and len(input_phones) == 10:
		phones.append(input_phones)
	else:
		print('Invalid input')

os.system('clear')
print('Waiting...')

url = 'http://www.swellinfo.com/surf-forecast/newport-rhode-island'

tag = '''<td width="35" align="right">(.+?)</td>
			<td width="30" align="center"><div class=".+?"></div></td>
			<td width="66" align="center">(.+?)</td>
			<td width="36" align="center">(.+?)</td>
			<td width="22" align="center"><div class=".+?"></div></td>
			<td width="87" align="center">(.+?)</td>'''

info = []
message_array = []

def get_url(url, tag):
	htmlfile = urllib.urlopen(url)
	htmltext = htmlfile.read()
	pattern = re.compile(tag)
	data = re.findall(pattern, htmltext)
	for x in data:
		info.append(x)

def send():
	print('\nSending to...')
	for x in phones:
		print(x)
	for x in range(0,len(info)):
		message = '%s Forecast\nWind Direction: %s\nSwell Direction: %s\nSwell Height and Interval: %s' % (info[x][0][0:], info[x][1][0:], info[x][2][0:], info[x][3][0:])
		message_array.append(message)

	message = ''
	for x in range(0,4):
		message = message + '\n' + message_array[x]

	for x in range(0,len(phones)):
		os.system("""osascript<<END

		 tell application "Messages"
		 		set stored to {}
		        set targetService to 1st service whose service type = iMessage
		        set targetBuddy to buddy "%s" of targetService
		        send "%s" to targetBuddy
		    END""" % (int(phones[x]), time.strftime("%d/%m/%Y") + message))
	time.sleep(60)

while True:
	for x in range(0, len(times)):	
		if time.strftime("%H%M") == times[x]:
			get_url(url, tag)
			send()
