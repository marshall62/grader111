import unittest
from grader_old import *
from collections import defaultdict

class MyTest(unittest.TestCase):
    def test_io_compare_same (self):
        x = io_compare('sd/subtract_outputs.txt', 'sd/subtract_outputs.txt')
        assert x == 1

    def test_io_compare_diff (self):
        x = io_compare('sd/subtract_outputs.txt', 'sd/add_outputs.txt')
        assert x == 0

    def test_grade_results (self):
        d = defaultdict(list)
        grade_results("stud1.py", 'sd/subtract_outputs.txt', {'output_filename': 'subtract_outputs.txt', 'label': '-'}, d)
        self.assertDictEqual(dict(d), {'stud1.py': [('-', 1)]})

    def test_grade_results (self):
        d = defaultdict(list)
        grade_results("stud1.py", 'sd/add_outputs.txt', {'output_filename': 'subtract_outputs.txt', 'label': '-'}, d)
        self.assertDictEqual(dict(d), {'stud1.py': [('-', 0)]})


    def test_test_two_program (self):
        d = defaultdict(list)
        sub = {'input_filename': 'subtract_inputs.txt', 'output_filename': 'subtract_outputs.txt', 'label': '-'}
        add = {'input_filename': 'add_inputs.txt', 'output_filename': 'add_outputs.txt', 'label': '+'}
        test_program('stud1.py', [add, sub], d)
        test_program('stud2.py', [add, sub], d)
        soln = {'stud1.py': [('+', 1), ('-', 1)],
                'stud2.py': [('+', 1), ('-', 1)]}
        for k, v in d.items():
            ev = soln[k]
            self.assertEqual(sorted(v), sorted(ev))


if __name__ == '__main__':
    unittest.main()