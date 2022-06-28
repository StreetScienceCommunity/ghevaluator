#!/usr/bin/env python3
import os
import sys

import requests
from bioblend.galaxy import GalaxyInstance
from history_compare import compare
import json


def get_user_workflow(history_id, history_name):
    gi = GalaxyInstance(url='https://usegalaxy.eu/', key='D4XEpojvk877VKOAtCpu8H2Irdr3kol')
    datasets = gi.histories.show_history(history_id, True, False, True, None, 'dataset')
    job = []
    for dataset in datasets:
        info = gi.histories.show_dataset_provenance(history_id, dataset['id'], follow=False)
        job.append(info['job_id'])
    wf = gi.workflows.extract_workflow_from_history(history_id, history_name + "visible=true", job,
                                                    dataset_hids=None, dataset_collection_hids=None)
    workflow_id = wf['id']
    print("The workflow Id is: " + workflow_id)
    userwf = gi.workflows.export_workflow_dict(workflow_id, version=None)
    return userwf


def get_history():
    user_input = input("Pls enter a galaxy history link:")
    history_name = user_input.split("/")[6]
    print("The name of the history you chose is: " + history_name)
    page_source = requests.get(user_input).text
    page_source = page_source.split('id="history-')[1]
    history_id = page_source.partition('"')[0]
    print("The id number of the history is: " + history_id)
    return history_id, history_name


# workflow_id = "c079401840ab7c3f"

# path = 'D:/Study/22sose/Project'
# gi.workflows.export_workflow_to_local_path(workflow_id, path, use_default_filename=True)

def get_standard_workflow():
    URL = "https://usegalaxy.eu/training-material/topics/assembly/tutorials/general-introduction/workflows/assembly-general-introduction.ga"
    response = requests.get(URL)
    open("stdwf.ga", "wb").write(response.content)
    with open(os.path.join(sys.path[0], "stdwf.ga"), "r") as f:
        standardtemp = f.read()
    standardwf = json.loads(standardtemp)
    return standardwf


def main():
    his = get_history()
    his_id = his[0]
    his_name = his[1]
    usrwf = get_user_workflow(his_id, his_name)
    stdwf = get_standard_workflow()
    compare(usrwf, stdwf)


#  https://usegalaxy.eu/u/siyu_chen/h/assemblyhands-onsiyu-chen

if __name__ == "__main__":
    main()

# history_link = 'https://usegalaxy.eu/u/sbray/h/mpro-x1093'
#
# gi.histories.get_histories(slug='mpro-x1093') # get history id from the history_link
#
# datasets = gi.datasets.get_datasets(history_id=history_id, state='ok') # filter datasets on id from above, and state=ok
#
# dataset_hids = [ds['hid'] for ds in datasets if ds['history_content_type'] == 'dataset'] # dataset hids for extracting WF
# dataset_collection_hids = [ds['hid'] for ds in datasets if ds['history_content_type'] == 'dataset_collection'] # dataset collection hids for extracting WF
#
# # extract workflow from history, get id of workflow
# gi.workflows.extract_workflow_from_history(history_id, dataset_collection_hids=dataset_collection_hids, dataset_hids=dataset_hids)
#
# gi.workflows.export_workflow_dict(workflow_id)


# need to create a dropdown list for selecting tutorials, and a database linking the tutorials with the related
# workflow id. how to access the standard workflow files of the tutorials? output in json/yaml file
# send dulplicate result to berenice
# two types of input for the standard workflow
