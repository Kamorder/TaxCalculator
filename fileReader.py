from pathlib import Path
from typing import Generator


def inputFile(textStr = '') -> Path:
    '''Turns a string into a file path and returns it'''
    return Path(input(textStr))

def openFile(path) -> Generator:
    '''Opens the file and returns a generator'''
    with open(path) as file:
        return yieldIter(file.readlines())

def yieldIter(iterable) -> Generator:
    '''turns an iterable into a generator'''
    yield from iterable
