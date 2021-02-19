#Script scrapes entire list of car manufacturers from Wikipedia
#This list and the list of models do not necessarily match up

from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import namedtuple
import random
import io

#Struct definition
makerStruct = namedtuple("makerStruct", "Name WikiLink")

#Open Maker.txt file
file = open("Maker.txt", "r", encoding = "utf-8")
lines = file.readlines()

#Array to be used for functions
theList = []

#Reads from file
for line in lines:
	name = line.split('\t')[0]
	link = line.split('\t')[1]
	m = makerStruct(name, link)
	theList.append(m)

#Closes file
file.close()	

#Will update the Maker.txt file
def scrapeMaker():
	#Organizational stuff to be used
	organizedList = []

	#File written for archival purposes
	file = open("Maker.txt", "w", encoding = "utf-8")

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

	#Writes list to Maker.txt
	for j in range(len(organizedList)):
		file.write(organizedList[j].Name + "\t" + organizedList[j].WikiLink + '\n')

	#Closes file
	file.close()

#Returns the list
def allManufacturers():
	return theList

#Returns a random manufacturer
def randomManufacturer():
	index = random.randint(0, len(theList) - 1)
	return theList[index]

