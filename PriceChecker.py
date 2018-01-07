###############################################
#                Price Checker                #
# Checks ceneo.pl for price of given products #
# then stores them in a table with historical #
# values.                                     #
#                                   by BartzK #
###############################################

import sys
import requests
import re
import datetime
import importlib
##importlib.import_module("lib/ceneo.py")
##importlib.import_module("lib/literals.py")

from bs4 import BeautifulSoup

def CharRange(character, number):
	string = ""
	for i in range(number):
		string = string + character
	return string

def ReadFile(filename):
	with open(filename, "r") as searchedFile:
		content = searchedFile.readlines()
		content = [x.strip() for x in content]
		content = [x.split(";") for x in content]
	return content

def AppendFile(filename, stringValue):
	with open(filename, "a") as output_file:
		output_file.write(stringValue + "\n")

def Main(args):
        # literals
        parser = "html.parser"
        ceneoAddress = "https://www.ceneo.pl"
        maxStringLength = 150

        searchListFilename = "tests/input/searchList.txt"
        blackListFilename = "tests/input/blackList.txt"
        outputFilename = "tests/output/outputData.txt"
        csvFilename = "tests/output/outputData.csv"

        csvHeaders ="Name;Price;Hyperlink;"
        csvSeparator = ";"

        ceneoCategoryName = "section-title section-title--oneline"
        ceneoProductContainer = "cat-prod-row js_category-list-item js_man-track-event "
        ceneoProductName = " js_conv"
        ceneoProductPrice = "value"
        ceneoProductResidue = "penny"

        htmlHyperlink = "href"

        # read user data from file 
        searchList = ReadFile(searchListFilename)
        blackList = ReadFile(blackListFilename)

        open(outputFilename, 'w').close()
        open(csvFilename, 'w').close()

        AppendFile(csvFilename, csvHeaders)

        # TITLE
        print("Trwa przeszukiwanie produktów...\n")

        for productString in searchList:
                htmlCodeString = requests.get(ceneoAddress + "/" + productString[0] + ";szukaj-" + productString[1]).text
                htmlObject = BeautifulSoup(htmlCodeString, parser)

                AppendFile(outputFilename, str(productString[1].title().center(maxStringLength)))

                if htmlObject.find(class_=ceneoCategoryName):
                        categoryName = htmlObject.find(class_=ceneoCategoryName).string.lower().lstrip().rstrip()
                        userCategoryName = productString[1].lower() + " - " + productString[0].replace("_", " ").lower()
                        if  categoryName == userCategoryName:
                                productList =  htmlObject.find_all(class_=ceneoProductContainer)
                                for product in productList:
                                        productName = product.find(class_=ceneoProductName).string
                                        productPrice = product.find(class_=ceneoProductPrice).string + \
                                                                   product.find(class_=ceneoProductResidue).string.replace(",", ".")
                                        productHyperlink = ceneoAddress + product.a.get(htmlHyperlink)
                                        #if not productName in blackList[0]:
                                        if not any(s in productName for s in blackList[0]):
                                                AppendFile(outputFilename, str(productName + productPrice.rjust(maxStringLength-len(productName)-1)))
                                                AppendFile(csvFilename, str(productName + csvSeparator + productPrice))# + csvSeparator + productHyperlink))
                AppendFile(outputFilename, str(CharRange('_', maxStringLength)))

if __name__ == "__main__":Main(sys.argv[1:])
