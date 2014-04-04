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


# Make sure script utilized correctly with command line arguments
args = sys.argv
if len(args) != 7 or args[1] != '-key' or (args[3] != '-q' and args[3] != '-f') or args[5] != '-t' or (args[6] != 'infobox' and args[6] != 'question'):
	usageStr = "Usage error: Format must be python knowledgegraph.py -key <Freebase API key> -q <query> -t <infobox|question>\n"
	usageStr += " or make ARGS=\"-key <Freebase API key> -q <query> -t <infobox|question>\"\n"
	usageStr += " or python knowledgegraph.py -key <Freebase API key> -f <file of queries> -t <infobox|question>\n"
	usageStr += " or make ARGS=\" -key <Freebase API key> -f <file of queries> -t <infobox|question>\""
	sys.exit(usageStr)
	
api_key = 'AIzaSyBsXEX0SMoWRYtQDRHWMHehGqmRiGRgQow'
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
		search_url = 'https://www.googleapis.com/freebase/v1/search'
		topic_url = 'https://www.googleapis.com/freebase/v1/topic'
		params = {
						'query': query,
						'key': api_key
		}
		url = search_url + '?' + urllib.urlencode(params)
		response = json.loads(urllib.urlopen(url).read())
		search_results = response['result']

		infobox = defaultdict(dict)

		# Gather information from query
		isPerson = False
		isAuthor = False
		isActor = False
		isBusinessPerson = False
		isLeague = False
		isSportsTeam = False
		for result in search_results:
			url = topic_url + result['mid'] + '?key=' + api_key
			topic_response = json.loads(urllib.urlopen(url).read())
			properties = topic_response['property']
			for val in properties['/type/object/type']['values']:
				# Check if search result is a Person
				if (val['id'] == '/people/person'):
					isPerson = True
					person = defaultdict(list)
					person['name'] = setDictVals(person['name'], properties, '/type/object/name')
					person['birthday'] = setDictVals(person['birthday'], properties, '/people/person/date_of_birth')
					person['birthplace'] = setDictVals(person['birthplace'], properties, '/people/person/place_of_birth')
					person['deathdate'] = setDictVals(person['Deathdate'], properties, '/people/deceased_person/date_of_death')
					person['deathplace'] = setDictVals(person['deathplace'], properties, '/people/deceased_person/place_of_death')
					person['deathcause'] = setDictVals(person['deathcause'], properties, '/people/deceased_person/cause_of_death')
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

					infobox['person'] = person

				# Check if search result is an Author
				elif (val['id'] == '/book/author'):
					isAuthor = True
					author = defaultdict(list)
					author['books'] = setDictVals(author['books'], properties, '/book/author/works_written')
					author['booksonauth'] = setDictVals(author['booksonauth'], properties, '/book/book_subject/works')
					author['influenced'] = setDictVals(author['influenced'], properties, '/influence/influence_node/influenced')
					author['influencedby'] = setDictVals(author['influencedby'], properties, '/influence/influence_node/influenced_by')
					infobox['author'] = author

				# Check if search result is an Actor
				elif (not isActor and (val['id'] == '/film/actor' or val['id'] == 'tv/tv_actor')):
					isActor = True
					actor = []
					if ('/film/actor/film' in properties):
						for film in properties['/film/actor/film']['values']:
							f = defaultdict(list)
							if ('/film/performance/character' in film['property']):
								for val in film['property']['/film/performance/character']['values']:
									f['character'].append(val['text'])
							if ('/film/performance/film') in film['property']:
								for val in film['property']['/film/performance/film']['values']:
									f['film'].append(val['text'])
							actor.append(f)
					infobox['actor'] = actor

				# Check if search result is a BusinessPerson
				elif (not isBusinessPerson and (val['id'] == '/organization/organization_founder' or val['id'] == '/business/board_member')):
					isBusinessPerson = True
					bp = defaultdict(list)
					bp['founded'] = setDictVals(bp['founded'], properties, '/organization/organization_founder/organizations_founded')
					# handle board member
					if ('/business/board_member/organization_board_memberships' in properties):
						for org in properties['/business/board_member/organization_board_memberships']['values']:
							a = defaultdict(str)
							if ('/organization/organization_board_membership/organization' in org['property']):
								a['organization'] = org['property']['/organization/organization_board_membership/organization']['values'][0]['text']
							if ('/organization/organization_board_membership/title' in org ['property']):
								a['title'] = org['property']['/organization/organization_board_membership/title']['values'][0]['text']
							if ('/organization/organization_board_membership/role' in org['property']):
								a['role'] = org['property']['/organization/organization_board_membership/role']['values'][0]['text']
							if ('/organization/organization_board_membership/from' in org['property']):
								a['from'] = org['property']['/organization/organization_board_membership/from']['values'][0]['text']
							if ('/organization/organization_board_membership/to' in org['property']):
								a['to'] = org['property']['/organization/organization_board_membership/to']['values'][0]['text']
							bp['boardmember'].append(a)
					# handle leadership
					if ('/business/board_member/leader_of' in properties):
						for org in properties['/business/board_member/leader_of']['values']:
							a = defaultdict(str)
							if ('/organization/leadership/organization' in org['property']):
								a['organization'] = org['property']['/organization/leadership/organization']['values'][0]['text']
							if ('/organization/leadership/title' in org ['property']):
								a['title'] = org['property']['/organization/leadership/title']['values'][0]['text']
							if ('/organization/leadership/role' in org['property']):
								a['role'] = org['property']['/organization/leadership/role']['values'][0]['text']
							if ('/organization/leadership/from' in org['property']):
								a['from'] = org['property']['/organization/leadership/from']['values'][0]['text']
							if ('/organization/leadership/to' in org['property']):
								a['to'] = org['property']['/organization/leadership/to']['values'][0]['text']
							bp['leadership'].append(a)
					infobox['businessperson'] = bp

				# Check if search result is a League
				elif (val['id'] == '/sports/sports_league'):
					isLeague = True
					league = defaultdict(list)
					league['name'] = setDictVals(league['name'], properties, '/type/object/name')
					league['championship'] = setDictVals(league['championship'], properties, '/sports/sports_league/championship')
					league['sport'] = setDictVals(league['sport'], properties, '/sports/sports_league/sport')
					league['slogan'] = setDictVals(league['slogan'], properties, '/organization/organization/slogan')
					league['website'] = setDictVals(league['website'], properties, '/common/topic/official_website')
					if ('/common/topic/description' in properties):
						for x in properties['/common/topic/description']['values']:
							league['description'].append(x['value'])
					if ('/sports/sports_league/teams' in properties):
						for team in properties['/sports/sports_league/teams']['values']:
							if ('/sports/sports_league_participation/team' in team['property']):
								league['teams'].append(team['property']['/sports/sports_league_participation/team']['values'][0]['text'])
					infobox['league'] = league

				# Check if search result is a SportsTeam
				elif (not isSportsTeam and (val['id'] == '/sports/sports_team' or val['id'] == '/sports/professional_sports_team')):
					isSportsTeam = True
					team = defaultdict(list)
					team['name'] = setDictVals(team['name'], properties, '/type/object/name')
					if ('/common/topic/description' in properties):
						for x in properties['/common/topic/description']['values']:
							team['description'].append(x['value'])
					team['sport'] = setDictVals(team['sport'], properties, '/sports/sports_team/sport')
					team['arena'] = setDictVals(team['arena'], properties, '/sports/sports_team/arena_stadium')
					team['championships'] = setDictVals(team['championships'], properties, '/sports/sports_team/championships')
					if ('/sports/sports_team/coaches' in properties):
						for coach in properties['/sports/sports_team/coaches']['values']:
							c = defaultdict(list)
							if ('/sports/sports_team_coach_tenure/coach' in coach['property']):
								for val in coach['property']['/sports/sports_team_coach_tenure/coach']['values']:
									c['name'].append(val['text'])
							if ('/sports/sports_team_coach_tenure/from' in coach['property']):
								for val in coach['property']['/sports/sports_team_coach_tenure/from']['values']:
									c['from'].append(val['text'])
							if ('/sports/sports_team_coach_tenure/to'	in coach['property']):
								for val in coach['property']['/sports/sports_team_coach_tenure/to']['values']:
									c['to'].append(val['text'])
							if ('/sports/sports_team_coach_tenure/position'	in coach['property']):
								for val in coach['property']['/sports/sports_team_coach_tenure/position']['values']:
									c['position'].append(val['text'])
							team['coaches'].append(c)
					team['founded'] = setDictVals(team['founded'], properties, '/sports/sports_team/founded')
					if ('/sports/sports_team/league' in properties):
						for league in properties['/sports/sports_team/league']['values']:
							if ('/sports/sports_league_participation/league' in league['property']):
								team['leagues'].append(league['property']['/sports/sports_league_participation/league']['values'][0]['text'])
					team['locations'] = setDictVals(team['locations'], properties, '/sports/sports_team/location')
					if ('/sports/sports_team/roster' in properties):
						for player in properties['/sports/sports_team/roster']['values']:
							c = defaultdict(list)
							if ('/sports/sports_team_roster/player' in player['property']):
								for val in player['property']['/sports/sports_team_roster/player']['values']:
									c['name'].append(val['text'])
							if ('/sports/sports_team_roster/number' in player['property']):
								for val in player['property']['/sports/sports_team_roster/number']['values']:
									c['number'].append(val['text'])
							if ('/sports/sports_team_roster/from' in player['property']):
								for val in player['property']['/sports/sports_team_roster/from']['values']:
									c['from'].append(val['text'])
							if ('/sports/sports_team_roster/to'	in player['property']):
								for val in player['property']['/sports/sports_team_roster/to']['values']:
									c['to'].append(val['text'])
							if ('/sports/sports_team_roster/position'	in player['property']):
								for val in player['property']['/sports/sports_team_roster/position']['values']:
									c['position'].append(val['text'])
							team['players'].append(c)
					infobox['team'] = team

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
					nameString += 'BUSINESS)'

			print nameString.ljust(122) + ' |'

			# Print Person Attributes
			person = infobox['person']
			if (person['name']):
				newRow('Name', person['name'])
			if (person['birthday']):
				newRow('Birthday', person['birthday'])
			if (person['deathdate'] or person['deathplace'] or person['deathcause']):
				if (person['deathdate']):
					newRow('Date of death', person['deathdate'])
				if (person['deathplace']):
					newRow('Place of death', person['deathplace'])
				if (person['deathcause']):
					newRow('Causes of death', person['deathcause'])
			if (person['birthplace']):
				newRow('Place of birth', person['birthplace'])
			if (person['description']):
				newRow('Description', person['description'])
			if (person['siblings']):
				newRow('Siblings', person['siblings'])
			if (person['spouses']):
				newRow('Spouses', person['spouses'])

			# Print Actor Attributes
			if (isActor):
				if infobox['actor']:
					data = []
					for film in infobox['actor']:
						movie_names = ''
						for film_name in film['film']:
							if movie_names == '':
								movie_names += film_name
							else:
								movie_names += ', ' + film_name
						movie_names = ' | ' + movie_names
						element = movie_names
						for character in film['character']:
							if element == movie_names:
								element = character + element
							else:
								element = character + ', ' + element
						data.append(element)
					newRow('Films (Character | Film Name)', data)

			# Print Author Attributes
			if (isAuthor):
				author = infobox['author']
				if (author['books']):
					newRow('Books', author['books'])
				if (author['influencedby']):
					newRow('Influenced by', author['influencedby'])
				if (author['booksonauth']):
					newRow('Books about', author['booksonauth'])
				if (author['influenced']):
					newRow('Influenced', author['influenced'])

			# Print BusinessPerson Attributes
			if (isBusinessPerson):
				bp = infobox['businessperson']
				if (bp['founded']):
					newRow('Founded', bp['founded'])
				if (bp['leadership']):
					data = []
					for org in bp['leadership']:
						element = ""
						if org['organization']:
							element = element + org['organization'] + '|'
						if org['role']:
								element = element + org['role'] + '|'
						if org['title']:
							element = element + org['title'] + '|'
						if org['from']:
							element = element + org['from'] + '-'
						if org['to']:
							element = element + org['to'] + '|'
						data.append(element)
					newRow('Leadership: | Organization | Role | Title | From-To |', data)
				if (bp['boardmember']):
					data = []
					for org in bp['boardmember']:
						element = ""
						if org['organization']:
							element = element + org['organization'] + '|'
						if org['role']:
							element = element + org['role'] + '|'
						if org['title']:
							element = element + org['title'] + '|'
						if org['from']:
							element = element + org['from'] + '-'
						if org['to']:
							element = element + org['to'] + '|'
						data.append(element)
					newRow('Board Member: | Organization | Role | Title | From-To |', data)
			print '| ' + ('-' * 120) + ' |\n\n'

		# Print League Attributes
		elif isLeague:
			league = infobox['league']
			if (league['name']):
				print '  ' + ('-' * 120)
				temp = '| ' + league['name'][0] + '(LEAGUE)'
				print temp.ljust(122) + ' |'
				newRow('Name', league['name'])
			if (league['sport']):
				newRow('Sport', league['sport'])
			if league['slogan']:
				newRow('Slogan', league['slogan'])
			if league['website']:
				newRow('Official website', league['website'])
			if league['championship']:
				newRow('Championship', league['championship'])
			if league['teams']:
				newRow('Teams', league['teams'])
			if league['description']:
				newRow('Description', league['description'])
			print '| ' + ('-' * 120) + ' |\n\n'

		# Print SportsTeam Attributes
		elif isSportsTeam:
			team = infobox['team']
			if team['name']:
				print '  ' + ('-' * 120)
				temp = '| ' + team['name'][0] + '(SPORTS TEAM)'
				print temp.ljust(122) + ' |'
				newRow('Name', team['name'])
			if team['sport']:
				newRow('Sport', team['sport'])
			if team['arena']:
				newRow('Arena', team['arena'])
			if team['championships']:
				newRow('Championships', team['championships'])
			if team['founded']:
				newRow('Founded', team['founded'])
			if team['leagues']:
				newRow('Leagues', team['leagues'])
			if team['coaches']:
				data = []
				for coach in team['coaches']:
					element = ""
					if coach['name']:
						for name in coach['name']:
						 element = element + name + '|'
					if coach['position']:
						for position in coach['position']:
							element = element + position + '|'
					if coach['from']:
						for date in coach['from']:
							element = element + date + '-'
					if coach['to']:
						for date in coach['to']:
							element = element + date + '|'
					data.append(element)
				newRow('Coaches: | Name | Position | From/To |', data)
			if team['players']:
				data = []
				for player in team['players']:
					element = ""
					if player['name']:
						for name in player['name']:
						 element = element + name + '|'
					if player['position']:
						for position in player['position']:
							element = element + position + '|'
					if player['number']:
						for number in player['number']:
							element = element + number + '|'
					if player['from']:
						for date in player['from']:
							element = element + date + '-'
					if player['to']:
						for date in player['to']:
							element = element + date + '|'
					data.append(element)
				newRow('PlayersRoster: | Name | Position | Number | From/To |', data)
			if team['description']:
				newRow('Description', team['description'])
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

		# Modify query for API
		query = question[12:]
		if query[-1] == '?':
			query = query[:-1]

		search_url = "https://www.googleapis.com/freebase/v1/mqlread"
		
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
		
		bookUrl = search_url + '?' + urllib.urlencode(bookParams)
		orgUrl = search_url + '?' + urllib.urlencode(orgParams)
		bookResponse = json.loads(urllib.urlopen(bookUrl).read())
		orgResponse = json.loads(urllib.urlopen(orgUrl).read())
		bookResults = []
		orgResults = []
		if 'result' in bookResponse:
			bookResults = bookResponse['result']
		if 'result' in orgResponse:
			orgResults = orgResponse['result']

		creators = {}

		for item in bookResults:
			if '/book/author/works_written' in item:
				bookList = []
				for book in item['/book/author/works_written']:
					if 'a:name' in book:
						bookList.append(book['a:name'])
				if item['name'] in creators:
					creators[item['name']].append(('Author', bookList))
				else:
					creators[item['name']] = []
					creators[item['name']].append(('Author', bookList))


		for item in orgResults:
			if '/organization/organization_founder/organizations_founded' in item:
				orgList = []
				for org in item['/organization/organization_founder/organizations_founded']:
					if 'a:name' in org:
						orgList.append(org['a:name'])
				if item['name'] in creators:
					creators[item['name']].append(('Business Person', orgList))
				else:
					creators[item['name']] = []
					creators[item['name']].append(('Business Person', orgList))

		

		print '  ' + ('-' * 120)
		temp = '| ' + question
		print temp.ljust(122) + ' |' 

		creators = collections.OrderedDict(sorted(creators.items()))

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



