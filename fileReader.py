from pathlib import Path
from typing import Generator


def inputFile(textStr = '') -> Path:
    return Path(input(textStr))

def openFile(path) -> Generator:
    with open(path) as file:
        return yieldIter(file.readlines)

def yieldIter(iterable) -> Generator:
    yield from iterable
