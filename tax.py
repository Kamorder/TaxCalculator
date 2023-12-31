class taxFormat:
    '''Main formatting class.'''
    def __init__(self, gen):
        self.taxHeader = dict()
        self.fileGen = gen

    def formatGen(self) -> None:
        '''Takes all the lines in a given file and assigns them as a header if they are alphanumeric. 
        If they are numeric the value is added to the most recent header.'''
        try:
            currentHeader = ''
            for line in self.fileGen:
                if line.strip():
                    splitLine = line.split()
                    if not splitLine[0].replace('.','',1).replace(',', '').isnumeric():
                        if line.strip() not in self.taxHeader:
                            self.taxHeader[line.strip()] = 0
                            currentHeader = line.strip()
                        else:
                            raise duplicateLabel(line.strip())
                    else:
                        if currentHeader:
                            self.taxHeader[currentHeader] += sum((float(x.replace(',', '')) for x in line.split()))

        except duplicateLabel as error:
            print(error)

    def printResults(self) -> None:
        '''Prints the results for the user to see before adding to a txt file.'''
        for header, money in self.taxHeader.items():
            print(f'{header}: ${money:,.2f}')

    def writeInFile(self) -> None:
        '''Writes the header with the money values into a txt file in the format Name: $money.'''
        fileName = input('Please type a file name: ')
        with open(fileName, "w") as newFile:
            for header, money in self.taxHeader.items():
                newFile.write(f'{header}: ${money:,.2f}\n')
        print(f"Done writing to file {fileName}")


class duplicateLabel(Exception):
    '''Exception if the user uses a duplicate name.'''
    def __init__(self, dupeName):
        self.dupeName = dupeName

    def __str__(self) -> str:
        return f'Error: The header -> {self.dupeName} was used as a header more than once'
