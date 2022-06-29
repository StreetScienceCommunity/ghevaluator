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


if __name__ == "__main__":
    main()




