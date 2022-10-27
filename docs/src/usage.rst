Usage
=======================

To use this tool, four inputs need to be pass in the command line.

The general structure of the tool, starting with the four inputs on the left, is shown on the graph:

.. image:: pic3.png
   :scale: 70 %
   :align: center



Here are some example inputs, feel free to try out the tool with them):

1. URL to history (the history to be assessed)

.. code-block:: bash

    $ https://usegalaxy.eu/u/siyu_chen/h/assemblyhands-onsiyu-chen

2. URL to workflow (the standard workflow/ extracted workflow from another history)

.. code-block:: bash

    $ https://usegalaxy.eu/training-material/topics/assembly/tutorials/general-introduction/workflows/assembly-general-introduction.ga

3. Galaxy API Key:
	
	To get your own Galaxy API key, follow the instructions below: https://training.galaxyproject.org/training-material/faqs/galaxy/preferences_admin_api_key.html

4. Output Path: (to the root folder of ghevaluator)

.. code-block:: bash

    $ .

To run the program, after installation, simply run the command like followed:

.. code-block:: bash

    $ ghevaluator "https://usegalaxy.eu/u/siyu_chen/h/assemblyhands-onsiyu-chen" "https://usegalaxy.eu/training-material/topics/assembly/tutorials/general-introduction/workflows/assembly-general-introduction.ga" "Dxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    (remember to replace the last argument with your own API key!)
|

The sample final report is of this structure:

.. image:: pic4.png
   :scale: 65 %
   :align: center

.. toctree::
   :maxdepth: 2

