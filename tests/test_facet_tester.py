import unittest
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)  # puts parent dir on python search path

from FacetTester import FacetTester, FacetTestScore
from ProgramRunner import ProgramResult
from exc import ConfigurationError

class TestFacetTester(unittest.TestCase):

    def setUp(self):
        f = {'facet_name': '+',
             'interpreter': 'python3',
             'description': 'add 2 numbers',
             'points': 1,
             'tests': [{}, {}]
             }
        module = 'add2nums.py'
        self.facet_tester = FacetTester(f, module, "python3", 2)

    def test_io_spec_correct (self):
        t ={
            'input_filename': 'add_inputs.txt', # input file gives 10 + 12
            'output_regex': r'.*22.*'  # there must be a 10 somewhere in the output
            }
        res = self.facet_tester.facet_io_test(t)
        self.assertTrue(res[1])
        pr: ProgramResult = res[1]
        print(pr)

    def test_io_spec_incorrect (self):
        t = {
            'input_filename': 'add_inputs.txt', # input file gives 10 + 12
            'output_regex': r'.*10.*'  # there must be a 10 somewhere in the output
        }
        res = self.facet_tester.facet_io_test(t)
        self.assertTrue(not res[1])

    def test_facet_test (self):
        t = {'type': 'io',
            'description': "Add two positive numbers",
            'io_test_spec':
                {
                'input_filename': 'add_inputs.txt', # input file gives 10 + 12
                'output_regex': r'.*10.*'  # there must be a 10 somewhere in the output
                }
        }
        res = self.facet_tester.run_facet_test(t)
        self.assertTrue(not res[1])

        
    def test_io_facet_2_correct (self):
        module = 'add2nums.py'
        f = {'facet_name': '+',
         'points': 1,
         'description': 'Correctly adds numbers',
            'tests': [
                {
                    'type': 'io',
                    'description': "Add two positive numbers",
                    'io_test_spec': {
                        'input_filename': 'add_inputs.txt', # input file gives 10 + 12
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
         }
        ft = FacetTester(f,module,"python3",2)
        sc: FacetTestScore = ft.test()
        self.assertEqual(1,sc.points_scored)

    def test_io_facet_1_correct (self):
        module = 'add2nums.py'
        f = {'facet_name': '+',
         'points': 1,
         'description': 'Correctly adds numbers',
            'tests': [
                {
                    'type': 'io',
                    'description': "Add two positive numbers",
                    'io_test_spec': {
                        'input_filename': 'add_inputs.txt', # input file gives 10 + 12
                        'output_regex': r'.*22.*'  # there must be a 22 somewhere in the output
                    }
                },
                {
                    'type': 'io',
                    'description': "Add a positive and a negative number",
                    'io_test_spec': {
                        'input_string': '5\n-8\n+\n',
                        'output_regex': r'.*4.*'  # Incorrect: there must be a 4 somewhere in the output
                    }
                }
            ]
         }
        ft = FacetTester(f,module,"python3",2)
        sc: FacetTestScore = ft.test()
        self.assertEqual(0.5,sc.points_scored)


        #TODO add unit tests for invalid facet structures with missing keys, referring to non-existent input files, regex problems, unit-test.