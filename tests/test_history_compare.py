import unittest
import sys
from history_compare import *

class TestCompare(unittest.TestCase):
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
        expected = 1
        self.assertEqual(actual, expected)


class TestGetInputId(unittest.TestCase):
    def test_get_input_id(self):
        actual = get_input_id({'input1': {'id': 1, 'output_name': 'output1'}, 'input2': {'id': 22, 'output_name': 'output2'}})
        expected = [1, 22]
        self.assertEqual(actual, expected)
