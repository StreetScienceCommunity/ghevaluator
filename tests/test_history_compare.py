#!/usr/bin/env python3
import json


def compare(user_workflow, standard_workflow):
    """
    This function takes in the two workflows generated in the main.py and passes them into the function
    where the actual comparison happens.

    :param user_workflow:
    :param standard_workflow:
    :return: report: dictionary

    >>> std = {'a_galaxy_workflow': 'true', 'name': 'galaxy-101visible=true', 'steps': {'0': {'content_id': \
    '__DATA_FETCH__', 'id': 0, 'input_connections': {},'inputs': [], 'name': 'Data Fetch', 'tool_id': '__DATA_FETCH__'}\
    , '1': { 'content_id': '__DATA_FETCH__', 'id': 1, 'input_connections': {}, 'inputs': [], 'name': 'Data Fetch', \
    'tool_id': '__DATA_FETCH__'}, '2': { 'content_id': \
    'toolshed.g2.bx.psu.edu/repos/iuc/bedtools/bedtools_intersectbed/2.30.0', 'id': 2, 'input_connections': {'inputA':\
    {'id': 1, 'output_name': 'output0'}, 'reduce_or_iterate|inputB': {'id': 1, 'output_name': 'output1'}}, 'inputs': []\
    , 'label': None, 'name': 'bedtools Intersect intervals', 'outputs': [{'name': 'output', 'type': 'input'}], \
    'tool_id': 'toolshed.g2.bx.psu.edu/repos/iuc/bedtools/bedtools_intersectbed/2.30.0', 'tool_state': \
    '{"__input_ext": "input", "bed": "false", "header": "false", "split": "false", "strand": "", "__page__": null}',\
    'tool_version': '2.30.0'}, '3': { 'content_id': 'toolshed.g2.bx.psu.edu/repos/iuc/datamash_ops/datamash_ops/1.1.0',\
     'id': 3, 'input_connections': {'in_file': {'id': 2, 'output_name': 'output'}}, 'inputs': [], 'label': None, \
     'name': 'Datamash', 'outputs': [{'name': 'out_file', 'type': 'tabular'}], \
     'tool_id': 'toolshed.g2.bx.psu.edu/repos/iuc/datamash_ops/datamash_ops/1.1.0', 'tool_state': \
     '{"__input_ext": "bed", "grouping": "4", "ignore_case": "false", "__rerun_remap_job_id__": null}', \
     'tool_version':'1.1.0'}}}
    >>> usr = {'a_galaxy_workflow': 'true', 'name': 'Find exons with the highest number', 'steps': {'0': {'content_id': \
    'None', 'id': 0, 'input_connections': {},'inputs': [], 'name': 'Input dataset', 'tool_id': 'None'}\
    , '1': { 'content_id': 'None', 'id': 1, 'input_connections': {}, 'inputs': [], 'name': 'Input dataset', \
    'tool_id': 'None'}, '2': { 'content_id': \
    'toolshed.g2.bx.psu.edu/repos/iuc/bedtools/bedtools_intersectbed/2.30.0', 'id': 2, 'input_connections': {'inputA':\
    {'id': 0, 'output_name': 'output'}, 'reduce_or_iterate|inputB': {'id': 1, 'output_name': 'output'}}, 'inputs': []\
    , 'label': None, 'name': 'bedtools Intersect intervals', 'outputs': [{'name': 'output', 'type': 'input'}], \
    'tool_id': 'toolshed.g2.bx.psu.edu/repos/iuc/bedtools/bedtools_intersectbed/2.30.0', 'tool_state': \
    '{"__input_ext": "bed", "bed": "false", "header": "false", "split": "false", "strand": "", "__page__": null}',\
    'tool_version': '2.30.0'}, '3': { 'content_id': 'toolshed.g2.bx.psu.edu/repos/iuc/datamash_ops/datamash_ops/1.1.0',\
     'id': 3, 'input_connections': {'in_file': {'id': 2, 'output_name': 'output'}}, 'inputs': [], 'label': None, \
     'name': 'Datamash', 'outputs': [{'name': 'out_file', 'type': 'tabular'}], \
     'tool_id': 'toolshed.g2.bx.psu.edu/repos/iuc/datamash_ops/datamash_ops/1.1.0', 'tool_state': \
     '{"__input_ext": "bed", "grouping": "4", "ignore_case": "false", "__rerun_remap_job_id__": null}', \
     'tool_version':'1.1.0'}}}
    >>> temp = compare(std,usr)
    >>> temp['number_of_steps'] == 2
    True
    """
    temp1 = standard_workflow['steps']
    temp2 = user_workflow['steps']
    result = get_all_values(temp1, temp2)
    return result


