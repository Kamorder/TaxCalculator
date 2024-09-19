import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import csvReader.readCSV

class ReadCSVTest(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()