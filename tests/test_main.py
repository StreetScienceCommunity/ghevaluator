import unittest
import sys
sys.path.insert(1, '/ghevaluator/') 
from main import *

class TestGetHistory(unittest.TestCase):
    def test_get_history(self):
        actual = get_history("https://usegalaxy.eu/u/berenice/h/galaxy-101")
        expected = ('96db5bbbc9a86365', 'galaxy-101')
        self.assertEqual(expected, actual)


class TestGetUserWorkflow(unittest.TestCase):
    def test_get_user_workflow(self):
        actual = get_user_workflow("96db5bbbc9a86365", "galaxy-101", "D4XEpojvk877VKOAtCpu8H2Irdr3kol")
        expected = "a_galaxy_workflow"
        self.assertIn(expected, actual)
