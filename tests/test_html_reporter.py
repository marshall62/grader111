import unittest
import os, sys
from typing import List
import json
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)  # puts parent dir on python search path

from grader2 import Grader
from StudentScore import StudentScore
from HTMLReport import HTMLReport, extract_name

class TestHTMLReporter (unittest.TestCase):

    def test_reporter(self):
        f = open('rub.json','r')
        rubric = json.load(f)
        f.close()
        module = 'solution.py'
        g = Grader(dir='', rubric_definition=rubric, interpreter='python3', timeout=10)
        module = os.path.join(currentdir,'bug_solution.py')
        module = os.path.join(currentdir,'stud1.py')
        student_score: StudentScore = g.test_program(module)
        n = extract_name(module)
        HTMLReport(dir=currentdir,results=g.results,rubric=g.rubric,filename="tab.html")



