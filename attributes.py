import javalang
import re
import lizard
import pandas as pd  # used for creating dataframes

""" Method returns 3-tuple
        avg_var_length:     Stores the average length of variables in the tree
        num_type1_matches:  Stores the number of variables with the form "var_name" 
        num_type2_matches:  Stores the number of variables with the form "varName"
"""


def variable_name_style(tree):
    type1 = "^[a-zA-Z0-9]+(_[a-zA-Z0-9]*)+"  # first type of variable nameing
    type2 = "^[a-z0-9]+([A-Z]+[a-zA-Z0-9])+"  # second type of variable nameming

    num_type1_matches = 0
    num_type2_matches = 0

    total_var_count = 0  # stores the total number of variables
    total_len = 0  # stores the total length of aall variables
    for path, node in tree.filter(javalang.tree.LocalVariableDeclaration):
        # list = [method_name for method_name in dir(node) if callable(getattr(node, method_name))]
        # print(node)
        # vartype = getattr(getattr(node, 'type'), 'name')
        name = getattr(getattr(node, 'declarators')[0], 'name')
        matches_type1 = re.findall(type1, name)
        matches_type2 = re.findall(type2, name)

        num_type1_matches += len(matches_type1)
        num_type2_matches += len(matches_type2)

        total_var_count += 1
        total_len += len(name)
    for path, node in tree.filter(javalang.tree.VariableDeclarator):
        name = getattr(node, 'name')
        matches_type1 = re.findall(type1, name)
        matches_type2 = re.findall(type2, name)

        num_type1_matches += len(matches_type1)
        num_type2_matches += len(matches_type2)

        total_var_count += 1
        total_len += len(name)
    try:
        avg_var_length = total_len / total_var_count
    except ZeroDivisionError as zt:
        avg_var_length = None

    return avg_var_length, num_type1_matches, num_type2_matches


#  returns number of tokens in treeMap
def token_length(tree):
    count = 0
    for x in tree:
        count += 1
    return count


def ternary_op(file):
    matches = re.findall(r"([_a-zA-Z0-9]*( *)=(.*?)[\?](.*?):( *)(.*))", file)
    return len(matches), matches


# ------------------------ Main Methods-----------------------------------------#
# These are the methods that are called from outside this file

def lizard_analysis(dir_path):
    print(lizard.__file__)
    data = lizard.main(["lizard.py", "-l", "java", dir_path])
    columns = ["filename", "total_nloc", "avg_nloc", "avg_ccn", "avg_token", "function_cnt"]
    return data, columns


def get_tree_col():
    columns = ["avg_var_length", "num_type1_var", "num_type2_var", "total_num_tokens"]
    return columns


def calculate_tree_attributes(tree):
    avg_var_length, num_type1_matches, num_type2_matches = variable_name_style(tree)
    num_tokens = token_length(tree)
    data = [avg_var_length, num_type1_matches, num_type2_matches, num_tokens]

    return data


def get_raw_col():
    columns = ['ternary']
    return columns


def calculate_raw_attributes(file):
    len = ternary_op(file)[0]
    data = [len]

    return data
