# Galaxy-History-Test-Tool

The current progress:

# In the main.py file:
- connect to the galaxy server
- get (visible and undelete) datasets from a history through a user-provided link
- extract the dataset IDs to a list, and then use this list to extract a workflow.
- download the standard workflow of the tutorial through a hard-coded link, and store it as a dictionary.
- Compare the two workflows

# In the history_compare.py file:
can check:
1. if the tools (steps) in standard workflow/tutorials were carried out.
2. if the parameters are correct (a rough version).

# The current problems:
- (solved) the datasets for "data input" are different and messier than those in the manually extracted workflow.
- (ongoing) There are some duplicated datasets. 
- (ongoing) The steps with the same tool names
- (ongoing) what else to check? are tool_version, input_connections, workflow_outputs worth checking?
- (ongoing) parameters still have a lot issues (mentioned in the codes comments)

#  Installation instructions:
    ...coming up