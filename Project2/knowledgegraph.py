import sys
import json
import urllib
import collections
from collections import defaultdict		# to initialize dictionary values to 0

# A function that extracts the important text from the values key of the path
# key of properties dictionary and stores it in ourList, returning ourList
def setDictVals(ourList, properties, path):
	if (path in properties):
		for x in properties[path]['values']:
			ourList.append(x['text'])
		return ourList

# Takes a string s and returns a list of count-sized pieces of the string
def splitCount(s, count):
	s = s.replace("\r","")
	s = s.replace("\n","")
	s = s.replace("\t","")
	remainder = len(s) % 110
	remainderStart = len(s) - remainder
	result = [''.join(x) for x in zip(*[list(s[z::count]) for z in range(count)])]
	result.append(s[remainderStart::])
	return result

# Outputs another row
def newRow(title, data):
	n = 120
	print '| ' + ('-' * n) + ' |'
	title = title + ':'
	print '| ' + title.ljust(n) + ' |'
	if data is list:
		for entry in data:
			newEntry(entry)
	else:
		newEntry(data)

# Does samething as newRow except data is stored
# at a dictionary key.
# Provides check that key exists
def newRowDict(title, d, k):
	if k in d and d[k]:
		newRow(title, d[k])

def newEntry(entry):
	#splitEntry = splitCount(entry, 70)
	n = 120
	for line in entry:
		if len(line) > n:
			splitLines = splitCount(line, 110)
			for splitLine in splitLines:
				print '| '.ljust(12) + splitLine.ljust(n-10) + ' |'
		else:
			print '| '.ljust(12) + line.ljust(110) + ' |'

# Concatenates attributes in d[k] to s followed by a pipe.
# Useful for outputting information for BusinessPerson
def concatAtts(s, d, k):
	if k in d:
		for att in d[k]:
			if att == d[k][0]:
				s += ' ' + att
			else:
				s += ', ' + att
		s += ' |'
	return s

# Make sure script utilized correctly with command line arguments
usageStr = "Usage error: Format must be python knowledgegraph.py -key <Freebase API key> -q <query> -t <infobox|question>\n"
usageStr += " or make ARGS=\"-key <Freebase API key> -q <query> -t <infobox|question>\"\n"
usageStr += " or python knowledgegraph.py -key <Freebase API key> -f <file of queries> -t <infobox|question>\n"
usageStr += " or make ARGS=\" -key <Freebase API key> -f <file of queries> -t <infobox|question>\""
if len(sys.argv) != 7:
	sys.exit(usageStr)
# args will store args in order they appear on reference implementation instructions
args = sys.argv
for i in xrange(len(sys.argv) -1):
	if i == '-key':
		args[1] = '-key'
		args[2] = sys.argv[i+1]
	elif i == '-q' or i == '-f':
		args[3] = sys.argv[i]
		args[4] = sys.argv[i+1]
	elif i == '-t':
		args[5] = '-t'
		args[6] = sys.argv[i+1]
if args[1] != '-key' or (args[3] != '-q' and args[3] != '-f') or args[5] != '-t' or (args[6] != 'infobox' and args[6] != 'question'):
	sys.exit(usageStr)
	
api_key = 'AIzaSyBsXEX0SMoWRYtQDRHWMHehGqmRiGRgQow'
#api_key = args[2]
print 'Let me see...'