def input_initialize():
    """
    initialize a dictionary template for the comparison results of data inputs

    >>> input_initialize()
    {'expected_number_of_inputs': 0, 'user_number_of_inputs': 0, 'status': True}
    """
    inputdict = {
        "expected_number_of_inputs": 0,
        "user_number_of_inputs": 0,
        "status": True
    }
    return inputdict


def tool_state_initialize():
    """
    initialize a dictionary template for the comparison results of name of the tool used in each step

    >>> tool_state_initialize()
    {'expected_value': 0, 'user_value': 0, 'status': True}
    """
    emptydict = {
        "expected_value": 0,
        "user_value": 0,
        "status": True
    }
    return emptydict


def tool_id_initialize():
    """
    initialize a dictionary template for the comparison results of the id of the tool used

    >>> tool_id_initialize()
    {'expected_id': 0, 'user_id': 0, 'status': False}
    """
    iddict = {
        "expected_id": 0,
        "user_id": 0,
        "status": False
    }
    return iddict


def tool_dev_initialize():
    """
    initialize a dictionary template for the comparison results of developers of the tool used

    >>> tool_dev_initialize()
    {'expected_dev': 0, 'user_dev': 0, 'status': False}
    """
    dvdict = {
        "expected_dev": 0,
        "user_dev": 0,
        "status": False
    }
    return dvdict


def tool_version_initialize():
    """
    initialize a dictionary template for the comparison results of version of the tool used

    >>> tool_version_initialize()
    {'expected_version': 0, 'user_version': 0, 'status': False}
    """
    vdict = {
        "expected_version": 0,
        "user_version": 0,
        "status": False
    }
    return vdict


def inpt_connection_initialize():
    """
    initialize a dictionary template for the comparison results of source of the input date to the tool used

    >>> inpt_connection_initialize()
    {'expected_input_source': [], 'user_input_source': [], 'status': True}
    """
    cntdict = {
        "expected_input_source": [],
        "user_input_source": [],
        "status": True
    }
    return cntdict


def splilt_id(s):
    """
    This function split the long tool id extracted from workflow into three subsections

    :param s: "content_id" from workflow file
    :return: sdev, sid, sversion: developer name, tool id name, tool version

    >>> splilt_id("toolshed.g2.bx.psu.edu/repos/iuc/multiqc/multiqc/1.7")
    ('iuc', 'multiqc', '1.7')
    """
    slist = str(s).split("/")
    if len(slist) >= 4:
        sdev = slist[2]
        sid = slist[4]
        sversion = slist[5]
    else:
        sdev = 0
        sid = 0
        sversion = 0
    return sdev, sid, sversion


def count_input_steps(std_input, usr_input):
    """
    count the numbers of the input datasets in both the user workflow and standard workflow

    :param std_input: standard workflow
    :param usr_input: user workflow
    :return: std, usr: (int) resulting counts

    >>> std_case = {'0': {'id': 0, 'input_connections': {}, 'inputs': [{'description': '', 'name': 'Exons'}], 'label':\
    'Exons', 'name': 'Input dataset', 'outputs': [], 'tool_id': None, 'tool_state': '{"optional": false}',\
    'tool_version': None, 'type': 'data_input'}, '1': {'id': 1, 'input_connections': {}, 'inputs': [{'description': '',\
    'name': 'Features'}], 'label': 'Features', 'name': 'Input dataset', 'outputs': [], 'tool_id': None, 'tool_state':\
     '{"optional": false}', 'tool_version': None, 'type': 'data_input'}}
    >>> usr_case = {'0': {'id': 0, 'input_connections': {}, 'inputs': [{'description': '', 'name': 'Exons'}], 'label':\
     'Exons', 'name': 'Data Fetch', 'outputs': [], 'tool_id': None, 'tool_state': '{"optional": false}', 'tool_version'\
     : None, 'type': 'data_input'}, '1': {'id': 1, 'input_connections': {}, 'inputs': [{'description': '', 'name': \
     'Features'}], 'label': 'Features', 'name': 'Data Fetch', 'outputs': [], 'tool_id': None, 'tool_state': \
     '{"optional\": false}', 'tool_version': None, 'type': 'data_input'}}
    >>> count_input_steps(std_case, usr_case)
    (2, 2)
    """

    std = 0
    usr = 0
    for key, value in std_input.items():
        if value['name'] == "Input dataset" or value['name'] == "Data Fetch":
            std = std + 1
    for key1, value2 in usr_input.items():
        if value2['name'] == "Data Fetch" or value2['name'] == "Input dataset":
            usr = usr + 1
            value2['name'] = value2['name'] + "_used"

    return std, usr


