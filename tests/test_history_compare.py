import unittest
import sys
from history_compare import *

def add_fish_to_aquarium(fish_list):
    if len(fish_list) > 10:
        raise ValueError("A maximum of 10 fish can be added to the aquarium")
    return {"tank_a": fish_list}


class TestAddFishToAquarium(unittest.TestCase):
    def test_add_fish_to_aquarium_success(self):
        actual = add_fish_to_aquarium(fish_list=["shark", "tuna"])
        expected = {"tank_a": ["shark", "tuna"]}
        self.assertEqual(actual, expected)


class TestGetInputId(unittest.TestCase):
    def test_get_input_id(self):
        actual = get_input_id({'input1': {'id': 1, 'output_name': 'output1'}, 'input2': {'id': 22, 'output_name': 'output2'}})
        expected = [1, 22]
        self.assertEqual(actual, expected)
