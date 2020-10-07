import importlib
import importlib.util
import os, sys
import multiprocessing as mp

import exc
from ProgramRunner import ProgramResult

def extract_module_name (module_path):
    return os.path.splitext(module_path)[0]

class UnitTester:
    def __init__ (self, dir, module, function, student_module_path, student_function_name):
        self.dir = dir
        self.module = module
        self.function = function
        self.unit_test_module = None
        self.student_module = None
        self.student_module_path = student_module_path
        self.student_function_name = student_function_name
        self.setup()

    def setup (self):
        self.add_dir_to_path()
        try:
            self.unit_test_module = self.load_module(extract_module_name(self.module))
        except Exception as e:
            raise exc.ConfigurationError(f"Unit testing module not loading {self.module}")
        self.student_module = self.load_module(extract_module_name(self.student_module_path))

    def add_dir_to_path (self):
        if self.dir not in sys.path:
            sys.path.append(self.dir)

    def load_module (self, module_path):
        mod_name = os.path.splitext(module_path)[0]
        if mod_name not in sys.modules:
            spec = importlib.util.find_spec(mod_name, package=None)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            sys.modules[mod_name] = mod
            return mod
        else:
            return sys.modules[mod_name]

    def run_student_program (self,q):
        try:
            res = self.tester_fn(self.tested_fn)
        except:
            q.put(False)
        else:
            q.put( res )

    def test (self):
        '''
        Will pass the student module to the unit test module test function.
        The test function will thencase thisfor isfor everythingint
        return something.  Any non-False value it returns will be considered to be a working unit-test.
        :return: True/False (or equiv)
        '''
        try:
            self.tester_fn = getattr(self.unit_test_module, self.function)
        except Exception as e:
            raise exc.ConfigurationError("Missing unit test ", self.test_fn)
        try:
            self.tested_fn = getattr(self.student_module, self.student_function_name)
        except:
            return ProgramResult(is_complete=True, returncode=-1, output='',
                                 error_message=f'{self.student_function_name} function not defined',
                                 is_correct=False)
        # The tester_fn is passed the tested_fn which it must call with args appropriately.

        try:
            ctx = mp.get_context('spawn')
            q = ctx.Queue()
            p = mp.Process(target=self.run_student_program, args=(q,))
            p.start()

            p.join(2)
            if p.exitcode == None:
                p.terminate()
                r = ProgramResult(is_complete=False,returncode=None,output='',error_message='',is_correct=False)
                return r
            else:
                res = q.get()
                r = ProgramResult(is_complete=True, returncode=p.exitcode, output=str(res), error_message='', is_correct=res)
                return r
        except Exception as e:
            return ProgramResult(is_complete=True, returncode=p.exitcode, output='', error_message=str(e), is_correct=False)




