import subprocess
import os.path
import json

# check the program with a perfect history following beerdecoded tutorial
subprocess.check_call(
    ['python', 'ghevaluator/ghevaluator_main.py',
     'https://usegalaxy.eu/u/siyu_chen/h/beerdecoded',
     'https://training.galaxyproject.org/training-material/topics/metagenomics/tutorials/beer-data-analysis/workflows/main_workflow.ga',
     'D4XEpojvk877VKOAtCpu8H2Irdr3kol'])
f = open('report.json', 'r')
report_str = f.read()
actual = json.loads(report_str)
assert actual['number_of_wrong_steps'] == 0

# check the program with a false history following beerdecoded tutorial
subprocess.check_call(
    ['python', 'ghevaluator/ghevaluator_main.py',
     'https://usegalaxy.eu/u/siyu_chen/h/blankhisotrytry',
     'https://training.galaxyproject.org/training-material/topics/metagenomics/tutorials/beer-data-analysis/workflows/main_workflow.ga',
     'D4XEpojvk877VKOAtCpu8H2Irdr3kol'])
f = open('report.json', 'r')
report_str = f.read()
actual = json.loads(report_str)
assert actual['number_of_wrong_steps'] == 6
