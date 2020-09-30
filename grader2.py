import os
import sys
import getopt
from collections import defaultdict
from CSVReport import CSVReport
from HTMLReport import HTMLReport
from FacetTester import FacetTester, FacetTestScore
import json
# assume that there is a colocated testdef.py module containing test definition + accessor class

from Rubric import Rubric
from StudentScore import StudentScore


class Grader:

    def __init__ (self, dir='', rubric_definition=None, interpreter='python3', timeout=2, csv_report_file='grades.csv', html_report_file='grades.html'):
        self.dir = dir
        self.results = {}
        self.timeout = timeout
        self.rubric = Rubric(rubric_definition)
        self.student_module = None
        self.interpreter = interpreter
        self.csv_report_file = csv_report_file
        self.html_report_file = html_report_file

    def test_program(self, student_module_filename):
        # facet:  a function of the program to be tested and scored with tests.
        # Scoring is done by determining the percentage of a facet tests that pass and
        # multiplying it by the points available for that facet.
        self.student_module_filename = student_module_filename
        self.student_module_path = os.path.join(self.dir, student_module_filename) # path to student module relative to here.
        score = 0.0
        facet_scores = []
        for facet in self.rubric.get_execution_tests():
            ft = FacetTester(facet, self.student_module_path, self.interpreter, self.timeout )
            facet_score: FacetTestScore = ft.test()
            score += facet_score.points_scored
            # add the facet scoring to the dictionary entry for this student
            facet_scores.append(facet_score)
        score_record = StudentScore(student_module_filename, facet_scores, score)
        self.results[student_module_filename] = score_record
        return score_record


    def cycle_dir (self):
        print("Grading")
        for entry in os.scandir(self.dir):
            if entry.path.endswith(".py") and entry.is_file and \
                entry.name not in ['grader_old.py', 'test.py', 'solution.py', '__init__.py']:
                print(entry.name)
                self.test_program(entry.name)
        print("Done")
        #  Maybe a Reporter becomes an input
        CSVReport(dir=self.dir, filename=self.csv_report_file).report_csv(self.results)
        HTMLReport(dir=self.dir, filename=self.html_report_file, results=self.results, rubric=self.rubric)



    def run (self):
        self.cycle_dir()


def parse_command_args (argv):
    try:
        dir = ''
        outputfile = 'grades.csv'
        interpreter = 'python3'
        rubricfile = 'rubric.json'
        opts, args = getopt.getopt(argv[1:], "hd:o:p:r:", ["dir", "outfile=", "python", "rubricfile="])
    except getopt.GetoptError as e:
        print(e)
        print('grader2.py -d <directory> -o <outputfile> -p <python-command> -r <rubricfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('grader2.py -d <directory> -o <outputfile> -p <python-command> -r <rubricfile>')
            sys.exit()
        elif opt in ("-d", "--dir"):
            dir = arg
        elif opt in ("-o", "--outfile"):
            outputfile = arg
        elif opt in ("-p", "--python"):
            interpreter = arg
        elif opt in ("-r", "--rubricfile"):
            rubricfile = arg
    return dir, outputfile, interpreter, rubricfile


if __name__ == '__main__':
    dir, report_file, interpreter, rubricfile = parse_command_args(sys.argv)
    html_report_file = report_file.split('.')[0] + '.html'
    rubric = json.load(open(os.path.join(dir,rubricfile), 'r'))
    g = Grader(dir=dir,rubric_definition=rubric,interpreter=interpreter)
    g.run()