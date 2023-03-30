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
    # Get dataset and their job ids
    hist = gi.histories.show_history(
        history_id=hist_id,
        types='dataset')
    jobs = []
    for ds in hist['state_ids']['ok']:
        info = gi.histories.show_dataset_provenance(
            history_id=hist_id,
            dataset_id=ds,
            follow=False)
        jobs.append(info['job_id'])
    jobs = list(set(jobs))  # remove duplicated ids
    # Extract workflow from history
    wf = gi.workflows.extract_workflow_from_history(
        history_id=hist_id,
        job_ids=jobs,
        workflow_name=f'{hist_name} workflow')
    wf_id = wf['id']
    return gi.workflows.export_workflow_dict(wf_id)


def get_standard_workflow(wf_url):
    """
    Turn the workflow in a provided link into a dictionary, as the standard to be compared with the user workflow.

    :param wf_url: link to the standard workflow file
    :return: dictionary with the workflow
    """
    r = requests.get(wf_url)
    return r.json()


def is_input(step):
    """
    Check if a step is an input step

    :param step: dictionary with a workflow step
    :return: boolean
    """
    return step['name'] == "Input dataset" or step['name'] == "Data Fetch" or step['type'] == 'data_input'


def count_wf_inputs(wf):
    """
    Count the numbers of the inputs in a workflow

    :param wf: a workflow
    :return: number of inputs in the workflow
    """
    nb = 0
    for key, step in wf.items():
        if is_input(step):
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
            return get_input_id(item)
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
        owner = None
        id = None
        version = None
    return owner, id, version


def reformate_workflows(wf):
    """
    Reformate history workflow into a list and a dictionary with key being the tool names

    :param wf: Bioblend workflow
    :return: list and dictionary
    """
    ordered_wf = []
    wf_by_tools = {}
    for key, step in wf.items():
        if is_input(step):
            continue
        tool = step['name']
        owner, id, version = split_id(step['tool_id'])
        # format parameters
        parameters = json.loads(step['tool_state'])
        for p in ['__page__', '__input_ext', 'chromInfo', '__rerun_remap_job_id__']:
            if p in parameters:
                del parameters[p]
        for p in parameters:
            if parameters[p] is not None:
                if parameters[p] == "null":
                    parameters[p] = None
                elif isinstance(parameters[p], str) and '"' in parameters[p]:
                    parameters[p] = parameters[p].replace('"', '')
        # format step
        step_dict = {
            "tool": tool,
            "id": id,
            "owner": owner,
            "version": version,
            "parameters": parameters,
            "inputs_connection": get_input_id(step['input_connections']),
            "order": key
        }
        # drop step
        ordered_wf.append(step_dict)
        wf_by_tools.setdefault(tool, [])
        wf_by_tools[tool].append(step_dict)
    return ordered_wf, wf_by_tools


def fill_step_comparison(ref_step, hist_step, key):
    """
    Compare reference and history steps for a specific key

    :param ref_step: dictionary with reference step
    :param hist_step: dictionary with history step
    :param key: key of values to compare
    :return: dictionary with expected, history, same
    """
    hist_value = hist_step[key] if hist_step is not None else None
    return {
        'expected': ref_step[key],
        'history': hist_value,
        'same': bool(ref_step[key] == hist_value)
    }


def fill_step_report(ref_step, hist_step=None):
    """
    Prepare the report for a step

    :param ref_step: dictionary with reference step
    :param hist_step: dictionary with history step
    :return: dictionary
    """
    s_report = {
        "tool": fill_step_comparison(ref_step, hist_step, 'tool'),
        "id": fill_step_comparison(ref_step, hist_step, 'id'),
        "owner": fill_step_comparison(ref_step, hist_step, 'owner'),
        "version": fill_step_comparison(ref_step, hist_step, 'version'),
        "order": fill_step_comparison(ref_step, hist_step, 'order'),
        "parameters": {
            'number': {
                'expected': len(ref_step['parameters']),
                'history': len(hist_step['parameters']) if hist_step is not None else None,
                'same': bool(len(ref_step['parameters']) == len(hist_step['parameters'])) if hist_step is not None else False
            },
            'wrong': len(ref_step['parameters']),
            'details': {}
        },
        "inputs_connection": fill_step_comparison(ref_step, hist_step, 'inputs_connection')
    }
    # compare parameters
    for p in ref_step['parameters']:
        s_report['parameters']['details'][p] = {
            'expected': ref_step['parameters'][p],
            'history': hist_step['parameters'][p] if hist_step is not None and p in hist_step['parameters'] else None,
            'same': bool(ref_step['parameters'][p] == hist_step['parameters'][p]) if hist_step is not None and p in hist_step['parameters'] else False
        }
        if s_report['parameters']['details'][p]['same']:
            s_report['parameters']['wrong'] -= 1
    return s_report


