class taxFormat:
    def __init__(self, gen):
        self.taxHeader = dict()
        self.fileGen = gen

    def formatGen(self) -> None:
        '''Write a dictionary based on the tax file summarizing total costs'''
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
        for header, money in self.taxHeader.items():
            print(f'{header}: ${money:,.2f}')

    def writeInFile(self) -> None:
        '''End process which writes everything into the final document'''
        fileName = input('Please type a file name: ')
        with open(fileName, "w") as newFile:
            for header, money in self.taxHeader.items():
                newFile.write(f'{header}: ${money:,.2f}\n')
        print(f"Done writing to file {fileName}")


class duplicateLabel(Exception):
    def __init__(self, dupeName):
        self.dupeName = dupeName

    def __str__(self) -> str:
        return f'Error: The header -> {self.dupeName} was used as a header more than once'