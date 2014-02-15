import urllib2
import base64
import json
from collections import defaultdict		# to initialize dictionary values to 0
from math import log # for log for idf

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
docs = results['d']['results']

print "Bing Search Results"
print "==================="

# Intialize idf dictionary to 0 for all documents
idf = defaultdict(list)

# traverse results
for i in xrange(10):
	# Print the search result for the user
	print "Result", i+1
	print "Title: " + docs[i]['Title']
	print "Description: " + docs[i]['Description']
	print "Url: " + docs[i]['Url']
	# Obtain relevance feedback
	answer = "X"
	while answer is not "Y" and answer is not "N":
		print "\nIs this relevant? (Y/N)"
		answer = raw_input()
	if answer is "Y":
		docs[i]['relevant'] = 'Y'
	else:
		docs[i]['relevant'] = 'N'
	print "\n==================================================\n"

	# Initialize all term scores to 0 for document
	docs[i]['scores'] = defaultdict(int)

	# Remove unnecessary characters
	docs[i]['Description'] = docs[i]['Description'].replace('.', '')
	docs[i]['Description'] = docs[i]['Description'].replace(',', '')
	docs[i]['Description'] = docs[i]['Description'].replace('&', '')
	# terms is the list of words in a document
	terms = docs[i]['Description'].split()
	# wordCt represents the number of words in a given document
	wordCt = float(len(terms))

	#for each term slurped, increment term's score for document
	for term in terms:
		# increment normalized term score
		docs[i]['scores'][term] = (docs[i]['scores'][term] + 1)/wordCt
		
		# elongate list if necessary
		if (len(idf[term]) is 0):
			idf[term] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

		# mark idf for this document
		idf[term][i] = 1

# Calculate actual idfs
for key in idf:
	count = 0
	for i in xrange(10):
		count = count + idf[key][i]
	idf[key][10] = count

# Apply idf to document's term scores
for i in xrange(10):
	for key in docs[i]['scores']:
		docs[i]['scores'][key] = docs[i]['scores'][key] * log(10./idf[key][10])
		print docs[i]['scores'][key]

# 2 dictionaries for relevant and nonrelevant
# taken as sums
# multiply by coefficients
# merge into master dictionary: subtract relvant from nonrelevant
# take 2 highest non original query scores from master
# sort terms by master score
# set that as new query
	
	
