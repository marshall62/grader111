import os
import sys
import importlib
import pprint
from _collections import defaultdict

def test_program (program_filename, io_specs, results, loaded_module=None):
    '''
    :param program_file:
    :param io_spec: list of dictionaries that specify inputs and outputs
    :param results dictionary of grades
    :return:
    Update the results dictionary (keyed by program_file) with either 0 or 1 if the students output matches the expected
    '''
    prog = program_filename[:-3]
    student_module_loaded = loaded_module
    # N.B. python only loads a module once.  So we have to hold onto it so that we can then force
    # it to be reloaded each time we want to run the students program.
    for io_spec in io_specs:
        test_input_file = io_spec['input_filename']
        if os.path.isfile('student_output.txt'):
            os.remove('student_output.txt')
        try:
            student_module_loaded = run_program(prog, test_input_file, 'student_output.txt', loaded_module=student_module_loaded)
            grade_results(program_filename, 'student_output.txt', io_spec, results)
        except:
            # exceptions will result in a 0 for each test.
            results[program_filename].append((io_spec['label'], 0))


def run_program(py_program, input_file, output_file, loaded_module=None):

    # print(file.name)
    # Redirect sys.stdout to the file
    sin = sys.stdin
    sout = sys.stdout
    serr = sys.stderr
    try:
        sys.stdin = open(input_file, 'r')
        sys.stdout = open(output_file, 'w')
        sys.stderr = sys.stdout
        if not loaded_module:
            loaded_module = importlib.import_module(py_program)
        else:
            importlib.reload(loaded_module)
        sys.stdout.flush()
        sys.stderr.flush()
        sys.stdout.close()
        sys.stdin.close()
        return loaded_module
    finally:
        sys.stdin = sin
        sys.stdout = sout
        sys.stderr = serr

def io_compare (student_filename, expected_out_filename):
    ''' Very brittle.  This is where improvements will need to be made in the future.'''
    s = open(student_filename)
    e = open(expected_out_filename)
    stxt = s.read().strip()
    etxt = e.read().strip()
    s.close()
    e.close()
    return 1 if etxt == stxt else 0

def grade_results (program_filename, student_output_file, io_spec, results):
    '''
    Compare the student output to expected and update the results dict.
    :param program_file:
    :param student_output:
    :param io_spec: dictionary defining inputs and expected outputs
    :param results:
    :return:
    '''
    exp_out_filename = io_spec["output_filename"]
    label = io_spec["label"]
    grade = io_compare(student_output_file, exp_out_filename)
    results[program_filename].append((label, grade))


def cycle_dir (dir, io_specs):
    print("Grading")
    results = defaultdict(list)
    for entry in os.scandir(dir):
        if entry.path.endswith(".py") and entry.is_file and \
            entry.name not in ['grader.py', 'test.py', 'solution.py']:
            print(".",end='')
            test_program(entry.name , io_specs, results)
    return results

def write_student_info (file, stud_filename, scores):
    scores = sorted(scores)
    print(stud_filename)
    pprint.pprint(scores)
    file.write(stud_filename+",")
    sum = 0
    for s in scores:
        sum += s[1]
        file.write(str(s[1])+",")
    file.write(f'{sum}\n')

def write_results (results, io_specs, grade_file):
    f = open(grade_file,'w')
    f.write('program name,')
    labels = sorted([s["label"] for s in io_specs])
    for l in labels:
        f.write(l + ',')
    f.write('total\n')
    for stud_filename in sorted(results.keys()):
        write_student_info(f, stud_filename, results[stud_filename])
    f.close()

def produce_expected_ouput_files (solution_module, io_specs):
    mod= None
    for io_spec in io_specs:
        input = io_spec['input_filename']
        output = io_spec['output_filename']
        mod = run_program(solution_module, input, output, mod)

if __name__ == "__main__":
    # TODO for now only allowing one input file per facet of output.  E.g. If we want to have a grade for the +
    # operation, there is only one input file that will run it and produce the grade for +.   This is probably
    # sufficient for this but ideally a list of input files could be run to test each facet of output.
    io_specs = [{"input_filename": "add_inputs.txt",
                 "output_filename": "add_outputs.txt",
                 "label": "+"
                 },
                {"input_filename": "subtract_inputs.txt",
                 "output_filename": "subtract_outputs.txt",
                 "label":"-"
                 },
                {"input_filename": "mult_inputs.txt",
                 "output_filename": "mult_outputs.txt",
                 "label": "*"
                 },
                {"input_filename": "div_inputs.txt",
                 "output_filename": "div_outputs.txt",
                 "label": "/"
                 },
                {"input_filename": "exp_inputs.txt",
                 "output_filename": "exp_outputs.txt",
                 "label": "**"
                 }
                ]
    solution = "solution" # solution.py is the correct solution
    produce_expected_ouput_files(solution, io_specs)
    grade_file = "grades.csv"
    dir = None # default to cwd for now
    results = cycle_dir(dir, io_specs)
    pprint.pprint(results)
    write_results(results, io_specs, grade_file)