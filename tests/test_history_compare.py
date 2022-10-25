import unittest
from ghevaluator.history_compare import *
 

class TestHistCompareMethods(unittest.TestCase):
    def test_get_input_id(self):
        actual = get_input_id({'input1': {'id': 1, 'output_name': 'output1'}, 'input2': {'id': 22, 'output_name': 'output2'}})
        expected = [1, 22]
        self.assertEqual(actual, expected)

    def test_compare(self):
        std = {'a_galaxy_workflow': 'true', 'name': 'galaxy-101visible=true', 'steps': {'0': {'content_id': \
    '__DATA_FETCH__', 'id': 0, 'input_connections': {},'inputs': [], 'name': 'Data Fetch', 'tool_id': '__DATA_FETCH__'}\
    , '1': { 'content_id': '__DATA_FETCH__', 'id': 1, 'input_connections': {}, 'inputs': [], 'name': 'Data Fetch', \
    'tool_id': '__DATA_FETCH__'}, '2': { 'content_id': \
    'toolshed.g2.bx.psu.edu/repos/iuc/bedtools/bedtools_intersectbed/2.30.0', 'id': 2, 'input_connections': {'inputA':\
    {'id': 1, 'output_name': 'output0'}, 'reduce_or_iterate|inputB': {'id': 1, 'output_name': 'output1'}}, 'inputs': []\
    , 'label': None, 'name': 'bedtools Intersect intervals', 'outputs': [{'name': 'output', 'type': 'input'}], \
    'tool_id': 'toolshed.g2.bx.psu.edu/repos/iuc/bedtools/bedtools_intersectbed/2.30.0', 'tool_state': \
    '{"__input_ext": "input", "bed": "false", "header": "false", "split": "false", "strand": "", "__page__": null}',\
    'tool_version': '2.30.0'}, '3': { 'content_id': 'toolshed.g2.bx.psu.edu/repos/iuc/datamash_ops/datamash_ops/1.1.0',\
     'id': 3, 'input_connections': {'in_file': {'id': 2, 'output_name': 'output'}}, 'inputs': [], 'label': None, \
     'name': 'Datamash', 'outputs': [{'name': 'out_file', 'type': 'tabular'}], \
     'tool_id': 'toolshed.g2.bx.psu.edu/repos/iuc/datamash_ops/datamash_ops/1.1.0', 'tool_state': \
     '{"__input_ext": "bed", "grouping": "4", "ignore_case": "false", "__rerun_remap_job_id__": null}', \
     'tool_version':'1.1.0'}}}
        usr = {'a_galaxy_workflow': 'true', 'name': 'Find exons with the highest number', 'steps': {'0': {'content_id': \
    'None', 'id': 0, 'input_connections': {},'inputs': [], 'name': 'Input dataset', 'tool_id': 'None'}\
    , '1': { 'content_id': 'None', 'id': 1, 'input_connections': {}, 'inputs': [], 'name': 'Input dataset', \
    'tool_id': 'None'}, '2': { 'content_id': \
    'toolshed.g2.bx.psu.edu/repos/iuc/bedtools/bedtools_intersectbed/2.30.0', 'id': 2, 'input_connections': {'inputA':\
    {'id': 0, 'output_name': 'output'}, 'reduce_or_iterate|inputB': {'id': 1, 'output_name': 'output'}}, 'inputs': []\
    , 'label': None, 'name': 'bedtools Intersect intervals', 'outputs': [{'name': 'output', 'type': 'input'}], \
    'tool_id': 'toolshed.g2.bx.psu.edu/repos/iuc/bedtools/bedtools_intersectbed/2.30.0', 'tool_state': \
    '{"__input_ext": "bed", "bed": "false", "header": "false", "split": "false", "strand": "", "__page__": null}',\
    'tool_version': '2.30.0'}, '3': { 'content_id': 'toolshed.g2.bx.psu.edu/repos/iuc/datamash_ops/datamash_ops/1.1.0',\
     'id': 3, 'input_connections': {'in_file': {'id': 2, 'output_name': 'output'}}, 'inputs': [], 'label': None, \
     'name': 'Datamash', 'outputs': [{'name': 'out_file', 'type': 'tabular'}], \
     'tool_id': 'toolshed.g2.bx.psu.edu/repos/iuc/datamash_ops/datamash_ops/1.1.0', 'tool_state': \
     '{"__input_ext": "bed", "grouping": "4", "ignore_case": "false", "__rerun_remap_job_id__": null}', \
     'tool_version':'1.1.0'}}}
        temp = compare(std, usr)
        actual = temp['number_of_steps']
        expected = 2
        self.assertEqual(actual, expected)

    def test_input_initialize(self):
        actual = input_initialize()
        expected = {'expected_number_of_inputs': 0, 'user_number_of_inputs': 0, 'status': True}
        self.assertEqual(actual, expected)

    def test_tool_state_initialize(self):
        actual = tool_state_initialize()
        expected = {'expected_value': 0, 'user_value': 0, 'status': True}
        self.assertEqual(actual, expected)

    def test_input_initialize(self):
        actual = tool_id_initialize()
        expected = {'expected_id': 0, 'user_id': 0, 'status': False}
        self.assertEqual(actual, expected)

    def test_tool_dev_initialize(self):
        actual = tool_dev_initialize()
        expected = {'expected_dev': 0, 'user_dev': 0, 'status': False}
        self.assertEqual(actual, expected)

    def test_tool_version_initialize(self):
        actual = tool_version_initialize()
        expected = {'expected_version': 0, 'user_version': 0, 'status': False}
        self.assertEqual(actual, expected)

    def test_inpt_connection_initialize(self):
        actual = inpt_connection_initialize()
        expected = {'expected_input_source': [], 'user_input_source': [], 'status': True}
        self.assertEqual(actual, expected)

    def test_splilt_id(self):
        actual = splilt_id("toolshed.g2.bx.psu.edu/repos/iuc/multiqc/multiqc/1.7")
        expected = ('iuc', 'multiqc', '1.7')
        self.assertEqual(actual, expected)

    def test_count_input_steps(self):
        std_case = {'0': {'id': 0, 'input_connections': {}, 'inputs': [{'description': '', 'name': 'Exons'}], 'label':\
    'Exons', 'name': 'Input dataset', 'outputs': [], 'tool_id': None, 'tool_state': '{"optional": false}',\
    'tool_version': None, 'type': 'data_input'}, '1': {'id': 1, 'input_connections': {}, 'inputs': [{'description': '',\
    'name': 'Features'}], 'label': 'Features', 'name': 'Input dataset', 'outputs': [], 'tool_id': None, 'tool_state':\
     '{"optional": false}', 'tool_version': None, 'type': 'data_input'}}
        usr_case = {'0': {'id': 0, 'input_connections': {}, 'inputs': [{'description': '', 'name': 'Exons'}], 'label':\
     'Exons', 'name': 'Data Fetch', 'outputs': [], 'tool_id': None, 'tool_state': '{"optional": false}', 'tool_version'\
     : None, 'type': 'data_input'}, '1': {'id': 1, 'input_connections': {}, 'inputs': [{'description': '', 'name': \
     'Features'}], 'label': 'Features', 'name': 'Data Fetch', 'outputs': [], 'tool_id': None, 'tool_state': \
     '{"optional\": false}', 'tool_version': None, 'type': 'data_input'}}
        actual = count_input_steps(std_case, usr_case)
        expected = (2, 2)
        self.assertEqual(actual, expected)

    def test_get_all_values(self):
        std = {'0': {'content_id': \
    '__DATA_FETCH__', 'id': 0, 'input_connections': {},'inputs': [], 'name': 'Data Fetch', 'tool_id': '__DATA_FETCH__'}\
    , '1': { 'content_id': '__DATA_FETCH__', 'id': 1, 'input_connections': {}, 'inputs': [], 'name': 'Data Fetch', \
    'tool_id': '__DATA_FETCH__'}, '2': { 'content_id': \
    'toolshed.g2.bx.psu.edu/repos/iuc/bedtools/bedtools_intersectbed/2.30.0', 'id': 2, 'input_connections': {'inputA':\
    {'id': 1, 'output_name': 'output0'}, 'reduce_or_iterate|inputB': {'id': 1, 'output_name': 'output1'}}, 'inputs': []\
    , 'label': None, 'name': 'bedtools Intersect intervals', 'outputs': [{'name': 'output', 'type': 'input'}], \
    'tool_id': 'toolshed.g2.bx.psu.edu/repos/iuc/bedtools/bedtools_intersectbed/2.30.0', 'tool_state': \
    '{"__input_ext": "input", "bed": "false", "header": "false", "split": "false", "strand": "", "__page__": null}',\
    'tool_version': '2.30.0'}, '3': { 'content_id': 'toolshed.g2.bx.psu.edu/repos/iuc/datamash_ops/datamash_ops/1.1.0',\
     'id': 3, 'input_connections': {'in_file': {'id': 2, 'output_name': 'output'}}, 'inputs': [], 'label': None, \
     'name': 'Datamash', 'outputs': [{'name': 'out_file', 'type': 'tabular'}], \
     'tool_id': 'toolshed.g2.bx.psu.edu/repos/iuc/datamash_ops/datamash_ops/1.1.0', 'tool_state': \
     '{"__input_ext": "bed", "grouping": "4", "ignore_case": "false", "__rerun_remap_job_id__": null}', \
     'tool_version':'1.1.0'}}
        usr = {'0': {'content_id': \
    'None', 'id': 0, 'input_connections': {},'inputs': [], 'name': 'Input dataset', 'tool_id': 'None'}\
    , '1': { 'content_id': 'None', 'id': 1, 'input_connections': {}, 'inputs': [], 'name': 'Input dataset', \
    'tool_id': 'None'}, '2': { 'content_id':\
    'toolshed.g2.bx.psu.edu/repos/iuc/bedtools/bedtools_intersectbed/2.30.0', 'id': 2, 'input_connections': {'inputA':\
    {'id': 0, 'output_name': 'output'}, 'reduce_or_iterate|inputB': {'id': 1, 'output_name': 'output'}}, 'inputs': []\
    , 'label': None, 'name': 'bedtools Intersect intervals', 'outputs': [{'name': 'output', 'type': 'input'}], \
    'tool_id': 'toolshed.g2.bx.psu.edu/repos/iuc/bedtools/bedtools_intersectbed/2.30.0', 'tool_state': \
    '{"__input_ext": "bed", "bed": "false", "header": "false", "split": "false", "strand": "", "__page__": null}',\
    'tool_version': '2.30.0'}, '3': { 'content_id': 'toolshed.g2.bx.psu.edu/repos/iuc/datamash_ops/datamash_ops/1.1.0',\
     'id': 3, 'input_connections': {'in_file': {'id': 2, 'output_name': 'output'}}, 'inputs': [], 'label': None, \
     'name': 'Datamash', 'outputs': [{'name': 'out_file', 'type': 'tabular'}], \
     'tool_id': 'toolshed.g2.bx.psu.edu/repos/iuc/datamash_ops/datamash_ops/1.1.0', 'tool_state': \
     '{"__input_ext": "bed", "grouping": "4", "ignore_case": "false", "__rerun_remap_job_id__": null}', \
     'tool_version':'1.1.0'}}
        temp = get_all_values(std, usr)
        self.assertTrue(temp['steps'][0]['tool_used']['expected_value'] == 'bedtools Intersect intervals')

    def test_dict_initialize(self):
        actual = dict_initialize(1)
        expected = "data_inputs"
        self.assertIn(expected, actual)

    def test_check_parameters(self):
        count, current_dict, total_param_tobechecked = check_parameters('{"complement": "", "count": "5", "infile": {"__class__": "RuntimeValue"}, "__page__": null}', \
             '{"__input_ext": "tabular", "complement": "", "count": "5", "infile": null, "__page__": null}', \
             {'param_values': {}, 'param_overall_status': True})
        if count == 1 and "param_values" in current_dict and total_param_tobechecked == 4:
            satisfied = True
        self.assertTrue(satisfied)
