Usage
=====

Galaxy History Evaluator can be used via command-line

.. code-block:: bash

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

The tool needs:

1. URL to the history to be evaluated

    A link with the history id (``/histories/view?id=...`` or ``/published/history?id=...``), or the ``/u/<username>/h/<slug>`` link of a published history, as explained in a `dedicated tutorial <https://training.galaxyproject.org/training-material/faqs/galaxy/histories_sharing.html>`_

    For example: https://usegalaxy.eu/histories/view?id=19b7e0ced2125767

2. A reference, either

    - URL to a reference workflow (``-w``): a workflow file, or a Galaxy workflow link (e.g. ``/published/workflow?id=...`` or ``/u/<username>/w/<slug>``). Links to the workflows of a tutorial are on the tutorial pages of the Galaxy Training website: https://training.galaxyproject.org/

        For example: https://training.galaxyproject.org/training-material/topics/introduction/tutorials/galaxy-intro-short/workflows/Galaxy-Workflow-galaxy-intro-short.ga

    - or URL to a reference history (``-r``). Output formats and the content of the final output are then compared too.

3. Optionally, a Galaxy API key, if the history is not published or shared via link. The key is only sent to the Galaxy server given with ``-g`` (https://usegalaxy.eu by default). Histories on other servers are read without key: give their server with ``-g`` if the key is for that server

    To get your own Galaxy API key, please follow the instructions `here <https://training.galaxyproject.org/training-material/faqs/galaxy/preferences_admin_api_key.html>`_

4. Optionally, the path to the folder where the reports should be created

Examples
--------

Compare a history to the workflow of a `GTN <https://training.galaxyproject.org/>`_ tutorial:

.. code-block:: bash

    $ ghevaluator \
        -u "https://usegalaxy.eu/histories/view?id=19b7e0ced2125767" \
        -w "https://training.galaxyproject.org/training-material/topics/introduction/tutorials/galaxy-intro-short/workflows/Galaxy-Workflow-galaxy-intro-short.ga" \
        -o report

Compare a history to a reference history, e.g. the tutor's own run of the tutorial:

.. code-block:: bash

    $ ghevaluator \
        -u "https://usegalaxy.eu/histories/view?id=892319be4e2b6ca2" \
        -r "https://usegalaxy.eu/histories/view?id=c1ad4cd9d7df4ada" \
        -o report

Compare a history shared only with your account (not published):

.. code-block:: bash

    $ ghevaluator -u "https://usegalaxy.eu/histories/view?id=..." -r "https://usegalaxy.eu/histories/view?id=..." -a $GALAXY_API_KEY -o report

On another Galaxy server, give the server with ``-g`` so the key is sent to it:

.. code-block:: bash

    $ ghevaluator -g https://usegalaxy.org -u "https://usegalaxy.org/histories/view?id=..." -w workflow.ga -a $GALAXY_API_KEY


Several histories
-----------------

Several histories can be evaluated at once with a CSV file (``-c``), e.g. all participants of a training:

.. code-block:: bash

    $ ghevaluator -c histories.csv -a $GALAXY_API_KEY -o reports

The CSV file has one row per history, with these columns (in any order, case does not matter):

=================== ====================== ===============================================================
Column              Other accepted name    Content
=================== ====================== ===============================================================
``student name``    ``student``            name of the student, used for the folder of the reports
``stud hist id``    ``student_history``    id or link of the history to evaluate
``ref hist id``     ``ref_history``        id or link of the reference history, or link of a workflow
``tutorial name``                          optional, shown in the overview and used for the folder
=================== ====================== ===============================================================

For example:

.. code-block:: text

    Tutorial name,Ref hist id,Stud hist id,Student name
    From Peaks to Genes,c1ad4cd9d7df4ada,892319be4e2b6ca2,Participant 1
    Galaxy intro,https://training.galaxyproject.org/training-material/topics/introduction/tutorials/galaxy-intro-short/workflows/Galaxy-Workflow-galaxy-intro-short.ga,19b7e0ced2125767,Participant 1

- History ids are on the Galaxy server given with ``-g``. Links can point to any server.
- Each row has its own reference, so one file can cover several tutorials. A reference is loaded once for all
  its rows. A reference that can not be loaded is tried only once: all its rows get the error.
- Files saved by Excel or Google Sheets work: separated by ``,``, ``;`` (e.g. German Excel) or tabs, in UTF-8 or
  Windows encoding. Rows without student, history or reference are skipped.
- A student can be in several rows, e.g. one per tutorial or several histories for the same tutorial. Each history
  gets its own row in the overview and its own folder: the folder is named after the student and the tutorial,
  with ``_2``, ``_3``, ... for the next histories with the same name. The **History** column of the overview links
  each history, so rows of the same student are told apart.
- A history that can not be evaluated (e.g. wrong link, not shared) gets an error in the overview, and the other
  histories are still evaluated.


Output
------

For each history, the tool generates:

- ``report.html`` and ``report.md`` with a summary in plain sentences, the score, and the comparison of each
  reference step with the matched history step (tool, version, inputs, settings, output formats), the extra steps,
  copied steps and, with a reference history, the comparison of the final output
- ``report.json`` with all the details of the comparison

With a CSV file, the reports of each history are in their own folder, with ``overview.md`` and ``overview.json``
for all histories. ``overview.md`` is a table with, for each history: student, tutorial, history link, step score,
final result, the summary in plain sentences, and the link to the report. It is written after each history, so the
histories already evaluated are kept if the run is interrupted.

How the steps are matched, what counts as done and how the score is computed is explained in :doc:`how_it_works`.
