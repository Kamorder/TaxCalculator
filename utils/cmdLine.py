import sys

def pdataTrue() -> bool:
    return len(sys.argv) > 1

def pdataPath() -> str:
    return sys.argv[1]