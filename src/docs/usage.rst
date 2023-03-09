Usage
=====

Galaxy History Evaluator can be used via command-line

.. code-block:: bash

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
                            Path to output report



This tool needs then 4 inputs:

1. URL to history to be evaluated

    To get the URL, you need to publish your history and get the `Share Link` URL as explained in a `dedicated tutorail <https://training.galaxyproject.org/training-material/faqs/galaxy/histories_sharing.html>`_

    For example you can use: https://usegalaxy.eu/u/siyu_chen/h/assemblyhands-onsiyu-chen

2. URL to the reference workflow

    To get the link, you can apply the same approach as for history but for workflow. You can also find link to reference workflow for tutorial directly in tutorial pages, you need to go on the Galaxy Training website: https://training.galaxyproject.org/, and then find the corresponding tutorial to your history.

    For example, you can use: https://usegalaxy.eu/training-material/topics/assembly/tutorials/general-introduction/workflows/assembly-general-introduction.ga


3. Galaxy API Key for the Galaxy server where the history is available

    To get your own Galaxy API key, please follow the instructions `here <https://training.galaxyproject.org/training-material/faqs/galaxy/preferences_admin_api_key.html>`_


4. Path to where the report file should be created


Output
------

The tool will generated a JSON file that will look like:

.. code-block:: bash

    TO FILL

