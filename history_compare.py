#!/usr/bin/env python3

def compare(user_workflow, standard_workflow):
    # print(standard_workflow['steps']['3']['name'])
    temp1 = standard_workflow['steps']
    temp2 = user_workflow['steps']
    get_all_values(temp1, temp2)
    print("Every step was executed as expected, good job!")


def get_all_values(dict1, dict2):
    for key, value in dict1.items():
        if type(value) is dict1:
            print("here!1")
            get_all_values(value, dict2)
        else:
            # print(key, ":", value)
            # returns the name of the tool of each step. We can potentially check the names in the userwf here.
            print("Now we are checking: " + value['name'])
            check_if_exist(value['name'], dict2)


def check_if_exist(term, wf):
    exist = False
    for key, value in wf.items():
        if type(value) is wf:
            check_if_exist(value, wf)
            print("here!")
        else:
            if term == "Input dataset" and value['name'] == "Data Fetch":
                exist = True
            if value['name'] == term:
                exist = True
    if exist:
        print("Tool( " + term + " ) was used.")