def compare_ordered_steps(ref_steps, hist_steps):
    """
    Compare ordered steps

    :param ref_steps: list of steps in reference workflow
    :param hist_steps: list of steps in history workflow
    :return: dictionary with comparison
    """
    comparison = {}
    h_step_count = 0
    for i, ref_step in enumerate(ref_steps):
        if hist_steps is None:
            comparison[i] = fill_step_report(ref_step, None)
        elif ref_step['tool'] == hist_steps[h_step_count]['tool']:
            comparison[i] = fill_step_report(ref_step, hist_steps[h_step_count])
            h_step_count += 1
        else:
            print("Need to implement input connection comparison so order is similar")
            comparison[i] = fill_step_report(ref_step, None)
    return comparison


def compare_workflows(hist_wf, ref_wf):
    """
    Compare a user workflow to a reference workflow and generate a report

    :param hist_wf: dictorionary with history extracted workflow
    :param ref_wf: dictionary with reference workflow
    :return: dictionary with report
    """
    report = {}
    hist_wf = hist_wf['steps']
    ref_wf = ref_wf['steps']
    # Reformate workflows
    ordered_hist_wf, hist_wf_by_tool = reformate_workflows(hist_wf)
    ordered_ref_wf, ref_wf_by_tool = reformate_workflows(ref_wf)
    report['reference_wf'] = ordered_ref_wf
    report['history_wf'] = ordered_hist_wf
    # Compare inputs in both workflows
    hist_wf_input_nb = count_wf_inputs(hist_wf)
    ref_wf_input_nb = count_wf_inputs(ref_wf)
    report['data_inputs'] = {
        "expected": ref_wf_input_nb,
        "history": hist_wf_input_nb,
        "same": bool(ref_wf_input_nb == hist_wf_input_nb)
    }
    # Compare number of steps in both workflows
    hist_step_nb = len(hist_wf) - hist_wf_input_nb
    ref_step_nb = len(ref_wf) - ref_wf_input_nb
    report['steps'] = {
        'expected': ref_step_nb,
        'history': hist_step_nb,
        'same': bool(ref_step_nb == hist_step_nb)
    }
    # Compare ordered workflows
    report['comparison_given_reference_workflow_order'] = compare_ordered_steps(ordered_ref_wf, ordered_hist_wf)
    # Compare workflows by tools
    comparison = {}
    for tool in ref_wf_by_tool:
        comparison[tool] = {
            'number': {
                'expected': len(ref_wf_by_tool[tool]),
                'history': len(hist_wf_by_tool[tool]) if tool in hist_wf_by_tool else 0,
                'same': bool(len(ref_wf_by_tool[tool]) == len(hist_wf_by_tool[tool])) if tool in hist_wf_by_tool else False
            },
            'details': compare_ordered_steps(ref_wf_by_tool[tool], hist_wf_by_tool[tool] if tool in hist_wf_by_tool else None)
        }
    report['comparison_by_reference_workflow_tools'] = comparison
    return report


def generate_report_files(data, output_dp):
    """
    Convert the report dictionary into a JSON file

    :param data: dictionary holding the information of the status of key features of user history
    :param output_dp: Path object of the output directory
    """
    json_fp = output_dp / Path("report.json")
    with json_fp.open('w') as out_f:
        json.dump(data, out_f, ensure_ascii=False, indent=4)


def ghevaluator(hist_url, wf_url, apikey, output_dp):
    """
    The main function

    This function serves as the driver and connection between all major parts of the program:

    1. Call different fundtions to process the parameters, and to generate two workflows.
    2. Pass the two workflows to the compare function in history_compare.py
    3. Call generate_report_file function to output the final report.

    :param hist_url: URL to Galaxy history
    :param wf_url: URL to template workflow
    :param apikey: a Galaxy API key obtained prehand
    :param output_dp: Path object of the output report
    """
    hist_wf = get_workflow_from_history(hist_url, apikey)
    ref_wf = get_standard_workflow(wf_url)
    report = compare_workflows(hist_wf, ref_wf)
    generate_report_files(report, output_dp)
