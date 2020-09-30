import unittest
import os, sys
from typing import List
import json
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)  # puts parent dir on python search path
from HTMLReport import extract_name
class TestExtractor (unittest.TestCase):

    def test_reporter(self):
        stud_file = os.path.join(currentdir,"stud1.py")
        n = extract_name(stud_file)
        print(n)



