from datetime import datetime
from utils.fileReader import getPath, openFile
from utils.cmdLine import pdataTrue, pdataPath
from tax.tax import taxFormat
from write.writeToFile import startProcess

def main():
    file = ''
    if pdataTrue():
        file = openFile(pdataPath())
    else:
        startProcess("writeTaxes", datetime.today().strftime('%Y-%m-%d')  + "_tax.txt")
        file = openFile(getPath("./writeTaxes/" + datetime.today().strftime('%Y-%m-%d')  + "_tax.txt"))
    
    taxDoc = taxFormat(file)
    taxDoc.formatGen()
    taxDoc.printResults()
    taxDoc.writeInFile()

if __name__ == "__main__":
    main()
