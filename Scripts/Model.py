from bs4 import BeautifulSoup
from urllib.request import urlopen
import wikipedia
import Maker

def getRandomCar():
	brand = Maker.randomManufacturer()
	link = brand.Name
	page = wikipedia.page(link)
	overview = page.sections
	if overview.size == 0:
		
getRandomCar()
