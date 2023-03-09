#!/usr/bin/env python3

import json
import requests

from bioblend.galaxy import GalaxyInstance
from pathlib import Path
from urllib import parse


def get_hist_info(hist_url):
    """
    Get history name and Galaxy URL from history URL

    :param hist_url: URL to Galaxy history
    :return: Galaxy URL, history name and id
    """
    url = parse.urlparse(hist_url)
    galaxy_url = url._replace(path="").geturl()
    hist_name = url.path.split("/")[4]
    # load history page to find history id
    page_source = requests.get(hist_url).text
    page_source = page_source.split('"params": {"id": "')[1]
    hist_id = page_source.partition('"')[0]
    return galaxy_url, hist_name, hist_id


def get_workflow_from_history(hist_url, apikey):
    """
    Extract the workflow from a Galaxy history using bioblend

    :param hist_url: URL to Galaxy history
    :param apikey: API key to Galaxy server with history
    :return: dictionary with the workflow corresponding to Galaxy history
    """
    # Get Galaxy URL, history name and id
    galaxy_url, hist_name, hist_id = get_hist_info(hist_url)
    # Connect to Galaxy instance
    gi = GalaxyInstance(url=galaxy_url, key=apikey)
    # Get dataset and thier job ids
    datasets = gi.histories.show_history(
        history_id=hist_id,
        types='dataset')
    print(datasets)
    jobs = []
    for ds in datasets:
        info = gi.histories.show_dataset_provenance(
            history_id=hist_id,
            dataset_id=ds['id'],
            follow=False)
        jobs.append(info['job_id'])
    # Extract workflow from history
    wf = gi.workflows.extract_workflow_from_history(
        history_id=hist_id,
        history_name= f"{ hist_name }visible=true",
        job_ids=jobs,
        dataset_hids=None,
        dataset_collection_hids=None)
    wf_id = wf['id']
    return gi.workflows.export_workflow_dict(wf_id, version=None)


def get_standard_workflow(wf_url):
    """
    Turn the workflow in a provided link into a dictionary, as the standard to be compared with the user workflow.

    :param wf_url: link to the standard workflow file
    :return: dictionary with the workflow
    """
    r = requests.get(wf_url)
    return r.json()


def count_wf_inputs(wf):
    """
    Count the numbers of the inputs in a workflow

    :param wf: a workflow
    :return: number of inputs in the workflow
    """
    nb = 0
    for key, value in wf.items():
        if value['name'] == "Input dataset" or value['name'] == "Data Fetch":
            nb += 1
    return nb


def get_input_id(unkw_dict):
    """
    Recursive function looking for the id number inside the part of the dictionary of the input connections.

    :param unkw_dict: unknown layers of length of input connections as a sub dictionary
    :return: a list of integers representing the input id numbers
    """
    ids = []
    for key, item in unkw_dict.items():
        if item is dict:
            get_input_id(item)
        elif 'id' in item:
            ids.append(item['id'])
        else:
            ids.append(-1)
    return ids


def split_id(tool_id):
    """
    Split the long tool id extracted from workflow into ToolShed owner, short tool id name, tool version

    :param tool_id: "content_id" from workflow file

    :return: owner, tool id, tool version
    """
    split_tool_id = str(tool_id).split("/")
    if len(split_tool_id) >= 4:
        owner = split_tool_id[2]
        id = split_tool_id[4]
        version = split_tool_id[5]
    else:
        owner = 0
        id = 0
        version = 0
    return owner, id, version


def get_parameters(param_str):
    """

    :param :
    :return:
    """
    params = json.loads(param_str)


