import urllib2
import base64
import json

query = raw_input()
query = query.replace(" ", "+")

bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27' + query + '%27&$top=10&$format=json'
#Provide your account key here
accountKey = 'NCei/F/B/mWf0X51305yv4IqAv8uuJKQ1Fx55SGzMqQ'

accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
headers = {'Authorization': 'Basic ' + accountKeyEnc}
req = urllib2.Request(bingUrl, headers = headers)
response = urllib2.urlopen(req)
content = response.read()
#content contains the xml/json response from Bing. 
results = json.loads(content)

relevant = []

print "Bing Search Results"
print "==================="

for i in xrange(10):
	print "Result", i+1
	print "Title: " + results['d']['results'][i]['Title']
	print "Description: " + results['d']['results'][i]['Description']
	print "Url: " + results['d']['results'][i]['Url']
	answer = "X"
	while answer is not "Y" and answer is not "N":
		print "\nIs this relevant? (Y/N)"
		answer = raw_input()
	if answer is "Y":
		relevant.append(results['d']['results'][i])
	print "\n==================================================\n"
print relevant[3]['Url']
