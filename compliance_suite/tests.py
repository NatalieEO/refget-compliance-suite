from info_algorithms import *
from metadata_algorithms import *
from sequence_algorithms import *


class Test():
    '''
    Test Case class. All the test cases are intances of this class.

    label - used in graph algorithms to label the test case graph
    alogorithm - Strategy design pattern in used here. It is the underlying algorithm used in the test case
    result - 0 indicates skipped, 1 indicates passed, -1 indicates failed and 2 is not yet ran
    pass_text - text in the report when test case is passed
    skip_text - text in the report when test case is skipped
    fail_text - text in the report when test case is failed
    parents - dependencies of the test case to run
    children - test cases which have this test case as dependency
    warning - if the result of this test case is warning for the server implementation
    cases - multiple edge cases of same test object
    '''
    def __init__(self, algorithm):
        '''
        Initiates the Test Case object. Algorithm is a required field to initiate test case object
        '''
        self.label = 0
        self.algorithm = algorithm
        self.result = 2
        self.pass_text = ''
        self.fail_text = ''
        self.skip_text = ''
        self.parents = []
        self.children = []
        self.warning = False
        self.cases = []
        self.case_ouputs = []

    def __str__(self):
        '''
        String repr of the test case
        '''
        return 'test_' + self.algorithm.__name__

    def set_pass_text(self, text):
        '''
        Setter for pass_text
        '''
        self.pass_text = text

    def set_fail_text(self, text):
        '''
        Setter for fail_text
        '''
        self.fail_text = text

    def set_skip_text(self, text):
        '''
        Setter for skip_text
        '''
        self.skip_text = text

    def generate_skip_text(self):
        '''
        Skip text is generated if there is no skip text (the case when test is skipped when the parent test cases fail or skip)
        To track down the root cause of this skip.
        '''
        text = str(self) + ' is skipped because' + '\n'
        for test in self.parents:
            if test.result != 1:
                text = text + '\t' + test.toecho()
        return text

    def add_parent(self, parent_test_case):
        '''
        Adds a parent test case
        '''
        self.parents.append(parent_test_case)

    def add_child(self, child_test_case):
        '''
        Adds a child test case
        '''
        self.children.append(child_test_case)
        child_test_case.add_parent(self)

    def toskip(self):
        '''
        Checks if any of the parent test cases failed or skipped which causes this case to skip
        '''
        for test in self.parents:
            if test.result != 1:
                return True
        return False

    def run(self, test_runner):
        '''
        First checks if the parent test cases were successful then run the text.
        '''
        # Checking if to skip
        if self.toskip() is True:
            # warning will be generated because the test case is skipped because of some parent failure
            self.warning = True
            self.result = 0
            return
        # run the test if not skipped
        self.algorithm(self, test_runner)
        # if it fails it'll generate a warning
        if self.result == -1:
            self.warning = True

    def toecho(self):
        '''
        Returns the text based on the result of the test case
        '''
        if self.result == 1:
            return self.pass_text
        elif self.result == -1:
            return self.fail_text
        elif self.skip_text == '':
            self.skip_text = self.generate_skip_text()
        return self.skip_text


