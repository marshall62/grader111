import unittest
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)  # puts parent dir on python search path

import ProgramRunner as pr
from exc import ConfigurationError

class TestProgramRunner(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.runner = pr.ProgramRunner(interpreter="python3", timeout=2)
        cls.path = os.path.abspath(__file__)
        cls.dir_path = os.path.dirname(cls.path)

    def mod_path (self, module):
        return os.path.join(TestProgramRunner.dir_path, module)
    """
    def test_working_program_input_string (self):
        module = self.mod_path('add2nums.py')
        inp = '3\n5\n'
        r: pr.ProgramResult = TestProgramRunner.runner.run_module(module=module,input_string=inp)
        self.assertEqual(True, r.is_complete)
        self.assertRegex(r.output, '.*8')

    def test_working_program_file_inputs (self):
        module = self.mod_path('add2nums.py')
        fn = 'f35.txt'
        r: pr.ProgramResult = TestProgramRunner.runner.run_module(module=module,input_filename=fn)
        self.assertEqual(True, r.is_complete)
        self.assertRegex(r.output, '.*8')

    def test_working_program_on_nonexist_input_file (self):
        module = self.mod_path('add2nums.py')
        fn = 'nosuch.txt'
        with self.assertRaises(ConfigurationError):
            TestProgramRunner.runner.run_module(module=module,input_filename=fn)

    def test_config_error_2_input_sources (self):
        module = self.mod_path('add2nums.py')
        fn = 'nosuch.txt'
        inp = '3\n5\n'
        with self.assertRaises(ConfigurationError):
            TestProgramRunner.runner.run_module(module=module,input_filename=fn, input_string=inp)
    """
    def test_handle_nohault (self):
        module = self.mod_path('infloop.py')
        r: pr.ProgramResult = TestProgramRunner.runner.run_module(module=module)
        self.assertEqual(False, r.is_complete)
        self.assertEqual(r.error_message, 'timed-out')

    def test_handle_module_error (self):
        module = self.mod_path('divby0.py')
        for i in range(20):
            r: pr.ProgramResult = TestProgramRunner.runner.run_module(module=module)
            self.assertEqual(False, r.is_complete)
            self.assertEqual(r.returncode, 1)
            self.assertRegex(r.output, '.*ZeroDivisionError.*')

    def test_handle_module_syntaxerror (self):
        module = self.mod_path('synterr.py')
        r: pr.ProgramResult = TestProgramRunner.runner.run_module(module=module)
        self.assertEqual(False, r.is_complete)
        self.assertEqual(r.returncode, 1)
        self.assertRegex(r.output, '.*SyntaxError.*')