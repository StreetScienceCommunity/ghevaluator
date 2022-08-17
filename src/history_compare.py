#!/usr/bin/env python3
import json


def compare(user_workflow, standard_workflow):
    """
    This function takes in the two workflows generated in the main.py and passes them into the function
    where the actual comparison happens.

    :param user_workflow:
    :param standard_workflow:
    :return: report: dictionary
    """

    temp1 = standard_workflow['steps']
    temp2 = user_workflow['steps']
    result = get_all_values(temp1, temp2)

    return result


def input_initialize():
    """
    initialize a dictionary template for the comparison results of data inputs
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


def count_input_steps(dict1, dict2):
    """
    count the numbers of the input datasets in both the user workflow and standard workflow
    :param dict1: standard workflow
    :param dict2: user workflow
    :return: std, usr: (int) resulting counts
    """
    std = 0
    usr = 0
    for key, value in dict1.items():
        if value['name'] == "Input dataset":
            std = std + 1
    for key1, value2 in dict2.items():
        if value2['name'] == "Data Fetch":
            usr = usr + 1
            value2['name'] = value2['name'] + "_used"
    return std, usr


def get_all_values(dict1, dict2):
    """
    Compare standard workflow with user workflow for multiple features
    :param dict1: standard workflow
    :param dict2: user workflow
    :return: report: the final report as a dictionary
    """
    std_input, usr_input = count_input_steps(dict1, dict2)
    tool_mistake = 0
    report = dict_initialize(len(dict1) - std_input)
    number_param = 0
    param_mistakes = 0
    step = 0

    for key, value in dict1.items():
        exist = False  # 1. "exist" - to check if a tool was used:
        id = True
        dev = True
        version = True
        parameters = 0  # 2. "parameters" - to check if parameters were selected correctly:

        current_tool = value['name']
        if current_tool != "Input dataset":
            std_inpt_list = get_input_id(value['input_connections'])
            current_parameters = value['tool_state']
            dict_for_thisloop = dict()
            dict_for_thisloop['param_values'] = dict()
            dict_for_thisloop['param_overall_status'] = True

            tool_state = tool_state_initialize()
            tool_id = tool_id_initialize()
            tool_dev = tool_dev_initialize()
            tool_version = tool_version_initialize()
            inpt_connect = inpt_connection_initialize()

            tool_state['expected_value'] = current_tool
            tool_dev['expected_dev'], tool_id['expected_id'], tool_version['expected_version'] = splilt_id(value['tool_id'])

            for key1, value2 in dict2.items():
                if value2['name'] == current_tool:
                    tool_state['user_value'] = value2['name']
                    tool_dev['user_dev'], tool_id['user_id'], tool_version['user_version'] = splilt_id(value2['tool_id'])
                    usr_inpt_list = get_input_id(value2['input_connections'])
                    if tool_id['user_id'] != tool_id['expected_id']:
                        id = False
                    if tool_version['user_version'] != tool_version['expected_version']:
                        version = False
                    if tool_dev['user_dev'] != tool_dev['expected_dev']:
                        dev = False

                    value2['name'] = value2['name'] + "_used"
                    exist = True
                    parameters, tempd, number_param = check_parameters(current_parameters, value2['tool_state'],
                                                                       dict_for_thisloop)
                    dict_for_thisloop = tempd
                    break

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

            report['steps'][step]['tool_used'] = tool_state
            report['steps'][step]['tool_id'] = tool_id
            report['steps'][step]['tool_dev'] = tool_dev
            report['steps'][step]['tool_version'] = tool_version

            for x in std_inpt_list:
                if -1 < x < std_input:
                    inpt_connect['expected_input_source'].append("datasets")
                else:
                    try:
                        discard1,idtemp,discard2 = splilt_id(dict1[str(x)]['tool_id'])
                        inpt_connect['expected_input_source'].append(idtemp)
                    except:
                        pass
            for y in usr_inpt_list:
                if -1 < y < std_input:
                    inpt_connect['user_input_source'].append("datasets")
                else:
                    try:
                        discard3, idtemp1, discard4 = splilt_id(dict2[str(y)]['tool_id'])
                        inpt_connect['user_input_source'].append(idtemp1)
                    except:
                        pass
            report['steps'][step]['inputs_connection'] = inpt_connect
            step = step + 1

    report['data_inputs']['expected_number_of_inputs'] = std_input
    report['data_inputs']['user_number_of_inputs'] = usr_input
    report['data_inputs']['status'] = bool(std_input == usr_input)
    report['number_of_steps'] = len(dict1.keys()) - std_input
    report['number_of_wrong_steps'] = tool_mistake

    return report


def get_input_id(unkw_dict):
    """
    recursive function looking for the id number in all formats of input connections

    :param unkw_dict: unknown layers of length of input connections as a sub dictionary
    :return: ids: a list of integers representing the input id numbers
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


def check_parameters(str1, str2, current_dict):
    """
    further compare the parameters between two matched tools used
    Some small bugs to be fixed:
    e.g. some differences in the format will result in a count as mistake, but they are actually the same.
      some values are set to as default in the newer version's of the tool, right now this case sets status to null.
      input connections have different values naturally.

    :param current_dict: pre-initialized parameter dictionary holding information outside this function
    :param str1: standard parameters
    :param str2: user parameters
    :return: count: numbers of mismatches
    :return: current_dict: the parameter dictionary now filled with information of each parameter
    :return: total_param_tobechecked: the total number of parameters
    """
    std_pr = json.loads(str1)
    user_pr = json.loads(str2)
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

