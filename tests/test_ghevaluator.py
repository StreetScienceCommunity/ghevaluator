import unittest
import os.path
import sys
tdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../ghevaluator'))
sys.path.insert(1, tdir)
import ghevaluator_main

class TestMainMethods(unittest.TestCase):
    def test_get_history(self):
        actual = ghevaluator_main.get_history("https://usegalaxy.eu/u/berenice/h/galaxy-101")
        expected = ('96db5bbbc9a86365', 'galaxy-101')
        self.assertEqual(expected, actual)

    def test_get_user_workflow(self):
        actual = ghevaluator_main.get_user_workflow("96db5bbbc9a86365", "galaxy-101", "D4XEpojvk877VKOAtCpu8H2Irdr3kol")
        expected = "a_galaxy_workflow"
        self.assertIn(expected, actual)

    def test_get_standard_workflow(self):
        stdwf = ghevaluator_main.get_standard_workflow("https://usegalaxy.eu/training-material/topics/assembly/tutorials/general-introduction/workflows/assembly-general-introduction.ga")
        actual = stdwf['name']
        expected = 'Intro to Genome Assembly'
        self.assertEqual(expected, actual)