def get_all_values(std_dict, usr_dict):
    """
    Compare standard workflow with user workflow on multiple features
    :param std_dict: standard workflow
    :param usr_dict: user workflow
    :return: report: the final report as a dictionary

    >>> std = {'0': {'content_id': \
    '__DATA_FETCH__', 'id': 0, 'input_connections': {},'inputs': [], 'name': 'Data Fetch', 'tool_id': '__DATA_FETCH__'}\
    , '1': { 'content_id': '__DATA_FETCH__', 'id': 1, 'input_connections': {}, 'inputs': [], 'name': 'Data Fetch', \
    'tool_id': '__DATA_FETCH__'}, '2': { 'content_id': \
    'toolshed.g2.bx.psu.edu/repos/iuc/bedtools/bedtools_intersectbed/2.30.0', 'id': 2, 'input_connections': {'inputA':\
    {'id': 1, 'output_name': 'output0'}, 'reduce_or_iterate|inputB': {'id': 1, 'output_name': 'output1'}}, 'inputs': []\
    , 'label': None, 'name': 'bedtools Intersect intervals', 'outputs': [{'name': 'output', 'type': 'input'}], \
    'tool_id': 'toolshed.g2.bx.psu.edu/repos/iuc/bedtools/bedtools_intersectbed/2.30.0', 'tool_state': \
    '{"__input_ext": "input", "bed": "false", "header": "false", "split": "false", "strand": "", "__page__": null}',\
    'tool_version': '2.30.0'}, '3': { 'content_id': 'toolshed.g2.bx.psu.edu/repos/iuc/datamash_ops/datamash_ops/1.1.0',\
     'id': 3, 'input_connections': {'in_file': {'id': 2, 'output_name': 'output'}}, 'inputs': [], 'label': None, \
     'name': 'Datamash', 'outputs': [{'name': 'out_file', 'type': 'tabular'}], \
     'tool_id': 'toolshed.g2.bx.psu.edu/repos/iuc/datamash_ops/datamash_ops/1.1.0', 'tool_state': \
     '{"__input_ext": "bed", "grouping": "4", "ignore_case": "false", "__rerun_remap_job_id__": null}', \
     'tool_version':'1.1.0'}}
    >>> usr = {'0': {'content_id': \
    'None', 'id': 0, 'input_connections': {},'inputs': [], 'name': 'Input dataset', 'tool_id': 'None'}\
    , '1': { 'content_id': 'None', 'id': 1, 'input_connections': {}, 'inputs': [], 'name': 'Input dataset', \
    'tool_id': 'None'}, '2': { 'content_id':\
    'toolshed.g2.bx.psu.edu/repos/iuc/bedtools/bedtools_intersectbed/2.30.0', 'id': 2, 'input_connections': {'inputA':\
    {'id': 0, 'output_name': 'output'}, 'reduce_or_iterate|inputB': {'id': 1, 'output_name': 'output'}}, 'inputs': []\
    , 'label': None, 'name': 'bedtools Intersect intervals', 'outputs': [{'name': 'output', 'type': 'input'}], \
    'tool_id': 'toolshed.g2.bx.psu.edu/repos/iuc/bedtools/bedtools_intersectbed/2.30.0', 'tool_state': \
    '{"__input_ext": "bed", "bed": "false", "header": "false", "split": "false", "strand": "", "__page__": null}',\
    'tool_version': '2.30.0'}, '3': { 'content_id': 'toolshed.g2.bx.psu.edu/repos/iuc/datamash_ops/datamash_ops/1.1.0',\
     'id': 3, 'input_connections': {'in_file': {'id': 2, 'output_name': 'output'}}, 'inputs': [], 'label': None, \
     'name': 'Datamash', 'outputs': [{'name': 'out_file', 'type': 'tabular'}], \
     'tool_id': 'toolshed.g2.bx.psu.edu/repos/iuc/datamash_ops/datamash_ops/1.1.0', 'tool_state': \
     '{"__input_ext": "bed", "grouping": "4", "ignore_case": "false", "__rerun_remap_job_id__": null}', \
     'tool_version':'1.1.0'}}
    >>> temp = get_all_values(std, usr)
    >>> temp['steps'][0]['tool_used']['expected_value'] == 'bedtools Intersect intervals'
    True
    """

    # first count the number of steps in both workflows
    std_input, usr_input = count_input_steps(std_dict, usr_dict)
    # initialize a few parameters to be emulated in the later steps
    tool_mistake = 0
    number_param = 0
    param_mistakes = 0
    step = 0
    # initialize an empty overall report dictionary based on the number of "true" steps (exclude data inputs steps)
    report = dict_initialize(len(std_dict) - std_input)

    # loop through the standard workflow steps
    for key, value in std_dict.items():
        exist = False  # 1. "exist" - to keep a track on if a tool was used:
        id = True   # 2. "id" - to keep a track on if the tool id matches
        dev = True  # 3. "dev" - to keep a track on if the tool developer name matches
        version = True  # 4. "dev" - to keep a track on if the tool versions match
        parameters = 0  # 5. "parameters" - to keep a track on the mistakes made in parameters

        current_tool = value['name']
        # start checking the current tool step, if it is not just a data input step
        if current_tool != "Input dataset" and current_tool != "Data Fetch":
            std_inpt_list = get_input_id(value['input_connections'])  # get and store the input connections' id numbers
            current_parameters = value['tool_state']
            dict_for_thisloop = dict()  # initialize a temp holder dictionary for this loop (for the params)
            dict_for_thisloop['param_values'] = dict()
            dict_for_thisloop['param_overall_status'] = True

            # initialize a series of sub dictionaries for different features of this current tool step
            # (to be renewed for every step(new loop))
            tool_state = tool_state_initialize()
            tool_id = tool_id_initialize()
            tool_dev = tool_dev_initialize()
            tool_version = tool_version_initialize()
            inpt_connect = inpt_connection_initialize()
            # set the standard values of the current tool in the dictionary
            tool_state['expected_value'] = current_tool
            tool_dev['expected_dev'], tool_id['expected_id'], \
            tool_version['expected_version'] = splilt_id(value['tool_id'])

            # have already stored most of the standard values, now we compare them with the user workflow in loops
            for key1, value2 in usr_dict.items():
                if value2['name'] == current_tool:  # first check if the tools are the same
                    tool_state['user_value'] = value2['name']
                    # if is the same tool, store the tool name,
                    # and start further comparisons
                    tool_dev['user_dev'], tool_id['user_id'], \
                    tool_version['user_version'] = splilt_id(value2['tool_id'])
                    usr_inpt_list = get_input_id(value2['input_connections'])
                    if tool_id['user_id'] != tool_id['expected_id']:
                        id = False
                    if tool_version['user_version'] != tool_version['expected_version']:
                        version = False
                    if tool_dev['user_dev'] != tool_dev['expected_dev']:
                        dev = False

                    value2['name'] = value2['name'] + "_used" # change a matched tool's name to prevent it to be matched
                    exist = True    # if the tools are not the same, exist will stay as false
                    # check the parameters in a separate function
                    parameters, tempd, number_param = check_parameters(current_parameters, value2['tool_state'],
                                                                       dict_for_thisloop)
                    dict_for_thisloop = tempd
                    break

            # now we are done with the compares, record the results into the dictionaries by checking the indicators
            if parameters != 0:
                dict_for_thisloop['param_overall_status'] = False
            param_mistakes = param_mistakes + parameters
            dict_for_thisloop['number_of_mismatches'] = parameters
            dict_for_thisloop['total_number_of_param'] = number_param
            report['steps'][step]['parameters'] = dict_for_thisloop

            # report the results of Tools
            if exist:
                if id:
                    tool_id['status'] = True
                if version:
                    tool_version['status'] = True
                if dev:
                    tool_dev['status'] = True
            else:
                tool_mistake = tool_mistake + 1
                tool_state['status'] = False

            # record the temporal dictionaries into the final report
            report['steps'][step]['tool_used'] = tool_state
            report['steps'][step]['tool_id'] = tool_id
            report['steps'][step]['tool_dev'] = tool_dev
            report['steps'][step]['tool_version'] = tool_version

            # record the input connection names based on the saved id lists into the report
            for x in std_inpt_list:
                if -1 < x < std_input:
                    inpt_connect['expected_input_source'].append("datasets")
                else:
                    try:
                        discard1,idtemp,discard2 = splilt_id(std_dict[str(x)]['tool_id'])
                        inpt_connect['expected_input_source'].append(idtemp)
                    except:
                        pass
            for y in usr_inpt_list:
                if -1 < y < std_input:
                    inpt_connect['user_input_source'].append("datasets")
                else:
                    try:
                        discard3, idtemp1, discard4 = splilt_id(usr_dict[str(y)]['tool_id'])
                        inpt_connect['user_input_source'].append(idtemp1)
                    except:
                        pass
            report['steps'][step]['inputs_connection'] = inpt_connect
            step = step + 1  # add values to the current loop number to continue to the next loop

    report['data_inputs']['expected_number_of_inputs'] = std_input
    report['data_inputs']['user_number_of_inputs'] = usr_input
    report['data_inputs']['status'] = bool(std_input == usr_input)
    report['number_of_steps'] = len(std_dict.keys()) - std_input
    report['number_of_wrong_steps'] = tool_mistake

    return report


