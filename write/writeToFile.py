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
                if category != "skip" or category not in allCategories:
                    parsedMap[item.parsed] = category.lower();
                    allCategories[str(len(allCategories))] = category.lower()
                    print(parsedMap)


            

def csvGenerator():
    yield from collateDocuments()
    


if __name__ == "__main__":
    openNewDirectory("writeTaxes")
    startTaxProcess(Path("writeTaxes"), datetime.today().strftime('%Y-%m-%d')  + "_tax.txt")