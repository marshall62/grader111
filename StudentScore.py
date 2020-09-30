class StudentScore:
    def __init__ (self, name, facet_scores, score):
        self.facet_score_list = facet_scores
        self.student_filename = name
        self.total_score = score