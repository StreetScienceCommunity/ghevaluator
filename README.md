Galaxy History Evaluator
========================

Galaxy History Evaluator or `ghevaluator` is a command-line Python tool to compare Galaxy histories to a reference, a workflow file or another history, and generate JSON, HTML and Markdown reports.

## Context

[Galaxy](https://galaxyproject.org/) is an **open, web-based platform for data-intensive computational research**.

When running their data analysis, Galaxy users create histories storing their data, but also the steps of the data analysis, i.e. the tools used, their versions and parameters.

Galaxy is also used for training where participants follow step-by-step tutorials, stored in Galaxy histories. At the end, participants might want to know if they followed correctly the tutorial and instructors might need to evaluate histories to give feedback and deliver certificates.
**Evaluating histories manually can be painful and error prone**.

Galaxy History Evaluator aims to solve this by providing a command-line tool to compare Galaxy histories to a reference and generate reports with the differences.

## Usage

```bash
$ ghevaluator --help
usage: ghevaluator [-h] [-u HISTORY_URL] [-w WORKFLOW_URL | -r REFERENCE_HISTORY_URL] [-c CSV]
                   [-g GALAXY_URL] [-a APIKEY] [-o OUTPUT]

Compare Galaxy histories to a reference workflow or history and generate JSON, HTML and Markdown
reports

options:
  -h, --help            show this help message and exit
  -u HISTORY_URL, --history_url HISTORY_URL
                        URL to Galaxy history
  -w WORKFLOW_URL, --workflow_url WORKFLOW_URL
                        URL to reference workflow: a workflow file (.ga) or a Galaxy workflow link
  -r REFERENCE_HISTORY_URL, --reference_history_url REFERENCE_HISTORY_URL
                        URL to reference Galaxy history
  -c CSV, --csv CSV     CSV file with several histories to evaluate, with columns 'student name',
                        'stud hist id', 'ref hist id' and optional 'tutorial name' (ids or URLs)
  -g GALAXY_URL, --galaxy_url GALAXY_URL
                        Galaxy server of the API key, also used for history ids in the CSV file.
                        The API key is only sent to this server (default: https://usegalaxy.eu)
  -a APIKEY, --apikey APIKEY
                        Galaxy API key of an account on the --galaxy_url server, needed for
                        histories shared with a specific account, not for published histories or
                        histories shared via link
  -o OUTPUT, --output OUTPUT
                        Path to output folder (default: current folder)
```

Compare a history to the workflow of a [GTN](https://training.galaxyproject.org/) tutorial:

```bash
$ ghevaluator \
    -u "https://usegalaxy.eu/histories/view?id=19b7e0ced2125767" \
    -w "https://training.galaxyproject.org/training-material/topics/introduction/tutorials/galaxy-intro-short/workflows/Galaxy-Workflow-galaxy-intro-short.ga" \
    -o report
```

Compare a history to a reference history:

```bash
$ ghevaluator \
    -u "https://usegalaxy.eu/histories/view?id=892319be4e2b6ca2" \
    -r "https://usegalaxy.eu/histories/view?id=c1ad4cd9d7df4ada" \
    -o report
```

Evaluate several histories listed in a CSV file, e.g. all participants of a training:

```csv
Tutorial name,Ref hist id,Stud hist id,Student name
From Peaks to Genes,c1ad4cd9d7df4ada,892319be4e2b6ca2,Participant 1
```

```bash
$ ghevaluator -c histories.csv -a $GALAXY_API_KEY -o reports
```

The reports of each history are written in a folder named after the student, with an `overview.md` and `overview.json` of all histories.

History URLs can be links with the history id (`/histories/view?id=...`, `/published/history?id=...`) or `/u/<username>/h/<slug>` links of published histories. Histories have to be accessible to the API key owner, e.g. shared with them, or published. The API key is only sent to the Galaxy server given with `-g` (https://usegalaxy.eu by default), so a link to another server in the CSV file can not get the key: histories on other servers are read without key, which works for published histories and histories shared via link. Reference workflows can also be Galaxy workflow links (`/published/workflow?id=...` or `/u/<username>/w/<slug>`). Nothing is created or changed in Galaxy.

### What is compared

- **Steps**: steps of the history are matched to the steps of the reference by tool and by the steps their inputs come from, not by their order. Steps run again, run in another order or not in the reference are handled. For each reference step, the report gives the matched history step, the tool version, the parameters and whether each input comes from the right step (swapped inputs are different). Datasets and collection element names are not compared as parameters.
- **Missing and extra steps**: reference steps not found in the history, and history steps not in the reference. Steps whose outputs were all deleted are reported but not counted as extra steps; a finished run whose outputs were deleted still counts as done (and is flagged), a cancelled job does not. Failed or unfinished steps do not count as done; a step run over a collection is failed when all its elements failed, and partly failed steps are reported with the number of failed elements. Steps the tutor threw away in a reference history (failed, or attempts replaced by another run of the tool: all outputs deleted and not used later) are not asked from the students. A deleted final result without another run is still asked.
- **Copied results**: steps whose job ran in another history, i.e. results copied from someone else's history, and steps whose job can not be read, usually because it ran in someone else's private history. For each copied step, the report says whether the job was run by the owner of the history (copied from their own other history) or by another user, without saying who. When no step ran in the history itself, the report says so, names the history where most steps ran and whether it is a copy of the same or another user: this is expected for a history imported by a tutor, not for a history shared by a student.
- **Job cache**: steps whose result was reused from an earlier job.
- **Outputs** (reference history only): output formats of matched steps, and the last step of the reference compared to the last 5 steps of the history (by job end time), including the similarity of the output content for text datasets.

### Score

Every step of the reference is worth 100 points. A step done in the history gets 50 points, 25 more if it was run on the same inputs as in the reference, and up to 25 more for the same settings (each setting counts the same, so 1 different setting out of 4 costs 6.25 points). A missing step gets 0 points. The step score is the average over all steps of the reference. A different tool version is shown but does not lower the score.

## Installation

Galaxy History Evaluator can be installed with pip:

```bash
$ pip install ghevaluator
```

## Tests

```bash
$ make test
```

Most tests run offline on histories saved in `tests/data/histories`. A few tests read public histories on usegalaxy.eu and the GTN, and need internet access but no API key.


## Documentation


Documentation could be found at https://streetscience.community/ghevaluator/

To update it:

1. Make the changes in `src/docs`
2. Generate the doc with

    ```bash
    $ make doc
    ```