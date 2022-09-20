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
    """
    Use the inputted history id to extract a workflow using bioblend API
    :param history_id:
    :param history_name:
    :return: userwf: the workflow of user history in the dictionary format

    >>> "a_galaxy_workflow" in get_user_workflow("96db5bbbc9a86365", "galaxy-101", "D4XEpojvk877VKOAtCpu8H2Irdr3kol")
    True
    """

    # config file to git.ignore, add specifications in the documentation
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
    """
    Parsing user input URL into parts of id number and name
    :param usr_url:
    :return: history_id, history_name:

    >>> get_history("https://usegalaxy.eu/u/berenice/h/galaxy-101")
    ('96db5bbbc9a86365', 'galaxy-101')
    """
    user_input = usr_url
    history_name = user_input.split("/")[6]
    page_source = requests.get(user_input).text
    page_source = page_source.split('id="history-')[1]
    history_id = page_source.partition('"')[0]
    return history_id, history_name


def get_standard_workflow(wf_url):
    """
    download workflow file via provided link

    turns the workflow into a dictionary, as the standard to be compared with the user workflow
    :return: standardwf: standard workflow in the form of dictionary

    >>> temp = get_standard_workflow\
    ("https://usegalaxy.eu/training-material/topics/introduction/tutorials/galaxy-intro-101/workflows/galaxy-intro-101-workflow.ga")
    >>> temp['name'] == "Find exons with the highest number of features"
    True
    """
    URL = wf_url
    response = requests.get(URL)
    open("stdwf.ga", "wb").write(response.content)
    with open(os.path.join(sys.path[0], "stdwf.ga"), "r") as f:
        standardtemp = f.read()
    standardwf = json.loads(standardtemp)
    return standardwf


def generate_report_file(target_path, data):
    """
    convert the report dictionary into a JSON file

    :param data: dictionary holding the information of the status of key features of user history
    :param target_path: the desired output destination of the report file, input via argparse

    >>> with open(os.path.join(sys.path[0], "report.json"), "r") as f: standardtemp = f.read()
    >>> "data_inputs" in standardtemp
    True
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

    This function only accept command line input in the format of URL(link to the user history)
    pass it to get_history function to get history id and name, which are then pass into get_uset_workflow function
    to generate the user workflow stored as a dictionary.
    get_standard_workflow gets standard workflow as dictionary from URLs.
    These two dictionaries are passed into compare function, which returns a report in dictionary format.
    The report dictionary then goes into generate_report_file function to be turned into a JSON file.
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


def _test():
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    main()
    _test()




