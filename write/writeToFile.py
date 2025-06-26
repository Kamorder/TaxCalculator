import pickle

from pathlib import Path
from typing import Generator
from typing import IO
from csvReader.readCSV import collateDocuments
from csvReader.csvClass import csvRow

def openNewDirectory(directoryName: Path) -> None:
    Path.mkdir(directoryName, exist_ok=True)

def startTaxProcess(directory: Path, fileName: str) -> None:
    '''Start the process using the CSV file format'''
    partialDirectory = directory/"packaged"
    parsedMap = loadOrDefault(partialDirectory, "parsedMap", {})
    allCategories = loadOrDefault(partialDirectory, "allCategories", {})
    prev5 = loadOrDefault(partialDirectory, "prev5", [])

    with open(directory/fileName, 'w') as taxFile:
        try:
            for item in csvGenerator():
                print(f"Current item:\n{item}")
                if item.parsed in parsedMap:
                    #TODO ADD rest
                    print("skip")
                else:
                    print(f"\n{allCategories}")
                    category = input("respective category: ")
                    while category.strip() == "edit previous":
                        edit = input(f"{[x.description for x in prev5]}, which would you like to edit? Press 1-5 or press enter to skip:\n")
                        if edit.isnumeric() and 0 < int(edit) <= len(prev5):
                            edit = prev5[int(edit) - 1] 
                            response = input(f"select new category for {edit}")
                            parsedMap[edit.parsed] = response.lower()
                            allCategories[str(len(allCategories))] = response.lower() 
                        print(f"Current item:\n{item}")
                        category = input("respective category: ")
                    addPrev(prev5, item)
                    if category in allCategories: 
                        parsedMap[item.parsed] = allCategories[category]
                    elif category.strip() != "skip":
                        parsedMap[item.parsed] = category.lower();
                        allCategories[str(len(allCategories))] = category.lower()
                        print(parsedMap)
                    else:
                        parsedMap[item.parsed] = "skip"
        finally:
            save(parsedMap,partialDirectory/"parsedMap")
            save(allCategories,partialDirectory/"allCategories")
            save(prev5, partialDirectory/"prev5")

        print(f"done, collating data...\n{parsedMap}\n{allCategories}\n")
        writeDict = collatedataintosheet(parsedMap,allCategories)
        writeAllData(taxFile, writeDict)

def collatedataintosheet(parsedMap: dict[str:csvRow], allCategories: dict[str:str]) -> dict:
    '''End process which rewinds and puts all the information into a formatted dictionary'''
    writeDict = {}
    for value in allCategories.values():
        writeDict[value] = []
    for item in csvGenerator():
        if parsedMap[item.parsed] != "skip":
            writeDict[parsedMap[item.parsed]].append(item.cost)
    return writeDict

def loadOrDefault(partialDir: Path, name: str, default: any) -> any:
    '''Loads a pkl file or picks a default'''
    path = partialDir/name
    return load(path) if (path.with_suffix(".pkl")).exists() else default

def addPrev(prev5: list[None|str], obj: str) -> None:
    """Manages the previous 5 objects"""
    prev5.insert(0,obj)
    if len(prev5) > 5:
        prev5.pop()

def save(object: any, objectFile: Path) -> None:
    '''Pkl an object and ensure it keeps the pkl file extension'''
    objectFile = objectFile.with_suffix(".pkl")
    with open(objectFile, mode="wb") as writeFile:
        pickle.dump(object, writeFile)

def load(objectFile: Path) -> any:
    '''Loads the object'''
    objectFile = objectFile.with_suffix(".pkl")
    with open(objectFile, mode="rb") as file:
        object = pickle.load(file)
    return object

def writeAllData(taxFile: IO, writeDict: dict[str:str]) -> None: 
    '''End process which takes a formatted dict and writes a document which which is formatted in the README way'''
    for key, values in writeDict.items():
        taxFile.write(key.upper() + "\n")
        for value in values:
            taxFile.write(str(value) + " ")
        taxFile.write("\n\n")


def csvGenerator() -> Generator:
    yield from collateDocuments()
