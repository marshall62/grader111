import os, sys
import unittest

import exc

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)  # puts parent dir on python search path

import UnitTester as ut

class TestUnitTester(unittest.TestCase):
    # @unittest.skip("reason for skipping")
    def test_1 (self):
        u = ut.UnitTester(dir=currentdir,
                          module="unit_tests.py",
                          function="test_add",
                          student_module_path="stud2.py",
                          student_function_name="add").test()
        self.assertTrue(u.is_correct)

    # @unittest.skip("reason for skipping")
    def test_2 (self):
        u = ut.UnitTester(dir=currentdir,
                          module="unit_tests.py",
                          function="test_sub",
                          student_module_path="stud2.py",
                          student_function_name="sub").test()
        self.assertTrue(u.is_correct)

    # @unittest.skip("reason for skipping")
    def test_div1 (self):
        u = ut.UnitTester(dir=currentdir,
                          module="unit_tests.py",
                          function="test_div",
                          student_module_path="stud2.py",
                          student_function_name="div").test()
        self.assertTrue(u.is_correct)

    # @unittest.skip("reason for skipping")
    def test_div2 (self):
        # student program will divide by zero and raise exception so this should
        # correctly get back False
        u = ut.UnitTester(dir=currentdir,
                          module="unit_tests.py",
                          function="test_div2",
                          student_module_path="stud2.py",
                          student_function_name="div").test()
        self.assertFalse(u.is_correct)

    # @unittest.skip("reason for skipping")
    def test_mult_infloop (self):
        # student function for mult infinitely loops so want False as result
        u = ut.UnitTester(dir=currentdir,
                          module="unit_tests.py",
                          function="test_mul",
                          student_module_path="stud2.py",
                          student_function_name="mult").test()
        self.assertFalse(u.is_correct)

    # @unittest.skip("reason for skipping")
    def test_undef (self):
        u = ut.UnitTester(dir=currentdir,
                          module="unit_tests.py",
                          function="test_div2",
                          student_module_path="stud2.py",
                          student_function_name="undef").test()
        self.assertFalse(u.is_correct)

    # @unittest.skip("reason for skipping")
    def test_undef(self):
        with self.assertRaises(exc.ConfigurationError):
            u = ut.UnitTester(dir=currentdir,
                              module="not_exist.py",
                              function="test_div2",
                              student_module_path="stud2.py",
                              student_function_name="undef").test()


