from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import namedtuple
import random

organizedList = []
makerStruct = namedtuple("makerStruct", "Name WikiLink")

#Processes the page
client = urlopen('https://en.wikipedia.org/wiki/List_of_automobile_manufacturers')
rawPage = client.read()
client.close()

#Parses the webpage
readablePage = BeautifulSoup(rawPage, "html.parser")

#Finds all the non-defunct manufacturer lists by country
fullList = readablePage.findAll("div", {"class": "div-col"})

#Adds each manufacturer to the list
for i in range(len(fullList)):
	list = fullList[i].ul.findAll("li")
	for j in range(len(list)):
		manufacturer = list[j].a["title"]
		wiki = list[j].a["href"]
		m = makerStruct(manufacturer, wiki)

		#Does not add manufacturers whose wiki page does not exist
		if manufacturer.find("page does not exist") == -1:
			isPresent = False

			#Checks if manufacturer already exists in list
			for k in organizedList:
				if (k == manufacturer):
					isPresent = True
					break

			if isPresent == False:
				organizedList.append(m)

#Sort Array
organizedList.sort()

#Returns the list
def allManufacturers():
	return organizedList

#Returns a random manufacturer
def randomManufacturer():
	index = random.randint(0, len(organizedList) - 1)
	return organizedList[index]
