from FacetTester import FacetTestScore
from StudentScore import StudentScore
from HTMLReport import extract_name
from typing import List
import os

class CSVReport:

    def __init__ (self, dir='', filename='grades.csv'):
        self.dir = dir
        self.report_dir = os.path.join(dir,'reports')
        try:
            if not os.path.isdir(self.report_dir):
                os.mkdir(self.report_dir)
        except OSError:
            print("Creation of the directory %s failed" % self.report_dir)
        self.filename = os.path.join(self.report_dir,filename)


    def sort_facets (self, facet_tests) -> List[FacetTestScore] :
        return sorted(facet_tests, key=lambda x: x.facet['facet_name'])

    def get_student_name (self, score_rec):
        fn = score_rec.student_filename
        path_to_mod = os.path.join(self.dir, fn)
        stud_name = extract_name(path_to_mod) or "Name not found"
        return stud_name

    def report_csv (self, results):
        '''
        Process the results dictionary and produce a report.
        Results dictionary is structured with keys that are the filenames of
        student programs.   The values are a list of tuples where each tuple is:
        (facet-name, FacetTestScore)
        :param results:
        :return:
        '''

        sorted_keys = sorted(results.keys()) # keys are student filenames, value is StudentScore object
        col_header = 'student name, module tested'
        first_score_rec: StudentScore = results[sorted_keys[0]]
        facet_entries: List[FacetTestScore] = first_score_rec.facet_score_list
        for facet_entry in self.sort_facets(facet_entries):
            facet = facet_entry.facet
            col_header += ',' + facet['facet_name']
        col_header += ',total\n'
        with open(self.filename,'w') as self.report_file:
            print("Writing CSV report to ", self.filename)
            self.report_file.write(col_header)
            for k in sorted_keys:
                score_rec: StudentScore = results[k]
                stud_name = self.get_student_name(score_rec)
                line = f'{stud_name}, {k}'
                score_total = 0
                for facet_score_info in self.sort_facets(score_rec.facet_score_list):
                    line += ',' + str(facet_score_info.points_scored)
                    score_total += facet_score_info.points_scored
                line += ',' + str(score_total) + '\n'
                self.report_file.write(line)
