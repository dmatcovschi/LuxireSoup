import csv
import requests
import re
from bs4 import BeautifulSoup

def findWeave(description):
	iteamWeave = "Unkown"
	find_result = re.findall("poplin|oxford|twill|chambray|end-on-end|seersucker|linen|herringbone|end on end", description.lower())
	if not find_result:
		itemWeave = "Unknown"
	else:
		for result in find_result:
			itemWeave = result
	return itemWeave


def searchDescription(itemLink):
	itemDescriptions = []
	itemOneDescription = []

	r = requests.get(itemLink)
	soup = BeautifulSoup(r.content)

	itemEachDescription = soup.find("div", {"class":"proCntnt"}).ul
	itemEachTitle = soup.find("div", {"class":"proCntnt"}).h1.string

	if itemEachDescription == None:
		return None

	for descriptionLineItem in itemEachDescription.stripped_strings:
		itemOneDescription.append(descriptionLineItem)
	itemOneDescription.append(itemEachTitle)
	itemDescriptions.append(itemOneDescription)

	for item in itemDescriptions:
		itemDescriptionString =  " ".join(item)
		return findWeave(itemDescriptionString)	

shirtNameList = ["Shirt Name"]
shirtPriceList = ["Shirt Price"]
shirtOriginalPriceList = ["Original Shirt Price"]
shirtPromotionList = ["Promotion"]
shirtLinkList = ["Link"]
shirtWeaveList = ["Weave"]

pages = range(100)
counter = 0
for page in pages:
	
	r = requests.get("http://custom.luxire.com/collections/dress-shirts?page=" + str(page))
	soup = BeautifulSoup(r.content)
	shirtsCollection = soup.find_all("a", {"class" : "collectionImg"})
	
	if not shirtsCollection:
		break

	for shirtCollection in shirtsCollection:
		shirtLink = "http://custom.luxire.com" + str(shirtCollection.get("href"))
		shirt = shirtCollection.parent
		shirtName = shirt.contents[3].text.replace("\n"," ").strip()
		shirtPrice = shirt.find("span", {"class" : "price"}).find("span", {"class" : "money"}).contents[0].strip()
		shirtOriginalPriceCheck = shirt.find("span", {"class" : "strike"})

		if shirtOriginalPriceCheck == None:
			shirtOriginalPrice = shirtPrice
			shirtPromotion = False
		else:
			shirtOriginalPrice = shirtOriginalPriceCheck.find("span", {"class" : "money"}).contents[0].strip()
			shirtPromotion = True

		shirtWeave = searchDescription(shirtLink)
		print shirtWeave
		shirtNameList.append(shirtName)
		shirtPriceList.append(shirtPrice)
		shirtOriginalPriceList.append(shirtOriginalPrice)
		shirtPromotionList.append(shirtPromotion)
		shirtLinkList.append(shirtLink)
		shirtWeaveList.append(shirtWeave)

		counter +=1
		print counter

shirtAllInfoRows = zip(shirtNameList,shirtPriceList,shirtOriginalPriceList,shirtPromotionList,shirtLinkList,shirtWeaveList)

with open("LuxireShirt.csv","w") as csvfile:
	writer = csv.writer(csvfile,delimiter=",")
	for shirtAllInfoRow in shirtAllInfoRows:
		writer.writerow(shirtAllInfoRow)
