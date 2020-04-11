import requests
import string
import json
from bs4 import BeautifulSoup

northernHemisphereFishUrl = 'https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)#Northern%20Hemisphere'
southerHemisphereFishUrl = 'https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)#Southern%20Hemisphere'
northernHemisphereBugsUrl = 'https://animalcrossing.fandom.com/wiki/Bugs_(New_Horizons)#Northern%20Hemisphere'
southernHemisphereBugsUrl = 'https://animalcrossing.fandom.com/wiki/Bugs_(New_Horizons)#Southern%20Hemisphere'
fossilsUrl = 'https://animalcrossing.fandom.com/wiki/Fossils_(New_Horizons)'

fishUrls = [ northernHemisphereFishUrl, southerHemisphereFishUrl ]
bugsUrls = [ northernHemisphereBugsUrl, southernHemisphereBugsUrl ]

def getCalendarAppearanceMap(cols, index):
	appearanceMap = {}
	for i in range(0, 12):
		appearanceMap[i + 1] = '-' not in cols[index + i].string
	return appearanceMap

for fishUrl in fishUrls:
	# Boolean, true if we're working on northern hemisphere
	isNorthernHemisphere = "Northern" in fishUrl

	# BS4, get all fish rows
	page = requests.get(fishUrl)
	soup = BeautifulSoup(page.content, 'html.parser')
	fishTable = soup.find_all("table", class_="roundy sortable")[0]
	fishRows = fishTable.find_all("tr")[1:81]

	# Collect list of fish objects
	results = []
	print("Processing " + str(len(fishRows)) + " fish...")
	for fishRow in fishRows:
		fishCols = fishRow.find_all("td")
		fish = {}
		fish['name']     = string.capwords(fishCols[0].a.get_text())
		fish['imageUrl']  = fishCols[1].find_all('img')[0]['data-src']
		fish['price']    = int(fishCols[2].string.strip())
		fish['location'] = fishCols[3].string.strip()
		fish['shadowSize'] = fishCols[4].string.strip()
		fish['timeOfDay'] = fishCols[5].small.string.strip()
		fish['calendarAppearance'] = getCalendarAppearanceMap(fishCols, 6)
		results.append(fish)

		# Download fish icon to assets folder
		fishImageFileName = fish['name'].replace(" ", "_")
		img_data = requests.get(fish['imageUrl']).content
		with open("../assets/fish/" + fishImageFileName + ".png", 'wb') as handler:
			handler.write(img_data)

	# Sort results alphabetically
	results = sorted(results, key=lambda x: x['name'])

	# Pretty format JSON
	prettyJson = json.dumps(results, indent=4)

	# Write JSON to file
	with open("../data/" + ("northern_hemisphere" if isNorthernHemisphere else "southern_hemisphere") + '_fish.json', 'w') as fp:
		fp.write(prettyJson)
		fp.close()

for bugUrl in bugsUrls:
	# Boolean, true if we're working on northern hemisphere
	isNorthernHemisphere = "Northern" in bugUrl

	# BS4, get all bug rows
	page = requests.get(bugUrl)
	soup = BeautifulSoup(page.content, 'html.parser')
	bugsTable = soup.find_all("table", class_="sortable")[0]
	bugRows = bugsTable.find_all("tr")[1:81]

	# Collect list of bug objects
	results = []
	print("Processing " + str(len(bugRows)) + " bugs...")
	for bugRow in bugRows:
		bugCols = bugRow.find_all("td")
		bug = {}
		bug['name']     = string.capwords(bugCols[0].a.get_text())
		bug['imageUrl']  = bugCols[1].find_all('img')[0]['data-src']
		bug['price']    = int(bugCols[2].string.strip())
		bug['location'] = bugCols[3].string.strip()
		bug['timeOfDay'] = bugCols[4].small.string.strip()
		bug['calendarAppearance'] = getCalendarAppearanceMap(bugCols, 5)
		results.append(bug)

		# Download bug icon to assets folder
		bugImageFileName = bug['name'].replace(" ", "_")
		img_data = requests.get(bug['imageUrl']).content
		with open("../assets/bugs/" + bugImageFileName + ".png", 'wb') as handler:
			handler.write(img_data)

	# Sort results alphabetically
	results = sorted(results, key=lambda x: x['name'])

	# Pretty format JSON
	prettyJson = json.dumps(results, indent=4)

	# Write JSON to file
	with open("../data/" + ("northern_hemisphere" if isNorthernHemisphere else "southern_hemisphere") + '_bugs.json', 'w') as fp:
		fp.write(prettyJson)
		fp.close()
