from utils.fileReader import inputFile
from utils.company import companyFolder
from tax.tax import taxFormat
from datetime import datetime


def main():
    companyName = inputFile("Enter folder name for company directory:")
    company = companyFolder(companyName)
    file = company.getProcessingFile()
    
    taxDoc = taxFormat(file)
    taxDoc.formatGen()
    taxDoc.printResults()
    '''TODO: Find out how you want to store the new file data, currently really sloppy so need to find a new way, 
    Current thinking... delete writeTaxes folder and instead create a companywide directory under a new folder then have a subfolder 
    with these documents, also store the data from these folders using pickle...
     '''
    taxDoc.writeInFile(company.companyPath/"polished"/f"{datetime.today().strftime('%Y-%m-%d')}_itemizedtax.txt")

if __name__ == "__main__":
    main()
