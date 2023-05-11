Galaxy History Evaluator
========================

Galaxy History Evaluator or `ghevaluator` is a command-line Python tool to compare Galaxy histories to a template workflow and generate a JSON report file.

## Context

[Galaxy](https://galaxyproject.org/) is an **open, web-based platform for data-intensive computational research**.

When running their data analysis, Galaxy users create histories storing their data, but also the steps of the data analysis, i.e. the tools used, their versions and parameters.

Galaxy is also used for training where participants follow step-by-step tutorials, stored in Galaxy histories. At the end, participants might want to know if they followed correctly the tutorial and instructors might need to evaluate histories to give feedback and deliver certificates.
**Evaluating histories manually can be painful and error prone**.

Galaxy History Evaluator aims to solve this by providing a command-line tool to compare a Galaxy history to a templare workflow and generate a report in JSON with difference between the provided history and the expected workflow.

## Usage

Galaxy History Evaluator can be used via command-line

```bash
$ ghevaluator --help
usage: ghevaluator [-h] -u HISTORY_URL -w WORKFLOW_URL -a APIKEY [-o OUTPUT]

Compare a Galaxy history to a template workflow and generate a JSON report file

options:
  -h, --help            show this help message and exit
  -u HISTORY_URL, --history_url HISTORY_URL
                        URL to Galaxy history
  -w WORKFLOW_URL, --workflow_url WORKFLOW_URL
                        URL to template workflow
  -a APIKEY, --apikey APIKEY
                        Galaxy API key
  -o OUTPUT, --output OUTPUT
                        Path to output directory
```

## Installation

Galaxy History Evaluator can be installed with pip:

```bash
$ pip install ghevaluator
```

## Tests

1. Export the Galaxy API key as environment variable

  ```bash
  $ export GALAXY_APIKEY = <>
  ```

2. Run the unit tests

  ```bash
  $ make tests
  ```


## Documentation


Documentation could be found at https://streetscience.community/ghevaluator/

To update it:

1. Make the changes in `src/docs`
2. Generate the doc with

    ```bash
    $ make html
    ```