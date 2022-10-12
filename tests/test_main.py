import unittest
from main import *

class TestGetHistory(unittest.TestCase):
    def test_get_history(self):
        actual = get_history("https://usegalaxy.eu/u/berenice/h/galaxy-101")
        expected = ('96db5bbbc9a86365', 'galaxy-101')
        self.assertEqual(expected, actual)

class TestGetStandardWorkflow(unittest.TestCase):
    def test_get_standard_workflow(self):
        temp = get_standard_workflow("https://usegalaxy.eu/training-material/topics/introduction/tutorials/galaxy-intro-101/workflows/galaxy-intro-101-workflow.ga")
        actual = temp['name']
        expected = "Find exons with the highest number of features"
        self.assertEqual(expected, actual)

class TestGenerateReportFile(unittest.TestCase):
    def test_generate_report_file(self):
        with open(os.path.join(sys.path[0], "report.json"), "r") as f: standardtemp = f.read()
        actual = standardtemp
        expected = "data_inputs"
        self.assertIn(expected, actual)

class TestGetUserWorkflow(unittest.TestCase):
    def test_get_user_workflow(self):
        actual = get_user_workflow("96db5bbbc9a86365", "galaxy-101", "D4XEpojvk877VKOAtCpu8H2Irdr3kol")
        expected = "a_galaxy_workflow"
        self.assertIn(expected, actual)
