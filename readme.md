Autograder 

**Setup Instructions:**

1. git clone this repo to an empty dir (e.g. hw-1)

1. Put all the student programs in this directory.

1. Create a JSON rubric and put it in the directory with student programs

1. Run the grader2 program

**Run the program:**

python3 grader2.py -d \<directory> -o \<outputfile> -p \<python-command> -r \<rubricfile>

OPTIONS are switches with arguments as:
- -d --dir: path to directory containing student programs and rubric JSON file.
- -o --outfile: The name of the .csv file you want it to produce (will be put in /reports subdir relative to student files)
- -p --python: The name of your python3.X interpreter (usually python3 or python)
- -r --rubricfile: The filename that contains JSON which defines a grading rubric (see example below)

```
python3 grader2.py -d /path/to/assignment1 -o grades.csv -p python3 -r rubric.json
```
Student python programs should all be in /path/to/assignment1.

All the report files will be placed in /path/to/assignment1/reports
You will find grades.csv, grades.html, and Participant_*.html 

**Configuration**

You need to create a JSON object and place it in a file like rubric.json
that is within the directory where student programs live.

is an example file that goes with the assignment for Clunky Calculator:

This demonstrates only the ability to test a program for its I/O.
You see that each criteria has a set of tests and a test has inputs
coming from a string.  Alternatively you can use input_file: within the
io_test_spec to create a file of inputs.  Providing descriptions is
necessary for generating good report files.  The output_regex is used to
compare the student program output so you need to skip over all the junk
in their output that isn't what you care about.  So for the calculator, all
we care about is whether they produce the correct number.

```
{
    "name": "Clunky Calculator",
    "interpreter": "python3",
    "execution_tests": [
        {
            "facet_name": "+",
            "points": 1,
            "description": "Correctly adds numbers",
            "tests": [
                {
                    "type": "io",
                    "description": "10 + 12 = 22",
                    "io_test_spec": {
                        "input_string": "10\n12\n+\n",
                        "output_regex": ".*22.*"
                    }
                },
                {
                    "type": "io",
                    "description": "5 - 8 = -3",
                    "io_test_spec": {
                        "input_string": "5\n-8\n+\n",
                        "output_regex": ".*-3.*"
                    }
                }
            ]
        },
        {
            "facet_name": "-",
            "points": 1,
            "description": "Correctly subtracts numbers",
            "tests": [
                {
                    "type": "io",
                    "description": "13 - 18 = -5",
                    "io_test_spec": {
                        "input_string": "13\n18\n-\n",
                        "output_regex": ".*-5.*"
                    }
                }
            ]
        },
        {
            "facet_name": "*",
            "points": 1,
            "description": "Correctly multiplies numbers",
            "tests": [
                {
                    "type": "io",
                    "description": "-5 * 10 = -50",
                    "io_test_spec": {
                        "input_string": "-5\n10\n*\n",
                        "output_regex": ".*-50.*"
                    }
                }
            ]
        },
        {
            "facet_name": "/",
            "points": 1,
            "description": "Correctly divides numbers",
            "tests": [
                {
                    "type": "io",
                    "description": "18 / 3 = 6",
                    "io_test_spec": {
                        "input_string": "18\n3\n/\n",
                        "output_regex": ".*6.*"
                    }
                },
                {
                    "type": "io",
                    "description": "10 / 3 = 3.33",
                    "io_test_spec": {
                        "input_string": "10\n3\n/\n",
                        "output_regex": ".*3\\.33.*"
                    }
                }
            ]
        },
        {
            "facet_name": "**",
            "description": "Correctly raises numbers to a power",
            "points": 1,
            "tests": [
                {
                    "type": "io",
                    "description": "-3 ^ 3 = -27",
                    "io_test_spec": {
                        "input_string": "-3\n3\n**\n",
                        "output_regex": ".*-27.*"
                    }
                }
            ]
        }
    ]
}
```

To do unit testing of a student module that contains functions you need to provide unit tests in your facets like:
```
{
    "type": "unit",
    "description": "function add(8,4) returns 12",
    "unit_test_spec": {
        "test_module": "calc_tests.py",
        "tester_function": "test_add",
        "tested_function": "add"
    }
}
```

In the example above, you must write a python file called calc_tests.py and it must contain a function called `test_add`.
The file must be placed in the same directory as the student python files.  
It will test the `add` function within the student module.  Here is what the `test_add` function looks like:

```
file: calc_tests.py

def test_add (add_fn):
    ''' Will be passed the function object for the add function in the student module '''
    return 22 == add_fn(10, 12)
```

So all unit tester_functions are passed the student function object which it can call however it likes as many times as it likes.  It must
return a True/False which indicates if the student function succeeds for this unit test.
