import unittest
import os, sys
from typing import List

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)  # puts parent dir on python search path

from grader2 import Grader
from CSVReport import DefaultReporter
from FacetTester import FacetTestScore

class TestGrader (unittest.TestCase):
    rubric = {
        'name': 'Clunky Calculator',
        'interpreter': 'python3',
        'execution_tests': [
            {'facet_name': '+',
             'points': 1,
             'description': 'Correctly adds numbers',
             'tests': [
                 {
                     'type': 'io',
                     'description': "Add two positive numbers",
                     'io_test_spec': {
                         'input_filename': 'add_inputs.txt',  # input file gives 10 + 12
                         'output_regex': r'.*22.*'  # there must be a 22 somewhere in the output
                     }
                 },
                 {
                     'type': 'io',
                     'description': "Add a positive and a negative number",
                     'io_test_spec': {
                         'input_string': '5\n-8\n+\n',
                         'output_regex': r'.*-3.*'  # there must be a 22 somewhere in the output
                     }
                 }
             ]
             },
            {'facet_name': '-',
             'points': 1,
             'description': 'Correctly subtracts numbers',
             'tests': [
                 {
                     'type': 'io',
                     'io_test_spec': {
                         'input_filename': 'subtract_inputs.txt',  # input file gives 13 - 18
                         'output_regex': r'.*-5.*'  # there must be a -5 somewhere in the output
                     }
                 }]
             },
            {'facet_name': '*',
             'points': 1,
             'tests': [
                 {
                     'type': 'io',
                     'io_test_spec': {
                         'input_filename': 'mult_inputs.txt',  # input file gives -5 * 10
                         'output_regex': r'.*-50.*'  # there must be a -50 somewhere in the output
                     }
                 }]
             },
            {'facet_name': '/',
             'points': 1,
             'tests': [
                 {
                     'type': 'io',
                     'io_test_spec': {
                         'input_filename': 'div_inputs_1.txt',  # input file gives 18 / 3
                         'output_regex': r'.*6.*'  # there must be a 6 somewhere in the output
                     }
                 },
                 {
                     'type': 'io',
                     'io_test_spec': {
                         'input_filename': 'div_inputs_2.txt',  # input file gives 10 / 3
                         'output_regex': r'.*3\.33.*'  # there must be a 3.33 somewhere in the output
                     }
                 }
             ]
             },
            # extra credit 1 point for exponentiation
            {'facet_name': '**',
             'points': 1,
             'tests': [
                 {
                     'type': 'io',
                     'io_test_spec': {
                         'input_filename': 'exp_inputs.txt',  # input file gives -3 ** 3
                         'output_regex': r'.*-27.*'  # there must be a -27 somewhere in the output
                     }
                 }
             ]
             }
        ]}

    def test_rubric (self):
        module = 'solution.py'
        g = Grader(dir='.', rubric_definition=TestGrader.rubric, interpreter='python3')
        module = 'solution.py'
        result = g.test_program(module)
        self.assertTrue(result[module] != None)
        results: List[FacetTestScore] = result[module]
        self.assertEqual(len(results), 5)
        for facet_score in results:
            self.assertEqual(facet_score.points_scored, 1)

    def test_reporter(self):
        module = 'solution.py'
        g = Grader(dir='.', rubric_definition=TestGrader.rubric, interpreter='python3')
        module = 'solution.py'
        result = g.test_program(module)
        DefaultReporter("grades.csv").report_csv(result)
        self.assertTrue(os.path.isfile("grades.csv"))


