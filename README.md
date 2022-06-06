# Galaxy-Hisoty-Test-Tool

The current progress:
- connect to the galaxy server
- get (visible and undelete) datasets from a history through a user-provided link
- extract the dataset IDs to a list, and then use this list to extract a workflow.

The current problems of the auto-generated workflow: (as shown in the workflow examples)
- the datasets for "data input" are different and messier than those in the manually extracted workflow.
- There are some duplicated datasets. (should be easily removed)
