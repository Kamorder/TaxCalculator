from datetime import datetime
from pathlib import Path
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from csvReader.readCSV import collateDocuments

def openNewDirectory(directoryName) -> None:
    if not os.path.isdir(directoryName):
        os.mkdir(directoryName)

def startTaxProcess(directory, fileName):
    currentSpot = 0
    parsedMap = {}
    allCategories = {}
    with open(directory/fileName, 'w') as taxFile:
        for item in csvGenerator():
            print(f"Current item:\n{item}")
            currentSpot += 1
            if item.parsed in parsedMap:
                #TODO ADD rest
                print("skip")
            else:
                print(f"\n{allCategories}")
                category = input("respective category: ")
                if category in allCategories: 
                    parsedMap[item.parsed] = allCategories[category]
                elif category != "skip":
                    parsedMap[item.parsed] = category.lower();
                    allCategories[str(len(allCategories))] = category.lower()
                    print(parsedMap)
        writeDict = collatedataintosheet(parsedMap,allCategories)
        writeAllData(taxFile, writeDict)

def collatedataintosheet(parsedMap, allCategories):
    writeDict = {}
    for value in allCategories.values():
        writeDict[value] = []
    for item in csvGenerator():
        writeDict[parsedMap[item.parsed]].append(item.cost)
    return writeDict

def writeAllData(taxFile, writeDict): 
    for key, values in writeDict.items():
        taxFile.write(key.upper() + "\n")
        for value in values:
            taxFile.write(str(value) + " ")
        taxFile.write("\n\n")


def csvGenerator():
    yield from collateDocuments()
    
def startProcess(documentDirectory, documentName):
    openNewDirectory(documentDirectory)
    startTaxProcess(Path(documentDirectory), documentName)

if __name__ == "__main__":
    startProcess("writeTaxes", datetime.today().strftime('%Y-%m-%d')  + "_tax.txt")