# Handle infobox request (Part 1)
if args[6] == 'infobox':
	queryList = []
	if args[3] == '-q':
		queryList.append(args[4])
	elif args[3] == '-f':
		with open(args[4]) as f:
			queryList = f.readlines()
	
	# Generate infobox for each query term
	for query in queryList:
		# Remove new line char
		if query[-1] == '\n':
			query = query[:-1]

		# Output Query-Question
		print 'Query-Question: ' + query

		# Prepare query to Freebase Search and Topic APIs
		search_url = 'https://www.googleapis.com/freebase/v1/search'
		topic_url = 'https://www.googleapis.com/freebase/v1/topic'
		params = {
						'query': query,
						'key': api_key
		}
		# First query Freebase's Search API to get topics
		url = search_url + '?' + urllib.urlencode(params)
		response = json.loads(urllib.urlopen(url).read())
		search_results = response['result']

		infobox = {}

		# Gather information from query
		isPerson = False
		isAuthor = False
		isActor = False
		isBusinessPerson = False
		isLeague = False
		isSportsTeam = False
		# Run until we have a valild topicin search_results
		for result in search_results:
			# query Freebase's Topic API
			url = topic_url + result['mid'] + '?key=' + api_key
			topic_response = json.loads(urllib.urlopen(url).read())
			properties = topic_response['property']
			for val in properties['/type/object/type']['values']:
				# Check if search result is a Person
				if (val['id'] == '/people/person'):
					isPerson = True
					# Every attribute of person stored in a list at key attribute in person dict
					person = defaultdict(list)
					setDictVals(person['name'], properties, '/type/object/name')
					setDictVals(person['birthday'], properties, '/people/person/date_of_birth')
					setDictVals(person['birthplace'], properties, '/people/person/place_of_birth')
					setDictVals(person['deathdate'], properties, '/people/deceased_person/date_of_death')
					setDictVals(person['deathplace'], properties, '/people/deceased_person/place_of_death')
					setDictVals(person['deathcause'], properties, '/people/deceased_person/cause_of_death')
					# For consistency with the values being lists of strings in person, we only take one name per sibling/spouse
					if ('/people/person/sibling_s' in properties):
						for sibling in properties['/people/person/sibling_s']['values']:
							if ('/people/sibling_relationship/sibling' in sibling['property']):
								person['siblings'].append(sibling['property']['/people/sibling_relationship/sibling']['values'][0]['text'])
					if ('/people/person/spouse_s' in properties):
						for spouse in properties['/people/person/spouse_s']['values']:
							if ('/people/marriage/spouse' in spouse['property']):
								person['spouses'].append(spouse['property']['/people/marriage/spouse']['values'][0]['text'])
					if ('/common/topic/description' in properties):
						for x in properties['/common/topic/description']['values']:
							person['description'].append(x['value'])

					# set the person key of infobox to the person dict
					infobox['person'] = person

				# Check if search result is an Author
				elif (val['id'] == '/book/author'):
					isAuthor = True
					# Every attribute of author stored in a list at key attribute in author dict
					author = defaultdict(list)
					setDictVals(author['books'], properties, '/book/author/works_written')
					setDictVals(author['booksonauth'], properties, '/book/book_subject/works')
					setDictVals(author['influenced'], properties, '/influence/influence_node/influenced')
					setDictVals(author['influencedby'], properties, '/influence/influence_node/influenced_by')
					
					# set the author key of infobox to the author dict
					infobox['author'] = author

				# Check if search result is an Actor
				elif (not isActor and (val['id'] == '/film/actor' or val['id'] == '/tv/tv_actor')):
					isActor = True
					# Every attribute of actor stored in a dict a given index in the author list
					actor = []
					if ('/film/actor/film' in properties):
						for film in properties['/film/actor/film']['values']:
							f = defaultdict(list)
							# Every character played/film name of a film f stored in a list at key character/film in dict f
							setDictVals(f['character'], film['property'], '/film/performance/character')
							setDictVals(f['film'], film['property'], '/film/performance/film')
							actor.append(f)
					# set the 'actor' key of infobox to the actor dict
					infobox['actor'] = actor

				# Check if search result is a BusinessPerson
				elif (not isBusinessPerson and (val['id'] == '/organization/organization_founder' or val['id'] == '/business/board_member')):
					isBusinessPerson = True
					# Every attribute of businessperson stored in a list at key attribute in bp dict
					bp = defaultdict(list)
					setDictVals(bp['founded'], properties, '/organization/organization_founder/organizations_founded')
					# handle board member
					if ('/business/board_member/organization_board_memberships' in properties):
						# the key 'boardmember's value is a list of dicts for each org
						for org in properties['/business/board_member/organization_board_memberships']['values']:
							# Every attribute of org a is stored in a list at key attribute in dict a
							a = defaultdict(list)
							setDictVals(a['organization'], org['property'], '/organization/organization_board_membership/organization')
							setDictVals(a['title'], org['property'], '/organization/organization_board_membership/title')
							setDictVals(a['role'], org['property'], '/organization/organization_board_membership/role')
							setDictVals(a['from'], org['property'], '/organization/organization_board_membership/from')
							setDictVals(a['to'], org['property'], '/organization/organization_board_membership/to')
							bp['boardmember'].append(a)
					# handle leadership
					if ('/business/board_member/leader_of' in properties):
						# the key 'leadership's value is a list of dicts for each org
						for org in properties['/business/board_member/leader_of']['values']:
							# Every attribute of org a is stored in a list at key attribute in dict a
							a = defaultdict(list)
							setDictVals(a['organization'], org['property'], '/organization/leadership/organization')
							setDictVals(a['title'], org['property'], '/organization/leadership/title')
							setDictVals(a['role'], org['property'], '/organization/leadership/role')
							setDictVals(a['from'], org['property'], '/organization/leadership/from')
							setDictVals(a['to'], org['property'], '/organization/leadership/to')
							bp['leadership'].append(a)
					# set the 'businessperson' key of infobox to the bp dict
					infobox['businessperson'] = bp

				# Check if search result is a League
				elif (val['id'] == '/sports/sports_league'):
					isLeague = True
					# Every attribute of league stored in a list at key attribute in league dict
					league = defaultdict(list)
					setDictVals(league['name'], properties, '/type/object/name')
					setDictVals(league['championship'], properties, '/sports/sports_league/championship')
					setDictVals(league['sport'], properties, '/sports/sports_league/sport')
					setDictVals(league['slogan'], properties, '/organization/organization/slogan')
					setDictVals(league['website'], properties, '/common/topic/official_website')
					if ('/common/topic/description' in properties):
						for x in properties['/common/topic/description']['values']:
							league['description'].append(x['value'])
					# For consistency purposes, we only take the first team name of a given team (league is dict of lists of strs)
					if ('/sports/sports_league/teams' in properties):
						for team in properties['/sports/sports_league/teams']['values']:
							if ('/sports/sports_league_participation/team' in team['property']):
								league['teams'].append(team['property']['/sports/sports_league_participation/team']['values'][0]['text'])
					# set the 'league' key of infobox to the league dict
					infobox['league'] = league

				# Check if search result is a SportsTeam
				elif (not isSportsTeam and (val['id'] == '/sports/sports_team' or val['id'] == '/sports/professional_sports_team')):
					isSportsTeam = True
					# Every attribute of team stored in a list at key attribute in team dict
					team = defaultdict(list)
					setDictVals(team['name'], properties, '/type/object/name')
					if ('/common/topic/description' in properties):
						for x in properties['/common/topic/description']['values']:
							team['description'].append(x['value'])
					setDictVals(team['sport'], properties, '/sports/sports_team/sport')
					setDictVals(team['arena'], properties, '/sports/sports_team/arena_stadium')
					setDictVals(team['championships'], properties, '/sports/sports_team/championships')
					if ('/sports/sports_team/coaches' in properties):
						# the key 'coaches's value is a list of dicts for each coach
						for coach in properties['/sports/sports_team/coaches']['values']:
							# Every attribute of coach c is stored in a list at key attribute in c dict
							c = defaultdict(list)
							setDictVals(c['name'], coach['property'], '/sports/sports_team_coach_tenure/coach')
							setDictVals(c['number'], coach['property'], '/sports/sports_team_coach_tenure/number')
							setDictVals(c['from'], coach['property'], '/sports/sports_team_coach_tenure/from')
							setDictVals(c['to'], coach['property'], '/sports/sports_team_coach_tenure/to')
							setDictVals(c['position'], coach['property'], '/sports/sports_team_coach_tenure/position')
							team['coaches'].append(c)
					setDictVals(team['founded'], properties, '/sports/sports_team/founded')
					if ('/sports/sports_team/league' in properties):
						for league in properties['/sports/sports_team/league']['values']:
							if ('/sports/sports_league_participation/league' in league['property']):
								team['leagues'].append(league['property']['/sports/sports_league_participation/league']['values'][0]['text'])
					setDictVals(team['locations'], properties, '/sports/sports_team/location')
					if ('/sports/sports_team/roster' in properties):
						# the key 'players's value is a list of dicts for each player
						for player in properties['/sports/sports_team/roster']['values']:
							# Every attribute of player c is stored in a list at key attribute in c dict
							c = defaultdict(list)
							setDictVals(c['name'], player['property'], '/sports/sports_team_roster/player')
							setDictVals(c['number'], player['property'], '/sports/sports_team_roster/number')
							setDictVals(c['from'], player['property'], '/sports/sports_team_roster/from')
							setDictVals(c['to'], player['property'], '/sports/sports_team_roster/to')
							setDictVals(c['position'], player['property'], '/sports/sports_team_roster/position')
							team['players'].append(c)
					# set the 'businessperson' key of infobox to the bp dict
					infobox['team'] = team

			# If we have received valuable information from this search result, we stop querying Topic API
			if (isPerson or isAuthor or isActor or isBusinessPerson or isLeague or isSportsTeam):
				break

		
		# Output Results
		if isPerson:
			# Print Person and Types
			print '  ' + ('-' * 120)

			nameString ='| ' + infobox['person']['name'][0]
			if (isAuthor or isActor or isBusinessPerson):
				nameString += '('
				if (isAuthor):
					nameString += 'AUTHOR'
					if (isActor or isBusinessPerson):
						nameString += ', '
					else:
						nameString += ')'
				if (isActor):
					nameString += 'ACTOR'
					if (isBusinessPerson):
						nameString += ', '
					else:
						nameString += ')'
				if (isBusinessPerson):
					nameString += 'BUSINESS_PERSON)'

			print nameString.ljust(122) + ' |'

			# Print Person Attributes
			person = infobox['person']
			newRowDict('Name', person, 'name')
			newRowDict('Birthday', person, 'birthday')
			if (person['deathdate'] or person['deathplace'] or person['deathcause']):
				newRowDict('Death date', person, 'deathdate')
				newRowDict('Death place', person, 'deathplace')
				newRowDict('Death causes', person, 'deathcause')
			newRowDict('Place of birth', person, 'birthplace')
			newRowDict('Description', person, 'description')
			newRowDict('Siblings', person, 'siblings')
			newRowDict('Spouses', person, 'spouses')

			# Print Actor Attributes
			if (isActor):
				if infobox['actor']:
					data = []
					for film in infobox['actor']:
						element = '|'
						element = concatAtts(element, film, 'character')
						element = concatAtts(element, film, 'film')
						data.append(element)
					newRow('Films (Character | Film Name)', data)

			# Print Author Attributes
			if (isAuthor):
				author = infobox['author']
				newRowDict('Books', author, 'books')
				newRowDict('Influenced by', author, 'influencedby')
				newRowDict('Books about', author, 'booksonauth')
				newRowDict('Influenced', author, 'influenced')

			# Print BusinessPerson Attributes
			if (isBusinessPerson):
				bp = infobox['businessperson']
				newRowDict('Founded', bp, 'founded')
				if (bp['leadership']):
					data = []
					for org in bp['leadership']:
						element = '|'
						element = concatAtts(element, org, 'organization')
						element = concatAtts(element, org, 'role')
						element = concatAtts(element, org, 'title')
						element = concatAtts(element, org, 'from')
						element = concatAtts(element, org, 'to')
						data.append(element)
					newRow('Leadership: | Organization | Role | Title | From-To |', data)
				if (bp['boardmember']):
					data = []
					for org in bp['boardmember']:
						element = '|'
						element = concatAtts(element, org, 'organization')
						element = concatAtts(element, org, 'role')
						element = concatAtts(element, org, 'title')
						element = concatAtts(element, org, 'from')
						element = concatAtts(element, org, 'to')
						data.append(element)
					newRow('Board Member: | Organization | Role | Title | From-To |', data)
			print '| ' + ('-' * 120) + ' |\n\n'

		# Print League Attributes
		elif isLeague:
			league = infobox['league']
			if 'name' in league:
				print '  ' + ('-' * 120)
				temp = '| ' + league['name'][0] + '(LEAGUE)'
				print temp.ljust(122) + ' |'
				newRow('Name', league['name'])
			newRowDict('Sport', league, 'sport')
			newRowDict('Slogan', league, 'slogan')
			newRowDict('Official website', league, 'website')
			newRowDict('Championship', league, 'championship')
			newRowDict('Teams', league, 'teams')
			newRowDict('Description', league, 'description')
			print '| ' + ('-' * 120) + ' |\n\n'

		# Print SportsTeam Attributes
		elif isSportsTeam:
			team = infobox['team']
			if team['name']:
				print '  ' + ('-' * 120)
				temp = '| ' + team['name'][0] + '(SPORTS TEAM)'
				print temp.ljust(122) + ' |'
				newRow('Name', team['name'])
			newRowDict('Sport', team, 'sport')
			newRowDict('Arena', team, 'arena')
			newRowDict('Championships', team, 'championships')
			newRowDict('Founded', team, 'founded')
			newRowDict('Leagues', team, 'leagues')
			if team['coaches']:
				data = []
				for coach in team['coaches']:
					element = '|'
					element = concatAtts(element, coach, 'name')
					element = concatAtts(element, coach, 'position')
					element = concatAtts(element, coach, 'from')
					element = concatAtts(element, coach, 'to')
					data.append(element)
				newRow('Coaches: | Name | Position | From | To |', data)
			if team['players']:
				data = []
				for player in team['players']:
					element = '|'
					element = concatAtts(element, player, 'name')
					element = concatAtts(element, player, 'position')
					element = concatAtts(element, player, 'number')
					element = concatAtts(element, player, 'from')
					element = concatAtts(element, player, 'to')
					data.append(element)
				newRow('PlayersRoster: | Name | Position | Number | From | To |', data)
			newRowDict('Description', team, 'description')
			print '| ' + ('-' * 120) + ' |\n\n'
		else:
			print 'No related information about the query ' + query + ' was found!'