def initiate_tests():
    '''
    Initiates test case objects and generates a test case graph for execution
    '''

    def base_algorithm(test, runner):
        if True is True:
            test.result = 1

    # Base test case
    test_base = Test(base_algorithm)

    # Info Success Test Cases

    test_info_implement = Test(info_implement)
    test_info_implement.set_pass_text('Info endpoint implemented by the server')
    test_info_implement.set_fail_text('Info endpoint not implemented by the server')

    test_info_implement_default = Test(info_implement_default)
    test_info_implement_default.set_pass_text('Info endpoint implemented with default encoding')
    test_info_implement_default.set_fail_text('Info endpoint not implemented with default encoding')

    test_info_circular = Test(info_circular)
    test_info_circular.set_pass_text('"circular" key in info response object')
    test_info_circular.set_fail_text('"circular" key not in info response object instead sends ')

    test_info_algorithms = Test(info_algorithms)
    test_info_algorithms.set_pass_text('"algorithms" key in info response object')
    test_info_algorithms.set_fail_text('"algorithms" key not in info response object instead sends ')

    test_info_subsequence_limit = Test(info_subsequence)
    test_info_subsequence_limit.set_pass_text('"subsequence_limit" key in info response object')
    test_info_subsequence_limit.set_fail_text('"subsequence_limit" key not in info response object instead sends ')

    test_info_api_version = Test(info_api_version)
    test_info_api_version.set_pass_text('"supported_api_versions" key in info response object')
    test_info_api_version.set_fail_text('"supported_api_versions" key not in info response object instead sends ')

    # Metadata Success Test Cases

    test_metadata_implement = Test(metadata_implement)
    test_metadata_implement.set_pass_text('Metadata endpoint implemented by the server')
    test_metadata_implement.set_fail_text('Metadata endpoint not implemented by the server')

    test_metadata_implement_default = Test(metadata_implement_default)
    test_metadata_implement_default.set_pass_text('Metadata endpoint implemented with default encoding')
    test_metadata_implement_default.set_fail_text('Metadata endpoint not implemented with default encoding')

    test_metadata_query_by_trunc512 = Test(metadata_query_by_trunc512)
    test_metadata_query_by_trunc512.set_pass_text('TRUNC512 algorithm is working in the server for metadata endpoint')
    test_metadata_query_by_trunc512.set_fail_text('TRUNC512 algorithm is not working in the server for metadata endpoint even though info endpoint indicates it"s support')

    test_metadata_query_circular_sequence = Test(metadata_query_circular_sequence)
    test_metadata_query_circular_sequence.set_pass_text('Circular sequence metadata can be retrived')
    test_metadata_query_circular_sequence.set_fail_text('Circular sequence metadata can not be retrived even though info endpoint indicates it"s support')

    test_metadata_md5 = Test(metadata_md5)
    test_metadata_md5.set_pass_text('"md5" key in metadata response object')
    test_metadata_md5.set_fail_text('"md5" key not in metadata response object instead sends ')

    test_metadata_trunc512 = Test(metadata_trunc512)
    test_metadata_trunc512.set_pass_text('"trunc512" key in metadata response object')
    test_metadata_trunc512.set_fail_text('"trunc512" key not in metadata response object even though info endpoint indicates it"s support instead sends ')

    test_metadata_length = Test(metadata_length)
    test_metadata_length.set_pass_text('"length" key in metadata response object')
    test_metadata_length.set_fail_text('"length" key not in metadata response object or incorrect value in "length" key instead sends ')

    test_metadata_aliases = Test(metadata_aliases)
    test_metadata_aliases.set_pass_text('"aliases" key in metadata response object')
    test_metadata_aliases.set_fail_text('"aliases" key not in metadata response object')

    test_metadata_invalid_checksum_404_error = Test(metadata_invalid_checksum_404_error)
    test_metadata_invalid_checksum_404_error.set_pass_text('Server is correctly sending 404 on invalid checksum')
    test_metadata_invalid_checksum_404_error.set_fail_text('Server is not sending 404 on invalid checksum instead sends ')

    test_metadata_invalid_encoding_415_error = Test(metadata_invalid_encoding_415_error)
    test_metadata_invalid_encoding_415_error.set_pass_text('Server is correctly sending 415 on invalid encoding')
    test_metadata_invalid_encoding_415_error.set_fail_text('Server is not sending 415 on invalid encoding instead sends ')

    # Sequence endpoint test cases

    test_sequence_implement = Test(sequence_implement)
    test_sequence_implement.set_pass_text('Sequence endpoint implemented in the server')
    test_sequence_implement.set_fail_text('Sequence endpoint not implemented in the server')

    test_sequence_implement_default = Test(sequence_implement_default)
    test_sequence_implement_default.set_pass_text('Sequence endpoint implemented with default encoding')
    test_sequence_implement_default.set_fail_text('Sequence endpoint not implemented with default encoding')

    test_sequence_query_by_trunc512 = Test(sequence_query_by_trunc512)
    test_sequence_query_by_trunc512.set_pass_text('TRUNC512 algorithm is working in the server for sequence endpoint')
    test_sequence_query_by_trunc512.set_fail_text('TRUNC512 algorithm is not working in the server for sequence endpoint even though info endpoint indicates it"s support')

    test_sequence_invalid_checksum_404_error = Test(sequence_invalid_checksum_404_error)
    test_sequence_invalid_checksum_404_error.set_pass_text('Server is correctly sending 404 on invalid checksum')
    test_sequence_invalid_checksum_404_error.set_pass_text('Server is not sending 404 on invalid checksum instead sends ')

    test_sequence_invalid_encoding_415_error = Test(sequence_invalid_encoding_415_error)
    test_sequence_invalid_encoding_415_error.set_pass_text('Server is correctly sending 415 on invalid encoding')
    test_sequence_invalid_encoding_415_error.set_pass_text('Server is not sending 415 on invalid encoding instead sends ')

    test_sequence_start_end = Test(sequence_start_end)
    test_sequence_start_end.set_pass_text('Server supports start end query params')
    test_sequence_start_end.set_fail_text('Server does not support start end query params')

    test_sequence_start_end_success_cases = Test(sequence_start_end_success_cases)
    test_sequence_start_end_success_cases.set_pass_text('Server passed all the success edge cases with start end query params')
    test_sequence_start_end_success_cases.set_fail_text('Server did not pass all the success edge cases with start end query params')
    test_sequence_start_end_success_cases.cases = [
        (['?start=10&end=10', 10, 10], 0),
        (['?start=10&end=20', 10, 20], 10),
        (['?start=10&end=11', 10, 11], 1),
        (['?start=230208', 230208, None], 10),
        (['?end=5', None, 5], 5),
        (['?start=230217&end=230218'], 1),
        (['?start=0', 0, None], 230218),
        (['?&end=230218', None, 230218], 230218),
        (['?start=0&end=230218', 0, 230218], 230218),
        (['?start=1&end=230218', 1, 230218], 230217),
        (['?start=230217', 230217, None], 1),
        (['?end=0', None, 0], 0)
    ]

    test_sequence_range = Test(sequence_range)
    test_sequence_range.set_pass_text('Server supports range header')
    test_sequence_range.set_fail_text('Server does not support range header')

    test_sequence_range_success_cases = Test(sequence_range_success_cases)
    test_sequence_range_success_cases.set_pass_text('Server passed all the success edge cases with range header query')
    test_sequence_range_success_cases.set_fail_text('Server did not pass all the success edge cases with range header query')
    test_sequence_range_success_cases.cases = [
        (['bytes=10-19', 10, 19], [206, 10]),
        (['bytes=10-230217', 10, 230217], [206, 230208]),
        (['bytes=10-999999', 10, 999999], [206, 230208]),
        (['bytes=0-230217', 0, 230217], [200, 230218]),
        (['bytes=0-999999', 0, 999999], [200, 230218]),
        (['bytes=0-0', 0, 0], [206, 1]),
        (['bytes=230217-230217', 230217, 230217], [206, 1])
    ]

    # test_sequence_circular = Test(sequence_circular)
    # test_sequence_circular.set_pass_text('Circular sequence can be rertieved successfully passing all the edge cases')
    # test_sequence_circular.set_fail_text('Circular sequences can not be retreived even though info endpoint indicates its support')
    # test_sequence_cirular.cases = [
    #     ('?start=5374&end=5', ['ATCCAACCTGCAGAGTT', 17]),
    #     ('?start=5374&end=0', ['ATCCAACCTGCA', 12]),
    #     ('?start=5380&end=25', ['CCTGCAGAGTTTTATCGCTTCCATGACGCAG', 31]),
    # ]


    # generating test graph

    test_base.add_child(test_info_implement)

    test_info_implement.add_child(test_info_implement_default)
    test_info_implement.add_child(test_info_circular)
    test_info_implement.add_child(test_info_algorithms)
    test_info_implement.add_child(test_info_subsequence_limit)
    test_info_implement.add_child(test_info_api_version)

    test_base.add_child(test_metadata_implement)

    test_metadata_implement.add_child(test_metadata_implement_default)

    test_metadata_implement.add_child(test_metadata_query_by_trunc512)
    test_info_algorithms.add_child(test_metadata_query_by_trunc512)

    test_metadata_implement.add_child(test_metadata_query_circular_sequence)
    test_info_circular.add_child(test_metadata_query_circular_sequence)

    test_metadata_implement.add_child(test_metadata_md5)

    test_metadata_implement.add_child(test_metadata_trunc512)
    test_info_algorithms.add_child(test_metadata_trunc512)

    test_metadata_implement.add_child(test_metadata_length)
    test_metadata_implement.add_child(test_metadata_aliases)
    test_metadata_implement.add_child(test_metadata_invalid_checksum_404_error)
    test_metadata_implement.add_child(test_metadata_invalid_encoding_415_error)

    test_base.add_child(test_sequence_implement)

    test_sequence_implement.add_child(test_sequence_implement_default)
    test_sequence_implement.add_child(test_sequence_start_end)
    test_sequence_implement.add_child(test_sequence_range)

    test_sequence_implement.add_child(test_sequence_query_by_trunc512)
    test_info_algorithms.add_child(test_sequence_query_by_trunc512)

    test_sequence_implement.add_child(test_sequence_invalid_checksum_404_error)
    # test_sequence_implement.add_child(test_sequence_invalid_encoding_415_error)

    # test_sequence_start_end.add_child(test_sequence_start_end_success_cases)
    test_sequence_range.add_child(test_sequence_range_success_cases)

    return test_base
