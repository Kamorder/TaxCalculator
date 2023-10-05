from fileReader import inputFile, openFile
from tax import taxFormat
def main():
    '''Gets the file, initiates a taxFormat instance,and utilizes the methods to create the formatted Report.'''
    initiateFile = inputFile("Please input the name of the formatted File: ")
    taxDoc = taxFormat(openFile(initiateFile))
    taxDoc.formatGen()
    taxDoc.printResults()
    taxDoc.writeInFile()

if __name__ == "__main__":
    main()
