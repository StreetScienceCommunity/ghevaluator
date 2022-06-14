#!/usr/bin/env python3
import os
import sys

import requests
from bioblend.galaxy import GalaxyInstance
from history_compare import compare
import json

gi = GalaxyInstance(url='https://usegalaxy.eu/', key='D4XEpojvk877VKOAtCpu8H2Irdr3kol')

user_input = input("Pls enter a galaxy history link:")
history_name = user_input.split("/")[6]
print("The name of the history you chose is: " + history_name)

page_source = requests.get(user_input).text
page_source = page_source.split('id="history-')[1]
history_id = page_source.partition('"')[0]
print("The id number of the history is: " + history_id)
datasets = gi.histories.show_history(history_id, True, False, True, None, 'dataset')

job = []

print("The datasets in this history are: ")
for dataset in datasets:
    # print(dataset['name'])
    info = gi.histories.show_dataset_provenance(history_id, dataset['id'], follow=False)
    job.append(info['job_id'])
    # print(info)

wf = gi.workflows.extract_workflow_from_history(history_id, history_name + "visible=true", job, dataset_hids=None,
                                                dataset_collection_hids=None)
workflow_id = wf['id'] #c079401840ab7c3f
# workflow_id = "c079401840ab7c3f"
print("The workflow Id is: " + workflow_id)
# path = 'D:/Study/22sose/Project'
# gi.workflows.export_workflow_to_local_path(workflow_id, path, use_default_filename=True)

userwf = gi.workflows.export_workflow_dict(workflow_id, version=None)

URL = "https://usegalaxy.eu/training-material/topics/assembly/tutorials/general-introduction/workflows/assembly-general-introduction.ga"
response = requests.get(URL)
open("userwf.ga", "wb").write(response.content)

with open(os.path.join(sys.path[0], "userwf.ga"), "r") as f:
    standardtemp = f.read()

standardwf = json.loads(standardtemp)
compare(userwf, standardwf)

# need to create a dropdown list for selecting tutorials, and a database linking the tutorials with the related
# workflow id. how to access the standard workflow files of the tutorials?
