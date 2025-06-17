from utils.fileReader import inputFile
from utils.company import companyFolder
from tax.tax import taxFormat
from datetime import datetime


def main():
    ''' Structurizes the tax document by creating a company directory, collating all the csv files into one, 
    applying labels to the data, summing all the data with the same labels, then outputting a document filled with 
    the summarized categories.'''
    companyName = inputFile("Enter folder name for company directory:")
    company = companyFolder(companyName)
    taxDoc = taxFormat(company.getProcessingFile())
    taxDoc.formatGen()
    taxDoc.printResults()
    taxDoc.writeInFile(company.companyPath/"polished"/f"{datetime.today().strftime('%Y-%m-%d')}_itemizedtax.txt")

if __name__ == "__main__":
    main()
