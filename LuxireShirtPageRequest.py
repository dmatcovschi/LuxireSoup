import re
import csv
import requests
from bs4 import BeautifulSoup



def findWeave(description):
	iteamWeave = "Unkown"
	find_result = re.findall("poplin|oxford|twill|chambray|end-on-end|seersucker|linen", description.lower())
	if not find_result:
		itemWeave = "Unknown"
	else:
		for result in find_result:
			itemWeave = result
	return itemWeave



itemDescriptions = []
itemOneDescription = []

r = requests.get("http://custom.luxire.com/collections/dress-shirts/products/white-with-blue-black-checks")
soup = BeautifulSoup(r.content)

itemDescription = soup.find("div", {"class":"yotpo yotpo-main-widget"})
itemEachDescription = soup.find("div", {"class":"proCntnt"}).ul
itemEachTitle = soup.find("div", {"class":"proCntnt"}).h1.string

print itemEachDescription
print "ok ok"

if itemEachDescription == None:
	print "is none"
	
for descriptionLineItem in itemEachDescription.stripped_strings:
	itemOneDescription.append(descriptionLineItem)
itemOneDescription.append(itemEachTitle)
itemDescriptions.append(itemOneDescription)

for item in itemDescriptions:
	itemDescriptionString =  " ".join(item)
	#print itemDescriptionString
	findWeave(itemDescriptionString)	

