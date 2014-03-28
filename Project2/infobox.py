import sys
import json
import urllib
from collections import defaultdict		# to initialize dictionary values to 0

# Function to avoid code duplication
def setDictVals(ourList, properties, path):
	if (path in properties):
		for x in properties[path]['values']:
			ourList.append(x['text'])
		return ourList

api_key = 'AIzaSyBsXEX0SMoWRYtQDRHWMHehGqmRiGRgQow'
# test query
query = raw_input("Query: ")
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
			actor = defaultdict(str)
			if ('/film/actor/film' in properties):
				# map film to character
				for film in properties['/film/actor/film']['values']:
					actor[film['property']['/film/performance/film']['values'][0]['text']] = film['property']['/film/performance/character']['values'][0]['text']
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
	print infobox['person']['name'][0],
	if (isAuthor or isActor or isBusinessPerson):
		sys.stdout.write('(')
		if (isAuthor):
			sys.stdout.write('AUTHOR')
			if (isActor or isBusinessPerson):
				print ',',
			else:
				print ')'
		if (isActor):
			sys.stdout.write('ACTOR')
			if (isBusinessPerson):
				print ',',
			else:
				print ')'
		if (isBusinessPerson):
			print 'BUSINESS)'

	# Print Person Attributes
	person = infobox['person']
	if (person['name']):
		print 'Name:',
		for name in person['name']:
			print name
	if (person['birthday']):
		print 'Birthday:',
		for date in person['birthday']:
			print date
	if (person['deathdate'] or person['deathplace'] or person['deathcause']):
		print 'Death:',
		if (person['deathdate']):
			for deathdate in person['deathdate']:
				print deathdate,
		if (person['deathplace']):
			print "at",
			for deathplace in person['deathplace']:
				print deathplace + ", ",
		if (person['deathcause']):
			sys.stdout.write('cause: (')
			for deathcause in xrange(len(person['deathcause'])):
				sys.stdout.write(person['deathcause'][dc])
				if (deathcause < len(person['deathcause'])-1):
					print ', ',
				else:
					print ')',
		print 
	if (person['birthplace']):
		print 'Place of birth:',
		for place in person['birthplace']:
			print place
	if (person['description']):
		print 'Descriptions:',
		for description in person['description']:
			print description
	if (person['siblings']):
		print 'Siblings:',
		for sibling in person['siblings']:
			print sibling
	if (person['spouses']):
		print 'Spouses:',
		for spouse in person['spouses']:
			print spouse

	# Print Actor Attributes
	if (isActor):
		if infobox['actor']:
			print 'Films: Character | Film Name'
			for film in infobox['actor']:
				print infobox['actor'][film] + ' | ' + film

	# Print Author Attributes
	if (isAuthor):
		author = infobox['author']
		if (author['books']):
			print 'Books:',
			for book in author['books']:
				print book
		if (author['influencedby']):
			print 'Influenced By:',
			for auth in author['influencedby']:
				print auth
		if (author['booksonauth']):
			print 'Books About:',
			for book in author['booksonauth']:
				print book
		if (author['influenced']):
			print 'Influenced:',
			for influenced in author['influenced']:
				print influenced

	# Print BusinessPerson Attributes
	if (isBusinessPerson):
		bp = infobox['businessperson']
		if (bp['founded']):
			print 'Founded:',
			for org in bp['founded']:
				print org
		if (bp['leadership']):
			print 'Leadership: | Organization | Role | Title | From-To |'
			for org in bp['leadership']:
				print '|',
				if org['organization']:
					print org['organization'],
				print '|',
				if org['role']:
					print org['role'],
				print '|',
				if org['title']:
					print org['title'],
				sys.stdout.write('| (')
				if org['from']:
					print org['from'],
				print '/',
				if org['to']:
					print org['to'],
				print ') |'
		if (bp['boardmember']):
			print 'Board Member: | Organization | Role | Title | From-To |'
			for org in bp['boardmember']:
				print '|',
				if org['organization']:
					print org['organization'],
				print '|',
				if org['role']:
					print org['role'],
				print '|',
				if org['title']:
					print org['title'],
				sys.stdout.write(' | (')
				if org['from']:
					print org['from'],
				print '/',
				if org['to']:
					print org['to'],
				sys.stdout.write(') |\n')

# Print League Attributes
elif isLeague:
	league = infobox['league']
	if (league['name']):
		print league['name'][0] + '(LEAGUE)'
		print 'Name:',
		for name in league['name']:
			print name
	if (league['sport']):
		print 'Sport:',
		for sport in league['sport']:
			print sport
	if league['slogan']:
		print 'Slogan:',
		for slogan in league['slogan']:
			print slogan
	if league['website']:
		print 'Official Website:',
		for website in league['website']:
			print website
	if league['championship']:
		print 'Championship:',
		for championship in league['championship']:
			print championship
	if league['teams']:
		print 'Teams:',
		for team in league['teams']:
			print team
	if league['description']:
		print 'Description:',
		for description in league['description']:
			print description

# Print SportsTeam Attributes
elif isSportsTeam:
	team = infobox['team']
	if team['name']:
		print team['name'][0] + '(SPORTS TEAM)'
		print 'Name:',
		for name in team['name']:
			print name
	if team['sport']:
		print 'Sport:',
		for sport in team['sport']:
			print sport
	if team['arena']:
		print 'Arena:',
		for arena in team['arena']:
			print arena
	if team['championships']:
		print 'Championships:',
		for championship in team['championships']:
			print championship
	if team['founded']:
		print 'Founded:',
		for date in team['founded']:
			print date
	if team['leagues']:
		print 'Leagues:',
		for league in team['leagues']:
			print league
	if team['coaches']:
		print 'Coaches: | Name | Position | From/To |'
		for coach in team['coaches']:
			print '|',
			if coach['name']:
				for name in coach['name']:
				 print name,
			print '|',
			if coach['position']:
				for position in coach['position']:
					print position,
			sys.stdout.write(' | (')
			if coach['from']:
				for date in coach['from']:
					print date,
			sys.stdout.write('/')
			if coach['to']:
				for date in coach['to']:
					print date,
			sys.stdout.write(') |\n')
	if team['players']:
		print 'PlayersRoster: | Name | Position | Number | From/To |'
		for player in team['players']:
			print '|',
			if player['name']:
				for name in player['name']:
				 print name,
			print '|',
			if player['position']:
				for position in player['position']:
					print position,
			print '|',
			if player['number']:
				for number in player['number']:
					print number,
			sys.stdout.write(' | (')
			if player['from']:
				for date in player['from']:
					print date,
			sys.stdout.write('/')
			if player['to']:
				for date in player['to']:
					print date,
			sys.stdout.write(') |\n')
	if team['description']:
		print 'Description:',
		for description in team['description']:
			print description


