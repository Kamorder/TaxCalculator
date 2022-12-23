class taxFormat:
    def __init__(self, gen):
        self.taxHeader = dict()
        self.fileGen = gen

    def formatGen(self) -> None:
        try:
            currentHeader = ''
            for line in self.fileGen:
                if not line.split()[0].isnumeric():
                    if line.strip() not in self.taxHeader:
                        self.taxHeader[line.strip()] = 0
                        currentHeader = line.strip()
                    else:
                        raise duplicateLabel(line.strip())
                else:
                    if currentHeader:
                        self.taxHeader[currentHeader] += sum((float(x) for x in line.split()))

        except duplicateLabel as error:
            print(error)

    def printResults(self) -> None:
        for header, money in self.taxHeader.items():
            print(f'{header}: ${money:,.2f}')

    def writeInFile(self) -> None:
        fileName = input('Please type a file name: ')
        with open(fileName, "w") as newFile:
            for header, money in self.taxHeader.items():
                newFile.write(f'{header}: ${money:,.2f}\n')
        print(f"Done writing to File {fileName}")


class duplicateLabel(Exception):
    def __init__(self, dupeName):
        self.dupeName = dupeName

    def __str__(self) -> str:
        return f'Error: The header -> {self.dupeName} was used as a header more than once'