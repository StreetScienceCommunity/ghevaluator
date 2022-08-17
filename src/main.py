#!/usr/bin/env python3
import os
import sys
import argparse
import requests
from bioblend.galaxy import GalaxyInstance
from history_compare import compare
import json

# https://usegalaxy.eu/u/siyu_chen/h/assemblyhands-onsiyu-chen
# https://usegalaxy.eu/u/berenice/h/galaxy-101
# https://usegalaxy.eu/u/filipposz/h/classification-in-machine-learning
def get_user_workflow(history_id, history_name):
    # config file
    gi = GalaxyInstance(url='https://usegalaxy.eu/', key='D4XEpojvk877VKOAtCpu8H2Irdr3kol')
    datasets = gi.histories.show_history(history_id, True, False, True, None, 'dataset')
    job = []
    for dataset in datasets:
        info = gi.histories.show_dataset_provenance(history_id, dataset['id'], follow=False)
        job.append(info['job_id'])
    # wf = gi.workflows.extract_workflow_from_history(history_id, history_name + "visible=true", job,
    #                                                 dataset_hids=None, dataset_collection_hids=None)
    # workflow_id = wf['id']
    workflow_id = '8fce485f316eb0ea'
    print("The workflow Id is: " + workflow_id)
    userwf = gi.workflows.export_workflow_dict(workflow_id, version=None)
    return userwf


def get_history(usr_url):
    # user_input = input("Pls enter a galaxy history link:")
    user_input = usr_url
    history_name = user_input.split("/")[6]
    print("The name of the history you chose is: " + history_name)
    page_source = requests.get(user_input).text
    page_source = page_source.split('id="history-')[1]
    history_id = page_source.partition('"')[0]
    print("The id number of the history is: " + history_id)
    return history_id, history_name


def get_standard_workflow():
    URL = "https://usegalaxy.eu/training-material/topics/assembly/tutorials/general-introduction/workflows/assembly-general-introduction.ga"
    # URL = "https://usegalaxy.eu/training-material/topics/introduction/tutorials/galaxy-intro-101/workflows/galaxy-intro-101-workflow.ga"
    # URL = "https://usegalaxy.eu/training-material/topics/statistics/tutorials/classification_machinelearning/workflows/ml_classification.ga"
    response = requests.get(URL)
    open("stdwf.ga", "wb").write(response.content)
    with open(os.path.join(sys.path[0], "stdwf.ga"), "r") as f:
        standardtemp = f.read()
    standardwf = json.loads(standardtemp)
    return standardwf


def generate_report_file(report):
    with open('report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=4)


def main():
    parser = argparse.ArgumentParser(description='This program takes in URL of user history link, outputs the report of the performance.')
    parser.add_argument('url', help="Check a url for straight quotes", type=str)
    results = parser.parse_args()
    url = results.url
    his = get_history(url)
    his_id = his[0]
    his_name = his[1]
    usrwf = get_user_workflow(his_id, his_name)
    stdwf = get_standard_workflow()
    report = compare(usrwf, stdwf)
    generate_report_file(report)


if __name__ == "__main__":
    main()




