Contributing
=======================
This page is intended to let anyone who is interested in contributing to the further development of this tool to know what kind of contribution is needed and how to contribute.


------------

**Development Process and Current Status**

The original motivation for this tool is to provide a way for student, who creates his or her new history after learning tutorials on Galaxy training, to evaluate the performance without an instructor. In the later stage of the tool's development, we realized this tool can also be simply used on comparing any two Galaxy histories, for the purpose of finding the differences, and then to study the difference.

For the original motivation mentioned above, this tool is used on DNAnalyzer: 
https://github.com/StreetScienceCommunity/DNAnalyzer
for evaluating user's results' in the BeerDEcoded part:


Currently, this tool still compares one history against one workflow, in order to realize the goal of simply comparing two Galaxy histories, some modifications needed to be done. For examples, the structure of the final report has to be alterd, because currently the tool only tracks which parts of the workflow are missing/wrong in the history. In another word, the workflow is the standard, so if there is a value existing in the history, but not in the workflow, this difference will not be recorded.


------------

**How to contribute:**

Feel free to clone, fork, open pull requests or issues to the git repository: https://github.com/chensy96/Galaxy-History-Evaluator



------------

**Testing**

Test for individual function is done via `unittests`. It automatically runs the tests everytime someone pushes or commits to the git repository.
After adding new function or making changes to an existing function, make sure to make changes to the unittest files under the `test` folder.

Test for the overall functionality and the intergration of the tool is done via `subprocess` under the `intergration test` folder. It also runs automatically everytime someone pushes or commits to the git repository.


------------

**Documentation**

This documentation is generated using Sphinx. 
If you wish to make descriptional changes to the documentation, you just need to alter the `rst` files in the `docs/src/` folder, and then run `make html` to generate the new documentation. Pushing the new documentation to the `docs/` folder in Git Repository will trigger the Git Page to update automatically. 

Also, if the source code(the key python modules) has been changed, then you need to run `sphinx-apidoc` to generate new `rst` files, before doing the steps described above.

For further usages of Sphinx, you may refer to documentation here: https://www.sphinx-doc.org/en/master/

.. toctree::
   :maxdepth: 2

