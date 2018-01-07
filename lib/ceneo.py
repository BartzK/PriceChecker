class Ceneo:
    parser = "html.parser"
    ceneoAddress = "https://www.ceneo.pl"
    maxStringLength = 150

    categoryHtmlClassName = "cat-prod-row js_category-list-item js_man-track-event "
    dataHtmlClassName = "category-list-name sibling-title"
    

    print("Trwa przeszukiwanie produktów...\n")

    for productString in searchList:
        htmlCodeString = requests.get(ceneoAddress + "/" + productString[0] + \
                                      ";szukaj-" + productString[1]).text
        htmlObject = BeautifulSoup(htmlCodeString, parser)
        
        productList =  htmlObject.find_all(class_=categoryHtmlClassName)

        AppendFile(outputFilename, str(productString[1].title().center(maxStringLength)))

        h1Tags = htmlObject.find(class_=dataHtmlClassName)
        if h1Tags.find(class_="section-title section-title--oneline").string == productString[1].replace("_", " "):
            for product in productList:
                productName = product.find(class_="cat-prod-row-name").find(class_=" js_conv").string
                productPrice = product.find(class_="cat-prod-row-price").find(class_="value").string + product.find(class_="cat-prod-row-price").find(class_="penny").string
                productAddress = product.find(class_="cat-prod-row-price").a.get("href")
                if not productName in blackList:
                    AppendFile(outputFilename, str(productName + ':' + productPrice.rjust(maxStringLength-len(productName)-1)))
                    AppendFile(outputCsvFilename, str(productName + ';' + productPrice.rjust(maxStringLength-len(productName)-1) + ";" + ceneoAddress + productAddress + "; "))
        AppendFile(outputFilename, str(CharRange('_', maxStringLength)))

