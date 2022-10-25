import os
import subprocess
import os.path
import sys
tdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\ghevaluator'))
sys.path.insert(1, tdir)

subprocess.check_call(
    ['python', 'ghevaluator/main.py',
     'https://usegalaxy.eu/u/siyu_chen/h/assemblyhands-onsiyu-chen',
     'https://usegalaxy.eu/training-material/topics/assembly/tutorials/general-introduction/workflows/assembly-general-introduction.ga',
     'D4XEpojvk877VKOAtCpu8H2Irdr3kol'])
assert os.path.exists('./report.json')


