import unittest
import os, sys
from typing import List
import json
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)  # puts parent dir on python search path

from grader2 import Grader
from StudentScore import StudentScore
from CSVReport import CSVReport

class TestGrader (unittest.TestCase):

    def test_reporter(self):
        f = open('rub.json','r')
        rubric = json.load(f)
        f.close()
        module = 'solution.py'
        dir = '/srv/dev/python/smith/grader/tests'
        g = Grader(dir='', rubric_definition=rubric, interpreter='python3', timeout=10)
        module = 'bug_solution.py'
        student_score: StudentScore = g.test_program(module)
        CSVReport(dir=dir,filename='testrep.csv').report_csv(g.results)