def get_input_id(unkw_dict):
    """
    recursive function looking for the id number in all formats of input connections

    :param unkw_dict: unknown layers of length of input connections as a sub dictionary
    :return: ids: a list of integers representing the input id numbers

    >>> get_input_id({'input1': {'id': 1, 'output_name': 'output1'}, 'input2': {'id': 22, 'output_name': 'output2'}})
    [1, 22]
    """
    ids = []
    for key, item in unkw_dict.items():
        if item is dict:
            get_input_id(item)
        else:
            try:
                ids.append(item['id'])
            except:
                ids.append(-1)
    return ids


def dict_initialize(nofsteps):
    """
    initialize the main structure of the report dictionary, to be filled with many sub dictionaries.
    :param nofsteps: the number of steps in the standard workflow
    :return: newdict: skeleton of the report dictionary

    >>> "data_inputs" in dict_initialize(1)
    True
    """
    newdict = dict()
    innerdict = dict()
    newdict['data_inputs'] = input_initialize()
    for i in range(nofsteps):
        innerdict[i] = {
            "tool_used": dict(),
            "tool_id": dict(),
            "tool_dev": dict(),
            "tool_version": dict(),
            "parameters": dict(),
            "inputs_connection": dict()
        }
    newdict['steps'] = innerdict
    newdict['number_of_steps'] = 0
    newdict['number_of_wrong_steps'] = 0
    return newdict


