from datetime import datetime
from utils.fileReader import getPath, openFile, inputFile
from utils.cmdLine import pdataTrue, pdataPath
from tax.tax import taxFormat
from write.writeToFile import openNewDirectory,startProcess

def main():
    file = ''
    companyName = inputFile("Enter folder name for company directory:")
    if pdataTrue():
        file = openFile(pdataPath())
    else:
        startProcess(f"writeTaxes/{companyName}", datetime.today().strftime('%Y-%m-%d')  + "_tax.txt")
        file = openFile(getPath(f"./writeTaxes/{companyName}/" + datetime.today().strftime('%Y-%m-%d')  + "_tax.txt"))
    
    taxDoc = taxFormat(file)
    taxDoc.formatGen()
    taxDoc.printResults()
    '''TODO: Find out how you want to store the new file data, currently really sloppy so need to find a new way, 
    Current thinking... delete writeTaxes folder and instead create a companywide directory under a new folder then have a subfolder 
    with these documents, also store the data from these folders using pickle...
     '''
    taxDoc.writeInFile(companyName/f"{datetime.today().strftime('%Y-%m-%d')}_itemizedtax.txt")

if __name__ == "__main__":
    main()
