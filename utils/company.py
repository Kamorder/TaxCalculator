import sys
import os
import shutil
from cmdLine import pdataTrue, pdataPath
from pathlib import Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from write.writeToFile import openNewDirectory

class companyFolder: 
    def __init__(self,name:str):
        self.companyname = name 
        self.companyPath = Path(name)
        self.csv = False
        self.parsedDocument = pdataTrue()

        self.initCompanyDirectory()
    
    def initCompanyDirectory(self) -> None:
        '''Initalizes the Directories'''
        if not os.path.exists(self.companyname):
            openNewDirectory(self.companyname)
            for name in ["raw","packaged","polished"]:
                openNewDirectory(self.companyPath/name)
            self.moveResources()

    def moveResources(self) -> None:
        '''Takes any csv files/path files and moves it into the raw folder'''

        if self.parsedDocument:
            self.addToRaw(Path(pdataPath()))

        for file in Path("resources").rglob("*.CSV"): 
            self.addToRaw(file)

    def addToRaw(self, filePath : Path) -> None:
        '''Moves a file into the raw directory'''
        shutil.move(filePath, self.companyPath/"raw")

if __name__ == "__main__":
    name = "testcompanyfolder"
    shutil.rmtree(name)
    companyFolder(name)