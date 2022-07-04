#!/usr/bin/env python3
import json


def compare(user_workflow, standard_workflow):
    """
    This function takes in the two workflows generated in the main.py,
    and passes them into the function where the actual comparison happens.
    Potentially, it will be linked to the yaml/json output for generating the report

    :param user_workflow:
    :param standard_workflow:
    :return: report (as a dictionary)
    """

    temp1 = standard_workflow['steps']
    temp2 = user_workflow['steps']
    result = get_all_values(temp1, temp2)
    # if result:
    #     print("Every step was executed as expected, good job!")
    #     return report
    # else:
    #     print("Some mistakes were made.")
    return result


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
    report = dict_initialize()
    dict_tools = dict()
    dict_param = dict()
    tool_score = 100
    penalty = 100/len(dict1.keys())
    param_mistakes = 0
    std_list = []
    usr_list = record_steps(dict2)
    # {keyName1: value1, keyName2: value2, keyName3: [val1, val2, val3]}

    for key, value in dict1.items():
        # returns the name of the tool of each step.
        print("Now we are checking Step: " + value['name'])

        exist = False  # 1. "exist" - to check if a tool was used:
        parameters = 0  # 2. "parameters" - to check if parameters were selected correctly:

        current_tool = value['name']
        current_parameters = value['tool_state']
        dict_for_thisloop = dict()
        dict_for_thisloop['standard_param'] = current_parameters
        std_list.append(current_tool)

        for key1, value2 in dict2.items():
            if current_tool == "Input dataset" and value2['name'] == "Data Fetch":
                value2['name'] = value2['name'] + "_used"
                exist = True
                parameters = check_parameters(current_parameters, value2['tool_state'])
                break
            if value2['name'] == current_tool:
                value2['name'] = value2['name'] + "_used"
                exist = True
                dict_for_thisloop['user_param'] = value2['tool_state']
                parameters = check_parameters(current_parameters, value2['tool_state'])
                break

        param_mistakes = param_mistakes + parameters
        dict_param[current_tool] = dict_for_thisloop

        # report the results of Tools
        if exist:
            all_tools_correct = True
        else:
            print("Tool( " + current_tool + " ) was NOT used.")
            tool_score = tool_score - penalty
            all_tools_correct = False

        # report the results of Parameters
        if parameters == 0:
            all_parameters_correct = True
        else:
            print("Parameters used in ( " + current_tool + " have " + str(parameters) + " mistakes")
            all_parameters_correct = False

    dict_tools['score'] = tool_score
    dict_tools['standard_steps'] = std_list
    dict_tools['user_steps'] = usr_list
    dict_param['number of mismatches'] = param_mistakes

    report['tool_selection'] = dict_tools
    report['parameters'] = dict_param

    if all_tools_correct:
        print("All Steps were carried out!")
    if not all_parameters_correct:
        print("There are some mistakes with parameters.")

    return report


def dict_initialize():
    newdict = dict()
    emptydict = dict()
    newdict['score'] = 100
    newdict['tool_selection'] = emptydict
    newdict['tool_versions'] = emptydict
    newdict['input_connection'] = emptydict
    newdict['parameters'] = emptydict
    return newdict


def record_steps(dict_temp):
    list_temp = []
    for key, value in dict_temp.items():
        list_temp.append(value['name'] )
    return list_temp


def check_parameters(str1, str2):
    """
    further compare the parameters between two matched tools used
    a lot more details needed to be added here:
    e.g. some differences in the format will result in a count as mistake, but they are actually the same
      some values are set to as default in the newer version's of the tool, need to be excluded
      input connections have different values naturally

    :param str1:
    :param str2:
    :return: the number of the mismatches
    """
    std_pr = json.loads(str1)
    user_pr = json.loads(str2)
    count = 0
    std_step_param = dict()
    user_step_param = dict()

    # not counting missing parameters as wrong at this moment.
    for k in std_pr.keys():
        std_step_param[k] = std_pr[k]
        # print("Current Parameter is: " + k)
        if k in user_pr:
            if std_pr[k] != user_pr[k]:
                count = count + 1
        else:
            print("!!! parameter [" + k + "] does NOT exist in user inputs")

    return count


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