def compare_workflows(hist_wf, ref_wf):
    """
    Compare a user workflow to a reference workflow and generate a report

    :param hist_wf: dictorionary with history extracted workflow
    :param ref_wf: dictionary with reference workflow
    :return: dictionary with report
    """
    hist_wf = hist_wf['steps']
    ref_wf = ref_wf['steps']
    # Compare number of steps in both workflows
    hist_wf_input_nb = count_wf_inputs(hist_wf)
    ref_wf_input_nb = count_wf_inputs(ref_wf)
    # Reformate history workflow inot dictionary with key being the tool names
    reform_hist_wf = {}
    for key, step in hist_wf.items():
        tool = step['name']
        reform_hist_wf.setdefault(tool, [])
        owner, id, version = split_id(step['tool_id'])
        reform_hist_wf[tool].append({
            "id": id,
            "owner": owner,
            "version": version,
            "parameters": json.loads(step['tool_state']),
            "inputs_connection": get_input_id(ref_step['input_connections'])
        })
    # Initialize some parameters
    tool_mistake = 0
    param_nb = 0
    param_mistakes = 0
    step_nb = len(ref_wf) - ref_wf_input_nb
    report = {
        'data_inputs': {
            "expected": ref_wf_input_nb,
            "history": hist_wf_input_nb,
            "status": bool(ref_wf_input_nb == hist_wf_input_nb)
        },
        'steps':{
            'number': {
                'expected': step_nb,
                'history': len(hist_wf) - hist_wf_input_nb,
                'same': False
            },
            'wrong': step_nb,
            'details': {}
        }
    }
    # Loop through the reference workflow steps
    step = 0
    for key, ref_step in ref_wf.items():
        tool = ref_step['name']
        # pass if it is a data input step
        if tool == "Input dataset" or tool == "Data Fetch":
            continue
        # initialize objects, in particular the step report
        owner, id, version = split_id(ref_step['tool_id'])
        ref_params = json.loads(ref_step['tool_state'])
        s_report = {
            "tool": {
                'expected': tool,
                'history': None,
                'same': False
            },
            "id": {
                'expected': id,
                'history': None,
                'same': False
            },
            "owner": {
                'expected': owner,
                'history': None,
                'same': False
            },
            "version": {
                'expected': version,
                'history': None,
                'same': False
            },
            "parameters": {
                'number': {
                    'expected': len(ref_params),
                    'history': None,
                    'same': False
                },
                'wrong': len(ref_params),
                'details': {}
            },
            "inputs_connection": {
                "expected": get_input_id(ref_step['input_connections']),
                "history": [],
                "same": False
            }
        }
        for p in ref_params:
            s_report['parameters']['details'][p] = {
                'expected': ref_params[p],
                'history': None,
                'same': False
            }
        # search for tool in history workflow
        if tool in reform_hist_wf:
            ## NEED TO DEAL with lists in reform_user_wf
            report['steps']['wrong'] -= 1
            # add given value and make comparison
            for n in ['tool', 'id', 'owner', 'version']:
                s_report[n]['history'] = reform_hist_wf[tool][n]
                s_report[n]['same'] = bool(report['steps'][step][n]['history'] == report['steps'][step][n]['expected'])
            # compare parameter numbers
            s_report['parameters']['number']['history'] = len(reform_hist_wf[tool]['parameters'])
            s_report['parameters']['number']['same'] = bool(s_report['parameters']['number']['history'] == s_report['parameters']['number']['expected'])
            # compare parameters one by one
            for p in s_report['parameters']['details']:
                if p in reform_hist_wf[tool]['parameters']:
                    s_report['parameters']['details'][p]['history'] = reform_hist_wf[tool]['parameters'][p]
                    s_report['parameters']['details'][p]['same'] = bool(s_report['parameters']['details'][p]['history'] == s_report['parameters']['details'][p]['expected'])
                    s_report['parameters']['wrong'] -= 1
            # compare inputs
            report['steps'][step]['inputs_connection']['history'] = reform_hist_wf[tool]['inputs_connection']

        # record the input connection names based on the saved id lists into the report
        #for x in std_inpt_list:
        #    if -1 < x < std_input:
        #        inpt_connect['expected_input_source'].append("datasets")
        #    else:
        #        try:
        #            discard1,idtemp,discard2 = splilt_id(std_dict[str(x)]['tool_id'])
        #            inpt_connect['expected_input_source'].append(idtemp)
        #        except:
        #            pass
        #for y in usr_inpt_list:
        #    if -1 < y < std_input:
        #        inpt_connect['user_input_source'].append("datasets")
        #    else:
        #        try:
        #            discard3, idtemp1, discard4 = splilt_id(usr_dict[str(y)]['tool_id'])
        #            inpt_connect['user_input_source'].append(idtemp1)
        #        except:
        #            pass
        report['steps']['details'][step] = s_report
    return report


def generate_report_file(data, output_fp):
    """
    Convert the report dictionary into a JSON file

    :param data: dictionary holding the information of the status of key features of user history
    :param output_fp: Path object of the output report
    """
    with output_fp.open('w') as out_f:
        json.dump(data, out_f, ensure_ascii=False, indent=4)


def ghevaluator(hist_url, wf_url, apikey, output_fp):
    """
    The main function

    This function serves as the driver and connection between all major parts of the program:

    1. Call different fundtions to process the parameters, and to generate two workflows.
    2. Pass the two workflows to the compare function in history_compare.py
    3. Call generate_report_file function to output the final report.

    :param hist_url: URL to Galaxy history
    :param wf_url: URL to template workflow
    :param apikey: a Galaxy API key obtained prehand
    :param output_fp: Path object of the output report
    """
    hist_wf = get_workflow_from_history(hist_url, apikey)
    ref_wf = get_standard_workflow(wf_url)
    report = compare_workflows(hist_wf, ref_wf)
    generate_report_file(report, output_fp)
