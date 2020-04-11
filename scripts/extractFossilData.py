import requests
import string
import json
import re
from bs4 import BeautifulSoup

fossilsUrl = 'https://animalcrossing.fandom.com/wiki/Fossils_(New_Horizons)'


# Get fossil data
# BS4, get all bug rows
page = requests.get(fossilsUrl)
soup = BeautifulSoup(page.content, 'html.parser')
fossilTables = soup.find_all("table", class_="sortable")

# Two classifcations of fossils
standaloneFossilRows = fossilTables[0].find_all('tr')[1:15]
multiPartFossilRows = fossilTables[1].find_all('tr')[1:82]

# Collect lists of fossils
standaloneFossils = []
for fossilRow in standaloneFossilRows:
	fossil = {}
	fossilCols = fossilRow.find_all('td')
	fossil['name'] = string.capwords(fossilCols[0].a.get_text())
	fossil['imageUrl'] = fossilCols[1].find_all('a')[0]['href']
	fossil['price'] = int(re.sub('[^0-9]', '', fossilCols[2].string))

	# Download image
	fossilFileName = fossil['name'].replace(" ", "_")
	img_data = requests.get(fossil['imageUrl']).content
	with open("../assets/fossils/" + fossilFileName + ".png", 'wb') as handler:
		handler.write(img_data)

	standaloneFossils.append(fossil)

dinosaurName = ""
multiPartFossils = []
i = 0
j = 0
for fossilRow in multiPartFossilRows:
	fossilCols = fossilRow.find_all('td')
	
	if len(fossilCols) == 0:
		dinosaurName = fossilRow.find_all('a')[0].string
		fossil = {}
		fossil['name'] = dinosaurName
		fossil['pieces'] = []
		multiPartFossils.append(fossil)
	elif len(fossilCols) == 3:
		fossilPiece = {}
		fossilPiece['name'] = string.capwords(fossilCols[0].find_all('a')[0].get_text())
		fossilPiece['imageUrl'] = fossilCols[1].find_all('a')[0]['href']
		fossilPiece['price'] = int(re.sub('[^0-9]', '', fossilCols[2].string))

		# Download image
		fossilFileName = fossilPiece['name'].replace(" ", "_")
		img_data = requests.get(fossilPiece['imageUrl']).content
		with open("../assets/fossils/" + fossilFileName + ".png", 'wb') as handler:
			handler.write(img_data)

		i += 1
		if i == 4:
			j += 1
			i = 0
		multiPartFossils[j]['pieces'].append(fossilPiece)
		
# Sort results alphabetically
standaloneFossils = sorted(standaloneFossils, key=lambda x: x['name'])
multiPartFossils = sorted(multiPartFossils, key=lambda x: x['name'])

results = { 'standaloneFossils' : standaloneFossils, 'multiPartFossils' : multiPartFossils }

# Pretty format JSON
prettyJson = json.dumps(results, indent=4)

# Write JSON to file
with open("../data/fossils.json", 'w') as fp:
	fp.write(prettyJson)
	fp.close()