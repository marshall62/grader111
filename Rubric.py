from exc import ConfigurationError
class Rubric():

    def __init__ (self, definition):
        self.definition = definition
        self.validate(definition)

    def validate (self, defn):
        try:
            assert defn['name'] and defn['interpreter'] and defn['execution_tests']
            for et in defn['execution_tests']:
                self.validate_execution_test(et)
        except KeyError as e:
            raise ConfigurationError("Rubric missing required field " + str(e))
        except ConfigurationError:
            raise

    def validate_execution_test (self, test_defn):
        try:
            assert test_defn['facet_name'] and test_defn['points'] and test_defn['tests']
            for ft in test_defn['tests']:
                self.validate_facet_test(ft)
        except KeyError as e:
            raise ConfigurationError("Facet missing required field " + str(e) + "in " + str(test_defn))
        except ConfigurationError:
            raise

    def validate_facet_test (self, facet_test_defn):
        try:
            assert facet_test_defn['type']
            if facet_test_defn['type'] not in ['io', 'unit']:
                raise ConfigurationError("Facet type must be io or unit " + str(facet_test_defn))
            elif facet_test_defn['type'] == 'io':
                assert facet_test_defn['io_test_spec']
                self.validate_io_test_spec(facet_test_defn['io_test_spec'])
        except KeyError as e:
            raise ConfigurationError("Facet missing required field " + str(e) + "in " + str(facet_test_defn))
        except ConfigurationError:
            raise

    def validate_io_test_spec (self, io_test_spec):
        try:
            assert io_test_spec['output_regex']
        except KeyError as e:
            raise ConfigurationError("Facet io_test_spec missing required field " + str(e) + "in " + str(io_test_spec))

    def get_name (self):
        return self.definition['name']

    def get_interpreter (self):
        return self.definition['interpreter']

    def get_test_function_module (self):
        return None

    def get_facet_with_name (self, name):
        for facet in self.get_execution_tests():
            if self.get_facet_name(facet) == name:
                return facet
        return None

    def get_source_code_test (self):
        return None

    def get_execution_tests(self) -> dict:
        '''
        :return: a list of facets
        '''
        return self.definition['execution_tests']

    def get_execution_test_facets (self, execution_test):
        return

    def get_facet_name (self, facet):
        return facet['facet_name']

    def get_facet_description(self, facet):
        return facet.get('description','')

    def get_facet_points(self, facet):
        return facet.get('points',1)

    def get_facet_tests (self, facet):
        return facet['tests']

    def get_facet_test_type (self, facet_test):
        return facet_test['type']

    def get_facet_test_description (self, facet_test):
        return facet_test.get('description','')

    def get_facet_test_points (self, facet_test):
        return facet_test['points']

    def get_facet_test_input_file (self, facet_test):
        return facet_test['io_test_spec'].get('input_filename') # input_filename can be None if no inputs.

    def get_facet_test_input_file (self, facet_test):
        return facet_test['io_test_spec'].get('output_regex') # can be none if we don't want to test outputs (e.g. just see if it runs)