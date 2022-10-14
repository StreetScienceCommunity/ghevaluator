# Galaxy History Evaluator

A command-line tool to assess user's histories on Galaxy, by comparing the history's corresponding workflow with a standard workflow. 
More general use would be to simply compare two Galaxy histories.
The end result is a json file reporting the differences between two histories/workflows.

# Motivation
The Galaxy history is a feature on Galaxy, the bio-data processing platform, which tracks the record of steps of data
analysis (including input datasets, tools used, parameters etc.). The original motivation for this tool is to provide a 
way for student, who creates his or her new history after learning tutorials on Galaxy training, to assess if the steps
in the history matches with the standards of the tutorial. In the later stage of the tool's development, we realized this
tool can also be simply used on comparing any two Galaxy histories, for the purpose of finding the differences, and then
to study the difference. 
 
Galaxy History Evaluator is currently implemented as a command-line tool.

Usage
-----
The command line takes four inputs
- url to history (the history to be assessed)
- url to workflow (the standard workflow/ extracted workflow from another history)
- Galaxy API Key
- Output Path (default to root)

Sample input: "https://usegalaxy.eu/u/siyu_chen/h/assemblyhands-onsiyu-chen" 
"https://usegalaxy.eu/training-material/topics/assembly/tutorials/general-introduction/workflows/assembly-general-introduction.ga" 
"Dxxxxxxxxxxxxxxxxxxxxxxxl"

Installation
-----

```bash
#  Install with pip
pip install ghevaluator
```

Tests
-----

-   Tests via `$ unittests` 
-   Automaticlly run the test everytime someone pushes or commits to the git repository


Documentation
--------------
Documentation could be found here: https://chensy96.github.io/Galaxy-History-Evaluator/

