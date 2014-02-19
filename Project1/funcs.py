import urllib2
import base64
import json
from collections import defaultdict		# to initialize dictionary values to 0
from math import log # for log for idf

def queryBing(query, bingUrl, accountKey):
	# Query bing api and receive response
	accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
	headers = {'Authorization': 'Basic ' + accountKeyEnc}
	req = urllib2.Request(bingUrl, headers = headers)
	response = urllib2.urlopen(req)

	# content contains the xml/json response from Bing. 
	content = response.read()
	results = json.loads(content)

	# return the list of the results stored as dictionaries
	return results['d']['results']

def displayResultsAndGetFeedback(docs):
	print "Total no of results : " + str(len(docs))
	print "Bing Search Results:"
	print "======================"

	# traverse results
	for i in xrange(len(docs)):
		# Print the search result for the user
		print "Result", i+1
		print "["
		print " Title: " + docs[i]['Title']
		print " Description: " + docs[i]['Description']
		print " Url: " + docs[i]['Url']
		print "]\n"
		# Obtain relevance feedback and update rel/irrel info
		answer = "X"
		while answer is not "Y" and answer is not "N":
			print "Relevant (Y/N)?"
			answer = raw_input()
		if answer is "Y":
			docs[i]['relevant'] = 'Y'
		else:
			docs[i]['relevant'] = 'N'
	return docs

# Returns the number of relevant documents
def getRelevantCount(docs):
	relevantCount = 0
	for i in xrange(len(docs)):
		if docs[i]['relevant'] is 'Y':
			relevantCount = relevantCount + 1
	return relevantCount

# Returns true if desired precision of relevant documents reached.
# Returns false otherwise
def precisionReached(docs, precision):
	relevantCount = getRelevantCount(docs)
	nonrelevantCount = len(docs) - relevantCount
	currentPrecision = float(relevantCount) / len(docs)
	print "Precision " + str(currentPrecision)
	if (currentPrecision >= precision):
		print "Desired precision reached, done"
		return True
	else:
		print "Still below the desired precision of " + str(precision)
		return False