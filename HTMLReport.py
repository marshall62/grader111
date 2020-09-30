import os
from StudentScore import StudentScore
from Rubric import Rubric
from jinja2 import Environment, FileSystemLoader
import pathlib
import re

def extract_name(path_to_student_module):
    p = '.*Names?\s*:?\s*(?P<name>.*)$'
    with open(path_to_student_module, 'r') as f:
        for line in f:
            m = re.match(p,line)
            if m:
                return m.group(1).strip().replace(',', ' ').replace('<','').replace('>','')
        return None

class IndividualHTMLReport:

    def __init__ (self, dir=''):
        self.dir = dir

    def report_student (self, report_filename, student_name, record: StudentScore, rubric: Rubric):
        env = Environment(loader=FileSystemLoader(os.path.join(pathlib.Path(__file__).parent.absolute(), 'templates')))
        template = env.get_template('report_template.html')
        output_from_parsed_template = template.render(student_name=student_name, score_rec=record, rubric=rubric)
        # to save the results
        with open(report_filename, "w") as fh:
            fh.write(output_from_parsed_template)

    def report (self, results, rubric):
        print("Writing HTML student reports to:",os.path.join(self.dir,'reports'))
        reports = {}
        for student_filename, score_record in results.items():
            report_filename = os.path.join(self.dir,'reports', os.path.splitext(student_filename)[0] + '.html')
            student_name = extract_name(os.path.join(self.dir,student_filename)) or "Name Not Found"
            self.report_student(report_filename, student_name, score_record, rubric)
            reports[student_name or student_filename] = (report_filename, score_record)
        return reports

class HTMLReport:

    def __init__(self, results, rubric, dir='', filename='grades.html'):
        self.dir = dir
        self.report_dir = os.path.join(self.dir, 'reports')
        try:
            if not os.path.isdir(self.report_dir):
                os.mkdir(self.report_dir)
        except OSError:
            print("Creation of the directory %s failed" % self.report_dir)
        self.rubric = rubric
        self.filename = os.path.join(self.report_dir, filename)
        self.indiv_report_table = IndividualHTMLReport(dir).report(results,rubric)
        self.report_table()

    def report_table(self):
        env = Environment(loader=FileSystemLoader(os.path.join(pathlib.Path(__file__).parent.absolute(), 'templates')))
        template = env.get_template('table_report_template.html')
        output_from_parsed_template = template.render(data=self.indiv_report_table, rubric=self.rubric)
        print("Writing Overall HTML report to", self.filename)
        with open(self.filename, "w") as fh:
            fh.write(output_from_parsed_template)