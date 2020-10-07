import subprocess
import exc
class ProgramRunner:
    def __init__ (self, interpreter, timeout=2, module=None):
        # don't use a timeout less than 1 or sometimes failing subprocesses timeout
        # even when they are just crashing and need time to finish.
        self.interpreter = interpreter
        self.module = module
        self.timeout = timeout

    def run_module(self, module=None, input_string=None, input_filename=None):
        '''
        Run the module and return two values: True/False if module completes.
        If it completes the second value is the output.  If it fails to complete,
        the second value is a an error string or the return code subprocess
        :return:
        '''
        self.module = module or self.module
        self.input_string = input_string
        self.input_filename = input_filename
        self.error_check_inputs()
        try:
            if self.input_filename:
                try:
                    f = None
                    f = open(self.input_filename, 'r')
                    completed = subprocess.run([self.interpreter, self.module], text=True, stdin=f,
                                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=self.timeout)
                except FileNotFoundError:
                    raise exc.ConfigurationError("Input file not found " + self.input_filename)
                finally:
                    if f:
                        f.close()
            else:
                completed = subprocess.run([self.interpreter, self.module], text=True, input=self.input_string,
                                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=self.timeout)
        except subprocess.TimeoutExpired:
            return ProgramResult(False, None, None, 'timed-out')
        except exc.ConfigurationError as e:
            raise e
        except Exception as ex:
            return ProgramResult(False,None,None,ex)
        else:
            if completed.returncode == 0:
                return ProgramResult(True, 0, completed.stdout, None)
            else:
                return ProgramResult(True, completed.returncode, completed.stdout, 'program had errors')

    def error_check_inputs(self):
        try:
            assert ( not self.input_filename and not self.input_string ) or \
               (not self.input_filename and self.input_string) or \
               (self.input_filename and not self.input_string), \
                "Must provide no inputs of either kind or else must provide a file or a string but not both."
        except AssertionError as e:
            raise exc.ConfigurationError(e)



class ProgramResult:

    def __init__ (self, is_complete, returncode, output, error_message, is_correct=False):
        self.is_complete = is_complete
        self.output = output
        self.returncode = returncode
        self.error_message = error_message
        self.is_correct = is_correct

    def set_is_correct (self, is_correct):
        self.is_correct = is_correct
