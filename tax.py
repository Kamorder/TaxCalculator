class taxFormat:
    def __init__(self, gen):
        self.taxLabels = dict()
        self.fileGen = gen

    def formatGen(self) -> None:
        for line in self.fileGen:
            pass #need to learn the formatting

    def printResults(self) -> None:
        for header, money in self.taxLabels.items():
            print(f'{header}: ${money:,.2f}')

    def writeInFile(self) -> None:
        fileName = input('Please type a file name: ')
        with open(fileName, "w") as newFile:
            for header, money in self.taxLabels.items():
                newFile.write(f'{header}: ${money:,.2f}\n')
        print(f"Done writing to File {fileName}")
