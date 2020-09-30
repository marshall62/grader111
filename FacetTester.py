from ProgramRunner import ProgramRunner, ProgramResult
import exc
import re

class FacetTester:

    def __init__ (self, facet, student_module_path, interpreter='python3', timeout=2):
        self.facet = facet
        self.student_module_path = student_module_path
        self.program_runner = ProgramRunner(interpreter=interpreter,timeout=timeout)


    def test(self):
        '''
        Run all the tests within a facet.  Each test returns True/False.  The points awarded for the facet
        is the (number of passed tests / number of tests) * facet points
        :param facet:
        :return: FacetTestScore object that contains score and information about
        each test it performed.
        '''
        count = 0
        tests = self.facet['tests']
        num_tests = len(tests)
        test_results = []
        for test in tests:
            tr = self.run_facet_test(test)
            result: ProgramResult = tr[0]
            isCorrect = tr[1]
            test_results.append(result)
            if isCorrect:
                count += 1
        points_scored = (count / num_tests) * self.facet['points']
        return FacetTestScore(self.facet, points_scored, test_results)

    def run_facet_test (self, test):
        '''
        :param test:
        :return: tuple (ProgramResult, isCorrect)
        '''
        if test['type'] == 'io':
            return self.facet_io_test(test['io_test_spec'])
        else:
            raise NotImplemented("unit tests not yet testable")


    def facet_io_test(self, io_test_spec):
        '''
        Run the student module with inputs.  If the program completes, grade its output.
        :param io_test_spec:
        :return: tuple with ProgramResult and grade
        '''
        input_filename = io_test_spec.get('input_filename')
        input_string = io_test_spec.get('input_string')
        output_regex = io_test_spec.get('output_regex', '')
        # get back True/False indicating whether program finished and its output (or error)
        r: ProgramResult = self.program_runner.run_module(module=self.student_module_path,
                                                input_filename=input_filename,
                                                input_string=input_string)
        grade = self.grade_io_result(r, output_regex)
        return (r, grade)


    def grade_io_result(self, r: ProgramResult, output_regex):
        '''
        If the program completed test its output against the regex
        :param self:
        :param r:
        :param output_regex:
        :return: True if program runs and produces correct output, False o/w
        '''
        # If student program finishes, test its output to see if correct
        if r.is_complete:
            r.is_correct = self.check_output(r.output, output_regex)

        else:
            r.is_correct = False
        return r.is_correct


    def check_output(self, student_module_output, regex):
        '''
        Tests the student program output against a regex and returns True/False regarding match
        :param student_module_output:
        :param regex:
        :return:
        '''
        pattern = re.compile(regex, re.DOTALL)
        mr = pattern.match(student_module_output)
        return mr != None


class FacetTestScore:
    def __init__ (self, facet, points_scored, test_results):
        self.facet = facet
        self.points_scored = points_scored
        self.test_results = test_results