from pathlib import Path
from typing import Generator, Iterable


def inputFile(textStr: str = '') -> Path:
    return Path(input(textStr))

def getPath(input: str) -> Path:
    return Path(input)

def openFile(path: Path) -> Generator:
    with open(path) as file:
        return yieldIter(file.readlines())

def yieldIter(iterable: Iterable) -> Generator:
    yield from iterable