elif args[6] == 'question':
	queryList = []
	if args[3] == '-q':
		queryList.append(args[4])
	elif args[3] == '-f':
		with open(args[4]) as f:
			queryList = f.readlines()
	
	# Generate infobox for each query term
	for question in queryList:
		if question[-1] == '\n':
			question = question[:-1]

		# Output Query-Question
		print 'Query-Question: ' + question

		# Modify query for API
		query = question[12:]
		if query[-1] == '?':
			query = query[:-1]

		# Prepare for book query and organization query to the Freebase MQL API using query
		search_url = "https://www.googleapis.com/freebase/v1/mqlread"
		
		# set book and organization query parameters
		bookQuery = '[{"/book/author/works_written": [{"a:name": null,"name~=": "' + query + '"}],"id": null,"name": null,"type": "/book/author"}]'
		orgQuery = '[{"/organization/organization_founder/organizations_founded": [{"a:name": null,"name~=": "' + query + '"}],"id": null,"name": null,"type": "/organization/organization_founder"}]'
		bookParams = {
						'query': bookQuery,
						'key': api_key
		}
		orgParams = {
						'query': orgQuery,
						'key': api_key
		}
		
		# Query Freebase MQL API
		bookUrl = search_url + '?' + urllib.urlencode(bookParams)
		orgUrl = search_url + '?' + urllib.urlencode(orgParams)
		bookResponse = json.loads(urllib.urlopen(bookUrl).read())
		orgResponse = json.loads(urllib.urlopen(orgUrl).read())

		# Store 'result' key of response dictionary as list book/org results
		bookResults = []
		orgResults = []
		if 'result' in bookResponse:
			bookResults = bookResponse['result']
		if 'result' in orgResponse:
			orgResults = orgResponse['result']

		# creators dictionary maps a person's name to a list of (as_what_kind_of_person, list_of_created_this) tuples
		creators = defaultdict(list)

		for item in bookResults:
			if '/book/author/works_written' in item:
				# incase book has two names (possible under Freebase's organization strategy)
				bookList = []
				for book in item['/book/author/works_written']:
					if 'a:name' in book:
						bookList.append(book['a:name'])
				# append tuple to list
				creators[item['name']].append(('Author', bookList))

		for item in orgResults:
			# incase organization has two names (possible under Freebase's organization strategy)
			if '/organization/organization_founder/organizations_founded' in item:
				orgList = []
				for org in item['/organization/organization_founder/organizations_founded']:
					if 'a:name' in org:
						orgList.append(org['a:name'])
				# append tuple to list
				creators[item['name']].append(('Business Person', orgList))

		# Output results
		print '  ' + ('-' * 120)
		temp = '| ' + question
		print temp.ljust(122) + ' |' 

		# creators is a dict with keys sorted
		creators = collections.OrderedDict(sorted(creators.items()))

		# Output creator as type_of_creator created:
		#				creation a
		# 			creation b
		#				...
		for key in creators:
			books = []
			orgs = []
			for creation in creators[key]:
				for work in creation[1]:
					if creation[0] == 'Author':
						books.append(work)
					else:
						orgs.append(work)
			if books:
				newRow(key + ' as Author created', books)
			if orgs:
				newRow(key + ' as Business Person created', orgs)

		print '| ' + ('-' * 120) + ' |\n\n'



