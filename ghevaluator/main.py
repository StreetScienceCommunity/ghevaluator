#!/usr/bin/env python3
import os
from pathlib import Path
import sys
import argparse
import requests
from bioblend.galaxy import GalaxyInstance
from history_compare import compare
import json

def get_user_workflow(history_id, history_name, apikey):
    """Use the inputted history id to extract a workflow using bioblend API

    :param history_id: The id of the user's history
    :param history_name: The name of the user's history
    :return: **userwf**: the workflow of user history in the dictionary format

    |
    """
    gi = GalaxyInstance(url='https://usegalaxy.eu/', key=apikey)
    datasets = gi.histories.show_history(history_id, True, False, True, None, 'dataset')
    job = []
    for dataset in datasets:
        info = gi.histories.show_dataset_provenance(history_id, dataset['id'], follow=False)
        job.append(info['job_id'])
    wf = gi.workflows.extract_workflow_from_history(history_id, history_name + "visible=true", job,
                                                    dataset_hids=None, dataset_collection_hids=None)
    workflow_id = wf['id']
    userwf = gi.workflows.export_workflow_dict(workflow_id, version=None)
    return userwf


def get_history(usr_url):
    """Parsing user input URL into parts of id number and name

    :param usr_url: link to the user's history which is intented to be evaluated.

    :return: **history_name**, **history_id**: the extracted name of the history, the extracted history id

    |
    """
    user_input = usr_url
    history_name = user_input.split("/")[6]
    page_source = requests.get(user_input).text
    page_source = page_source.split('id="history-')[1]
    history_id = page_source.partition('"')[0]
    return history_id, history_name


def get_standard_workflow(wf_url):
    """Download workflow file via provided link.
    turns the workflow into a dictionary, as the standard to be compared with the user workflow.

    :param wf_url: link to the standard workflow file

    :return: **standardwf**: standard workflow in the form of dictionary

    |
    """
    URL = wf_url
    response = requests.get(URL)
    open("stdwf.ga", "wb").write(response.content)
    with open(os.path.join(sys.path[0], "stdwf.ga"), "r") as f:
        standardtemp = f.read()
    standardwf = json.loads(standardtemp)
    return standardwf


def generate_report_file(target_path, data):
    """Convert the report dictionary into a JSON file

    :param data: dictionary holding the information of the status of key features of user history
    :param target_path: the desired output destination of the report file, input via argparse

    |
    """
    if not os.path.exists(target_path):
        try:
            os.makedirs(target_path)
        except Exception as e:
            print(e)
            raise
    with open(os.path.join(target_path, 'report.json'), 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    """
    The main function
    
    This function serves as the driver and connection between all major parts of the program:
    It does four things:

    1. Take in 4 parameters via ArgumentParser.
    2. Call different fundtions to process the parameters, and to generate two workflows.
    3. Pass the two workflows to the compare function in history_compare.py
    4. Call generate_report_file function to output the final report.
  
    :param history_url: the link to the user's history, which is intended to be tested.
    :param workflow_url: the link to the workflow, corresponding to the history, which serves as the standard.
    :param apikey: a Galaxy API key obtained prehand
    :param path: the desired system path to output the final report
    :return: **final report**: a JSON file

    |
    """
    parser = argparse.ArgumentParser(description='This program tests user history against standard tutorial steps, then generate a detailed report on the performance.')
    parser.add_argument('history_url', help="the URL to the user's history", type=str)
    parser.add_argument('workflow_url', help="the URL to the corresponding standard workflow", type=str)
    parser.add_argument('apikey', help="the Galaxy API key", type=str)
    parser.add_argument('path', nargs="?", default=".", help="Please input the output path of the final report", type=Path)
    results = parser.parse_args()
    url = results.history_url
    workflow = results.workflow_url
    apikey = results.apikey
    path = results.path
    his_id, his_name = get_history(url)
    usrwf = get_user_workflow(his_id, his_name, apikey)
    stdwf = get_standard_workflow(workflow)
    report = compare(usrwf, stdwf)
    generate_report_file(path, report)
 

if __name__ == "__main__":
    main()




