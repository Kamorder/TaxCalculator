from fileReader import inputFile, openFile
from tax import taxFormat
def main():
    initiateFile = inputFile("Please input the name of the formatted File: ")
    taxDoc = taxFormat(openFile(initiateFile))
    taxDoc.formatGen()
    taxDoc.printResults()
    taxDoc.writeInFile()