import csv
import os
import re
from .csvClass import csvRow, csvDebitRow


resourcePath = os.getcwd() + "/resources"

def collateDocuments(resource = None) -> list[csvRow | csvDebitRow]:
    '''Take all CSV documents and put them into the entry list'''
    entryList = []
    global resourcePath
    if resource is not None: 
        resourcePath = resource
    for _,_,files in os.walk(resourcePath):
        for name in files:
            if name.lower().endswith(".csv"):
                openCSVandAddRows(name,entryList)
    return entryList

def openCSVandAddRows(fileName : str, entryList : list[csvRow | csvDebitRow]) -> None:
    '''Reformat the lines in either the CSV DEBIT or CREDIT'''
    file = resourcePath/fileName
    with open(file, mode='r', encoding="utf-8-sig") as csvFile:
        openedCSV = csv.reader(csvFile)
        firstLine = next(openedCSV)
        if firstLine[0].strip().lower() == "details":
            for line in openedCSV:
                entryList.append(getCSVTypeDebit(line,fileName))
        else:
            for line in openedCSV:
                 entryList.append(getCSVType(line, fileName))

def getCSVType(infoList : list[str], fileName : str) -> csvRow:
    '''Parse lines into a csvRow'''
    card = fileName.split("_")[0]
    date = infoList[0]
    description = infoList[2]
    parsed = parseDescription(infoList[2])
    cost = abs(float(infoList[5]))
    
    return csvRow(card,date,description,parsed,cost)

def getCSVTypeDebit(infoList : list[str], fileName : str) -> csvDebitRow:
    '''Parse lines into a csvDebitRow'''
    line = fileName.split("_")[0]
    date = infoList[1]
    description = infoList[2]
    parsed = parseDescription(infoList[2])
    cost = abs(float(infoList[3]))
    
    return csvDebitRow(line,date,description,parsed,cost)

def parseDescription(info : str) -> str:
    '''REGEX only have alphacharacters'''
    return re.sub(r'[^a-zA-Z]', '', info).upper()

def parseStarDescription(info : str) -> str:
    '''REGEX ignore after *'''
    return re.sub(r'[^a-zA-Z]*\*.*|[^a-zA-Z]', '', info).upper()
