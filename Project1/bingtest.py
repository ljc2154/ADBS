import urllib2
import base64
import json
from collections import defaultdict		# to initialize dictionary values to 0
from math import log # for log for idf

# Take query from user
query = raw_input()
queryTerms = query.split()
query = queryTerms[0]
# Convert query to HTTP string
for term in xrange(len(queryTerms)-1):
	query += ("+"+queryTerms[term+1])

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

# Keep track of the number of relevant and irrelevant docs
relevantCount = 0
irrelevantCount = 0

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
		relevantCount = relevantCount + 1
		docs[i]['relevant'] = 'Y'
	else:
		irrelevantCount = irrelevantCount + 1
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


# 2 dictionaries for relevant and nonrelevant
relevant = defaultdict(int)
irrelevant = defaultdict(int)
for i in xrange(10):
	if docs[i]['relevant'] == 'Y':
		for key in docs[i]['scores']:
			relevant[key] = relevant[key] + docs[i]['scores'][key]
	else:
		for key in docs[i]['scores']:
			relevant[key] = relevant[key] + docs[i]['scores'][key]


# merge into master dictionary: subtract relvant from nonrelevant
master = defaultdict(int)
max1Score = -100
max2Score = -100
max1Term = ""
max2Term = ""
for key in relevant:
	master[key] = (.75 * relevant[key])/relevantCount - (.15 * irrelevant[key])/irrelevantCount
	notYetATerm = True
	for term in queryTerms:
		if key == term:
			notYetATerm = False
	if (notYetATerm):
		if (master[key] > max1Score):
			newMax2 = max1Score
			newMax2Term = max1Term
			max1Score = master[key]
			max1Term = key
			max2Score = newMax2
			max2Term = newMax2Term
		elif (master[key] > max2Score):
			max2Score = master[key]
			max2Term = key

# Add 2 highest scoring terms to query
queryTerms.append(max1Term)
queryTerms.append(max2Term)

for term in queryTerms:
	print term
# sort terms by master score
# set that as new query
	
	
