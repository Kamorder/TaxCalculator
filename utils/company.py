import os
import shutil

from typing import Generator
from datetime import datetime
from pathlib import Path

from write.writeToFile import startTaxProcess, openNewDirectory
from utils.cmdLine import pdataTrue, pdataPath
from utils.fileReader import openFile, getPath



class companyFolder: 
    def __init__(self, name: str):
        self.companyName = f"{datetime.now().year - 1} taxes {name}" 
        self.companyPath = getPath(self.companyName)
        self.parsedPath = None
        self.ifParsed = pdataTrue()

        self.initCompanyDirectory()
    
    def initCompanyDirectory(self) -> None:
        '''Initalizes the Directories'''
        if not os.path.exists(self.companyName):
            openNewDirectory(self.companyName)
            for name in ["raw","packaged","polished"]:
                openNewDirectory(self.companyPath/name)
            self.moveResources()

    def moveResources(self) -> None:
        '''Takes any csv files/path files and moves it into the raw folder'''

        if self.ifParsed:
            self.parsedPath = self.moveToRaw(getPath(pdataPath()))

        for file in Path("resources").rglob("*.CSV"): 
            self.moveToRaw(file)
            

    def moveToRaw(self, filePath: Path) -> str:
        '''Moves a file into the raw directory'''
        return shutil.move(filePath, self.companyPath/"raw")

    def getProcessingFile(self) -> Generator:
        '''Gives the user the processed file'''
        if self.ifParsed:
            file = openFile(self.parsedPath)
        else:
            
            startTaxProcess(self.companyPath/"raw", datetime.today().strftime('%Y-%m-%d')  + "_tax.txt")
            file = openFile(getPath(self.companyPath/"raw"/f"{datetime.today().strftime('%Y-%m-%d')}_tax.txt"))
        return file

if __name__ == "__main__":
    name = "testcompanyfolder"
    #shutil.rmtree(name)
    companyFolder(name)
