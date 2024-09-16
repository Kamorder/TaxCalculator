import csv
import os
import re
from .csvClass import csvRow, csvDebitRow

resourcePath = os.getcwd() + "/resources"

def collateDocuments() -> list:
    entryList = []
    for _,_,files in os.walk(resourcePath):
        for name in files:
            if name.lower().endswith(".csv"):
                openCSVandAddRows(name,entryList)
    return entryList

def openCSVandAddRows(fileName, entryList) -> None:
    file = resourcePath + "/" + fileName
    with open(file, mode='r') as csvFile:
        openedCSV = csv.reader(csvFile)
        firstLine = next(openedCSV)
        if firstLine[0].lower() == "details":
            for line in openedCSV:
                entryList.append(getCSVTypeDebit(line,fileName))
        else:
            for line in openedCSV:
                 entryList.append(getCSVType(line, fileName))

def getCSVType(infoList, fileName) -> csvRow:
    card = fileName.split("_")[0]
    date = infoList[0]
    description = infoList[2]
    parsed = parseDescription(infoList[2])
    cost = abs(float(infoList[5]))
    
    return csvRow(card,date,description,parsed,cost)

def getCSVTypeDebit(infoList, fileName) -> csvDebitRow:
    line = fileName.split("_")[0]
    date = infoList[1]
    description = infoList[2]
    parsed = parseDescription(infoList[2])
    cost = abs(float(infoList[3]))
    
    return csvDebitRow(line,date,description,parsed,cost)

def parseDescription(info) -> str:
    return re.sub(r'[^a-zA-Z]', '', info).upper()

