#Program Takes in Car data from Automobile Catalog
#Does not take in model variants (i.e. hardtop, coupe, convertible, etc.) because of bot protections on the site

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from collections import namedtuple
import Maker
import random

#Array used for bot
modelDB = []
modelStruct = namedtuple("modelStruct", "Maker Name Date Image Description")

#Opens "Model.txt"
file = open("Model.txt", "r")
lines = file.readlines()

#Reads from file into array
for line in lines:
	maker = line.split('\t')[0]
	name = line.split('\t')[1]
	date = line.split('\t')[2]
	image = line.split('\t')[3]
	description = line.split('\t')[4]

	#Creates struct and adds it to array
	new = modelStruct(maker, name, date, image, description)
	modelDB.append(new)

#Close file
file.close()

#Function to update Model.txt (Do not use regularly)
def updateModels():
	#File to copy down models from database
	file = open("Model.txt", "w")

	#Used to check dupes
	removeDupes = []

	#If the scraped data already exists in the list
	def isDupe(struct):
		for model in removeDupes:
			if struct.Maker == model.Maker and struct.Name == model.Name and struct.Date == model.Date and struct.Image == model.Image:
				return True
		return False

	#Opens main database webpage
	hdr = {'User-Agent': 'Mozilla/5.0'}
	request = Request('https://www.automobile-catalog.com/browse.php', headers = hdr)
	client = urlopen(request)
	rawPage = client.read()
	client.close()

	#Parses database home into readable html
	readIt = BeautifulSoup(rawPage, "html.parser")

	#Cell where brand links are found
	brandList = readIt.findAll("td", {"width": "160"})

	#Iterates through all brand cells
	for i in range(len(brandList)):
		#Finds brand link
		cellLink = brandList[i].p.b.a["href"]

		#Finds brand name
		brand = brandList[i].p.b.a.font.findAll(text = True, recursive = False)

		#Opens brand link
		request2 = Request(f'https://www.automobile-catalog.com/{cellLink}', headers = hdr)
		client = urlopen(request2)
		rawPage2 = client.read()
		client.close()
		
		#Parses brand page into readable html
		readIt2 = BeautifulSoup(rawPage2, "html.parser")

		#Cell where model links are found
		modelList= readIt2.findAll("td", {"width": "320"}, {"height": "250"})

		#Iterates through all the model cells
		for j in range(len(modelList)):
			#Finds space for model name and date
			modelSeriesNameBox = modelList[j].find("p", {"style": "font-size: 13pt;monospace"})
			nameDate = modelSeriesNameBox.a.font.b.findAll(text = True, recursive = False)

			#Finds model name
			modelSeriesName = nameDate[0]

			#Finds model dates
			modelSeriesDate = nameDate[1]

			#Finds model image src, if applicable
			if modelList[j].find("td", {"width": "100%"}) != None:
				modelSeriesPic = modelList[j].find("td", {"width": "100%"}).center.a.img["src"]
			else:
				modelSeriesPic = "No pic"

			#Finds model description, if applicable
			if modelList[j].find("p", {"style": "font-size: 11pt;monospace"}) != None:
				modelSeriesDescrBox = modelList[j].find("p", {"style": "font-size: 11pt;monospace"})
				modelSeriesDescr = modelSeriesDescrBox.font.b.findAll(text = True, recursive = False)[0]
			else:
				modelSeriesDescr = "No description"

			#Struct created to check for dupes
			m = modelStruct(brand, modelSeriesName, modelSeriesDate, modelSeriesPic, modelSeriesDescr)

			#If the model scraped is a new model not scraped already
			if isDupe(m) == False:
				removeDupes.append(m)

				#Writes info into file
				file.write(brand[0] + "\t" + modelSeriesName + "\t" + modelSeriesDate + "\t" + modelSeriesPic + "\t" + modelSeriesDescr + '\n')

			#MODEL LINKS CAN BE FOUND IN "ModelLinks.txt"

			#Finds model link
			#modelLink = modelList[j].p.a["href"]
			#file.write(f"https://www.automobile-catalog.com{modelLink}\n")

	#CODE BELOW WILL NOT WORK BECAUSE THE SITE HAS BOT PROTECTIONS!!!

			#Opens model link
	#		request3 = Request(f'https://www.automobile-catalog.com{modelLink}', headers = hdr)
	#		client = urlopen(request3)
	#		rawPage3 = client.read()
	#		client.close()

			#Parses model page into readable html
	#		readit3 = BeautifulSoup(rawPage3, "html.parser")

			#Cell where model info is found
	#		modelBox = readit3.findAll("table", {"valign": "top"}, {"border": "0"})

			#Finds the model name and picture link
	#		for m in range(len(modelBox)):
	#			modelName = modelBox[m].tbody.tr.td.p.font.b

				#Process to find img link
	#			modelPicBox = modelBox.find("img")
	#			modelPic = modelPicBox["src"]

				#Statement to make sure link of an in progress page isnt used
	#			if modelPic == "/photo_coming_soon_2.png":
	#				file.write(modelName + " NoPic\n")
	#			else:
	#				file.write(modelName + " " + modelPic + '\n')

	#Closes file
	file.close()

#Finds and returns a random car
def randomCar():
	index = random.randint(0, len(modelDB) - 1)
	return modelDB[index]


	
	
