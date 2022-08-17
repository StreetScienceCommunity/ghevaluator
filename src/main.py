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
    """
    Use the inputted history id to extract a workflow using bioblend API
    :param history_id:
    :param history_name:
    :return: userwf: the workflow of user history in the dictionary format
    """
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
    """
    Parsing user input URL into parts of id number and name
    :param usr_url:
    :return: history_id, history_name:
    """
    user_input = usr_url
    history_name = user_input.split("/")[6]
    page_source = requests.get(user_input).text
    page_source = page_source.split('id="history-')[1]
    history_id = page_source.partition('"')[0]
    return history_id, history_name


def get_standard_workflow():
    """
    download workflow file via provided link(in the current case from a hardcoded droplist on the datanalyzer website)

    turns the workflow into a dictionary, as the standard to be compared with the user workflow
    :return: standardwf: standard workflow in the form of dictionary
    """
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
    """
    conver the report dictionary into a JSON file

    :param report: dictionary holding the information of the status of key features of user history
    """
    with open('report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=4)


def main():
    """
    The main function

    This function only accept command line input in the format of URL(link to the user history)
    pass it to get_history function to get history id and name, which are then pass into get_uset_workflow function
    to generate the user workflow stored as a dictionary.
    get_standard_workflow gets standard workflow as dictionary from hardcoded URLs,
    which will be a droplist on the website.
    These two dictionaries are passed into compare function, which returns a report in dictionary format.
    The report dictionary then goes into generate_report_file function to be turned into a JSON file.
    """
    parser = argparse.ArgumentParser(description='This program takes in URL of user history link, outputs the report of the performance.')
    parser.add_argument('url', help="Check a url for straight quotes", type=str)
    results = parser.parse_args()
    url = results.url
    his_id, his_name = get_history(url)
    usrwf = get_user_workflow(his_id, his_name)
    stdwf = get_standard_workflow()
    report = compare(usrwf, stdwf)
    generate_report_file(report)


if __name__ == "__main__":
    main()




