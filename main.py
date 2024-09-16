from datetime import datetime
from utils.fileReader import getPath, openFile, inputFile
from tax.tax import taxFormat
from write.writeToFile import startProcess
def main():
    initiateFile = inputFile("Please input the name of the formatted File: ")
    startProcess("writeTaxes", datetime.today().strftime('%Y-%m-%d')  + "_tax.txt")
    taxDoc = taxFormat(openFile(getPath("./writeTaxes/" + datetime.today().strftime('%Y-%m-%d')  + "_tax.txt")))
    taxDoc.formatGen()
    taxDoc.printResults()
    taxDoc.writeInFile()

if __name__ == "__main__":
    main()