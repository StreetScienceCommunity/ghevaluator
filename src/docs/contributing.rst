Contributing
============

First off, thanks for taking the time to contribute!


This page is intended to let anyone who is interested in contributing to the further development of this tool to know what kind of contribution is needed and how to contribute.


What should I know before I get started?
----------------------------------------

This project is there to offer a compare Galaxy histories to a template workflow.

The original motivation for this tool is to provide a way for student, who creates their new history after learning tutorials on Galaxy training, to evaluate the performance without an instructor.

Currently, this tool still compares one history against one workflow, in order to realize the goal of simply comparing two Galaxy histories, some modifications needed to be done. For examples, the structure of the final report has to be alterd, because currently the tool only tracks which parts of the workflow are missing/wrong in the history. In another word, the workflow is the standard, so if there is a value existing in the history, but not in the workflow, this difference will not be recorded.


The project is developed on GitHub at `https://github.com/StreetScienceCommunity/Galaxy-History-Evaluator <https://github.com/StreetScienceCommunity/Galaxy-History-Evaluator>`_.


How can I contribute?
---------------------

Reporting mistakes or errors
****************************

The easiest way to start contributing is to file an issue to tell us about a spelling mistake or a factual error.

Your first content contribution
*******************************

Once you are feeling more comfortable, you can propose changes via Pull Request.

Indeed, to manage changes, we use `GitHub flow <https://guides.github.com/introduction/flow/>`_ based on Pull Requests:

1. `Create a fork <https://help.github.com/articles/fork-a-repo/>`_ of this repository on GitHub
2. Clone your fork of this repository to create a local copy on your computer
3. Create a new branch in your local copy for each significant change
4. Commit the changes in that branch
5. Push that branch to your fork on GitHub
6. Submit a pull request from that branch to the `master repository <https://github.com/StreetScienceCommunity/Galaxy-History-Evaluator>`_
7. If you receive feedback, make changes in your local clone and push them to your branch on GitHub: the pull request will update automatically

For beginners, the GitHub interface will help you in the process of editing a file. It will automatically create a fork of this repository where you can safely work and then submit the changes as a pull request without having to touch the command line.

Development
-----------

To modify the code and test it locally:

1. Make changes in the `ghevaluator` folder
2. Setup develop mode

   .. code-block:: bash

      $ make develop

3. Run `ghevaluator`

   .. code-block:: bash

      $ ghevaluator ...


Tests
-----

The code and individual functions are covered by tests, using `unittests`.

We also recommend to run them locally before pushing to GitHub with:

.. code-block:: bash

   $ make test


After adding new function or making changes to an existing function, make sure to make changes to the unittest files under the `test` folder.

In addition to unit tests, the overall functionality and the intergration of the tool is tested via `subprocess` under the `integration test` folder. It also runs automatically everytime someone pushes or commits to the git repository.


Documentation
-------------

This documentation is generated using Sphinx.


To update it:

1. Make the changes in `src/docs`
2. Generate the doc with

   .. code-block:: bash

      $ make doc

3. Check it by opening the `docs/index.html` file in a web browser
4. Propose the changes via a Pull Request


For further usages of Sphinx, you may refer to documentation here: https://www.sphinx-doc.org/en/master/
