.. Galaxy History Evaluator documentation master file, created by
   sphinx-quickstart on Thu Oct  6 17:32:38 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Galaxy History Evaluator's documentation!
====================================================

A command-line tool to evaluate Galaxy histories, e.g. of participants of a training, by comparing them to a
reference: the workflow of a tutorial, or a reference history such as the tutor's own run of the tutorial.

For each history, it tells which steps are done, missing, run on other inputs or with other settings, which results
were copied from another history, and gives a score. The results are HTML, Markdown and JSON reports, and an overview
when several histories are evaluated. Nothing is created or changed in Galaxy.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage
   how_it_works
   installation
   api_documentation
   contributing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
