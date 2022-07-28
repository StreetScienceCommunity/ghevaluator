#!/usr/bin/env python3
import json


def compare(user_workflow, standard_workflow):
    """
    This function takes in the two workflows generated in the main.py,
    and passes them into the function where the actual comparison happens.
    Potentially, it will be linked to the yaml/json output for generating the report
    next key what we would like to compare tool ID, version, parameter, inputs
    Store the compare information (status, expected value, user value)
    :param user_workflow:
    :param standard_workflow:
    :return: report (as a dictionary)
    """

    temp1 = standard_workflow['steps']
    temp2 = user_workflow['steps']
    result = get_all_values(temp1, temp2)

    return result


def tool_state_initialize():
    emptydict = {
        "expected_value": 0,
        "user_value": 0,
        "status": True
    }
    return emptydict


def tool_id_initialize():
    iddict = {
        "expected_id": 0,
        "user_id": 0,
        "status": False
    }
    return iddict


def tool_dev_initialize():
    dvdict = {
        "expected_dev": 0,
        "user_dev": 0,
        "status": False
    }
    return dvdict


def tool_version_initialize():
    vdict = {
        "expected_version": 0,
        "user_version": 0,
        "status": False
    }
    return vdict


def param_initialize():
    paramdict = {
        "expected_value": 0,
        "user_value": 0,
        "status": True
    }
    return paramdict


def splilt_id(s):
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


def get_all_values(dict1, dict2):
    """
    Compare standard workflow with user workflow for multiple features, return a boolean representing the final result
    idea: for param! under each tool,  start a new dictionary{matched:xxx, mismached:xxx}, xxx is another
    dictionary{std_param: usrparam(or empty if not found)}.
    :param dict1:
    :param dict2:
    :return:
    """
    all_tools_correct = False
    all_parameters_correct = False
    tool_mistake = 0
    report = dict_initialize(len(dict1))

    number_param = 0
    param_mistakes = 0
    step = 0

    for key, value in dict1.items():
        # returns the name of the tool of each step.
        print("Now we are checking Step: " + key)
        exist = False  # 1. "exist" - to check if a tool was used:
        id = True
        dev = True
        version = True
        parameters = 0  # 2. "parameters" - to check if parameters were selected correctly:

        current_tool = value['name']
        current_parameters = value['tool_state']
        dict_for_thisloop = dict()
        dict_for_thisloop['param_values'] = dict()
        dict_for_thisloop['param_overall_status'] = True

        tool_state = tool_state_initialize()
        tool_id = tool_id_initialize()
        tool_dev = tool_dev_initialize()
        tool_version = tool_version_initialize()

        tool_state['expected_value'] = current_tool
        s_dev, s_id, s_version = splilt_id(value['tool_id'])
        tool_id['expected_id'] = s_id
        tool_dev['expected_dev'] = s_dev
        tool_version['expected_version'] = s_version

        for key1, value2 in dict2.items():
            if current_tool == "Input dataset" and value2['name'] == "Data Fetch":
                tool_state['user_value'] = value2['name']
                u_dev, u_id, u_version = splilt_id(value2['tool_id'])
                tool_id['user_id'] = u_id
                tool_dev['user_dev'] = u_dev
                tool_version['user_version'] = u_version

                if u_id != s_id:
                    id = False
                if u_version != s_version:
                    version = False
                if u_dev != s_dev:
                    dev = False

                value2['name'] = value2['name'] + "_used"
                exist = True
                parameters, tempd, number_param = check_parameters(current_parameters, value2['tool_state'],
                                                                   dict_for_thisloop)
                dict_for_thisloop = tempd
                break
            if value2['name'] == current_tool:
                tool_state['user_value'] = value2['name']
                u_dev, u_id, u_version = splilt_id(value2['tool_id'])
                tool_id['user_id'] = u_id
                tool_dev['user_dev'] = u_dev
                tool_version['user_version'] = u_version

                if u_id != s_id:
                    id = False
                if u_version != s_version:
                    version = False
                if u_dev != s_dev:
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
        report[step]['parameters'] = dict_for_thisloop

        # report the results of Tools
        if exist:
            all_tools_correct = True
            if id:
                tool_id['status'] = True
            if version:
                tool_version['status'] = True
            if dev:
                tool_dev['status'] = True
        else:
            print("Tool( " + current_tool + " ) was NOT used.")
            tool_mistake = tool_mistake + 1
            tool_state['status'] = False
            all_tools_correct = False

        report[step]['tool_used'] = tool_state
        report[step]['tool_id'] = tool_id
        report[step]['tool_dev'] = tool_dev
        report[step]['tool_version'] = tool_version
        step = step + 1

        # report the results of Parameters
        if parameters == 0:
            all_parameters_correct = True
        else:
            print("Parameters used in ( " + current_tool + " have " + str(parameters) + " mistakes")
            all_parameters_correct = False

    report['number_of_steps'] = len(dict1.keys())
    report['number_of_wrong_steps'] = tool_mistake

    if all_tools_correct:
        print("All Steps were carried out!")
    if not all_parameters_correct:
        print("There are some mistakes with parameters.")

    return report


def dict_initialize(nofsteps):
    newdict = dict()
    for i in range(nofsteps):
        newdict[i] = {
            "tool_used": dict(),
            "tool_id": dict(),
            "tool_dev": dict(),
            "tool_version": dict(),
            "parameters": dict(),
            "inputs": dict()
        }
    newdict['number_of_steps'] = 0
    newdict['number_of_wrong_steps'] = 0
    return newdict


def record_steps(dict_temp):
    list_temp = []
    for key, value in dict_temp.items():
        list_temp.append(value['name'])
    return list_temp


def check_parameters(str1, str2, current_dict):
    """
    further compare the parameters between two matched tools used
    a lot more details needed to be added here:
    e.g. some differences in the format will result in a count as mistake, but they are actually the same
      some values are set to as default in the newer version's of the tool, need to be excluded
      input connections have different values naturally

    :param current_dict:
    :param str1:
    :param str2:
    :return: the number of the mismatches
    """
    std_pr = json.loads(str1)
    user_pr = json.loads(str2)
    count = 0
    total_param_tobechecked = len(std_pr.keys())
    # not counting missing parameters as wrong at this moment.
    for k in std_pr.keys():
        current_dict['param_values'][k] = {
            "expected_input": std_pr[k],
            "user_input": "none",
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
            print("!!! parameter [" + k + "] does NOT exist in user inputs")

    return count, current_dict, total_param_tobechecked


def check_if_exist(term, wf):
    """
    OLD function used to check if the current tool in standard workflow exists in user workflow
    no longer in used, since it has been merged into the get_all_values.
    for the simplicity of the codes, maybe I will change it back.

    :param term:
    :param wf:
    :return: true or false
    """
    exist = False
    for key, value in wf.items():
        if term == "Input dataset" and value['name'] == "Data Fetch":
            value['name'] = value['name'] + "_used"
            exist = True
            break
        if value['name'] == term:
            value['name'] = value['name'] + "_used"
            exist = True
            break
    if exist:
        print("Tool( " + term + " ) was used.")
        return True
    else:
        print("Tool( " + term + " ) was NOT used.")
        return False
