# Galaxy History Evaluator

A command-line tool to assess user's histories on Galaxy, by comparing the history's corresponding workflow with a standard workflow. 
More general use would be to simply compare two Galaxy histories. The Galaxy history is a feature on Galaxy, the bio-data processing platform, which tracks the record of steps of data analysis (including input datasets, tools used, parameters etc.).
The end result is a json file reporting the differences between two histories/workflows.


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

- Unit Tests via `$ unittests` 
- Functional Test via `$ subprocess` 
- Automatically run the test everytime someone pushes or commits to the git repository


Documentation
--------------
Documentation could be found here: https://chensy96.github.io/Galaxy-History-Evaluator/

