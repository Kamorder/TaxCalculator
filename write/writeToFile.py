from datetime import datetime
from pathlib import Path
import os


def openNewDirectory(directoryName) -> None:
    if not os.path.isdir(directoryName):
        os.mkdir(directoryName)

def startTaxProcess(directory, fileName):
    with open(directory/fileName, 'w') as taxFile:
        pass

if __name__ == "__main__":
    openNewDirectory("writeTaxes")
    startTaxProcess(Path("writeTaxes"), datetime.today().strftime('%Y-%m-%d')  + "_tax.txt")