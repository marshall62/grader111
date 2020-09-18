Autograder 

**Setup Instructions:**

git clone this repo to an empty dir (e.g. hw-1)

**Create input files that define program inputs and expected outputs.**

View the *_inputs.txt files to make sure these are inputs you want to run the program
with.  

Provide a solution program (must be called solution.py).  It takes
its inputs from the input files and will produce the expected output files
 which will be used to grade each student program's outputs.
 
**Note:  MAKE SURE YOUR SOLUTION PROGRAM'S OUTPUT EXACTLY MATCHES WHAT YOU DESCRIBE IN INSTRUCTIONS
YOU HAVE PROVIDED TO STUDENTS!!!!**   

Note: There is very little leeway for student programs to deviate from the
expected outputs produced by solution.py.  We simply remove 
some trailing whitespace.  More work necessary to provide flexibility.


**Place student programs**
Put all the student programs in this directory.

**Run the program:**

python3 grader.py

If all goes well the results will be the file grades.csv

**Configuration**

Note that in the bottom of the program (grader.py) there is some setup
which builds a dictionary using these input and output files and defining a label 
for each column in the report that will be output.

It looks like:
```
io_specs = [{"input_filename": "add_inputs.txt", 
             "output_filename": "add_outputs.txt",
             "label": "+"},
            {"input_filename": "subtract_inputs.txt", 
             "output_filename": "subtract_outputs.txt",
             "label": "-"},
 ...
]   
```
The grader will use each pair of input/output file to test the student program.
A grade of 1 or 0 will be given depending on whether the student program matches
the output file.  The spreadsheet will be labeled with columns taken from each
io spec to yield something like:
program name,+,-,*,/,**,
stud1.py,1,1,1,1,1,
...

