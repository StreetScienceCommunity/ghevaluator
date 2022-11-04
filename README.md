# Galaxy History Evaluator

A command-line tool to evaluate user's histories on Galaxy, by comparing the history's corresponding workflow with a standard workflow. 
More general use would be to simply compare two Galaxy histories. The Galaxy history is a feature on Galaxy, the bio-data processing platform, which tracks the record of steps of data analysis (including input datasets, tools used, parameters etc.).
The end result is a json file reporting the differences between two histories/workflows.


Usage
-----
The command line takes four inputs:

-u:  url to history (the history to be evaluated)

-w:  url to workflow (the standard workflow/extracted workflow from another history)

-a:  Galaxy API Key

-p:  Output Path (default to root)


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

