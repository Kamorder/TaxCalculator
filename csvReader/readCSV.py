import csv
import os
from csvClass import csvRow

resourcePath = os.getcwd() + "/resources"

def collateDocuments():
    entryList = []
    for _,_,files in os.walk(resourcePath):
        for name in files:
            openCSVandAddRows(name,entryList)
    return entryList

def openCSVandAddRows(fileName, entryList):
    file = resourcePath + "/" + fileName
    with open(file) as csvFile:
        openedCSV = csv.reader(csvFile)
        next(openedCSV)
        for line in openedCSV:
            entryList.append(getCSVType(line,fileName))

def getCSVType(infoList, fileName):
    card = fileName.split("_")[0]
    date = infoList[0]
    description = infoList[2]
    cost = abs(float(infoList[5]))
    
    return csvRow(card,date,description,cost)
    
if __name__ == "__main__":
    print(collateDocuments())