def check_parameters(std_param_str, usr_param_str2, current_dict):
    """
    further compare the parameters between two matched tools used
    notes:
      some values are set to as default in the newer version's of the tool, right now this case sets status to null.
      input connections have different values naturally.

    :param current_dict: pre-initialized parameter dictionary holding information outside this function
    :param std_param_str: standard parameters
    :param usr_param_str2: user parameters
    :return: count: numbers of mismatches
    :return: current_dict: the parameter dictionary now filled with information of each parameter
    :return: total_param_tobechecked: the total number of parameters

    >>> count, current_dict, total_param_tobechecked  = check_parameters\
    ('{"complement": "", "count": "5", "infile": {"__class__": "RuntimeValue"}, "__page__": null}',\
     '{"__input_ext": "tabular", "complement": "", "count": "5", "infile": null, "__page__": null}', \
     {'param_values': {}, 'param_overall_status': True})
    >>> count == 1
    True
    >>> "param_values" in current_dict
    True
    >>> total_param_tobechecked == 4
    True
    """
    std_pr = json.loads(std_param_str)
    user_pr = json.loads(usr_param_str2)
    count = 0
    total_param_tobechecked = len(std_pr.keys())
    # not counting missing parameters as wrong at this moment.
    for k in std_pr.keys():
        current_dict['param_values'][k] = {
            "expected_input": std_pr[k],
            "user_input": None,
            "status": False
        }
        if k in user_pr:
            current_dict['param_values'][k]["user_input"] = user_pr[k]
            if std_pr[k] == user_pr[k]:
                current_dict['param_values'][k]["status"] = True
            else:
                current_dict['param_values'][k]["status"] = False
                count = count + 1
        else:
            current_dict['param_values'][k]["status"] = None
    return count, current_dict, total_param_tobechecked


