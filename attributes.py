from collections import defaultdict
from typing import List

import javalang
import re
import lizard
import pandas as pd  # used for creating dataframes


# --------------------------- Tree Attributes ---------------------------------#
def variable_name_style(tree):
    """ Method returns 3-tuple
            avg_var_length:     Stores the average length of variables in the tree
            num_type1_matches:  Stores the number of variables with the form "var_name"
            num_type2_matches:  Stores the number of variables with the form "varName"
    """

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


def token_length(tree):
    """ Returns number of tokens in the given tree """
    count = 0
    for x in tree:
        count += 1
    return count


# -------------------------- File Attributes -------------------------------------#
def ternary_op(file):
    """ Returns the number of ternary operator matches in the Java file """
    matches = re.findall(r"([_a-zA-Z0-9]*( *)=(.*?)[\?](.*?):( *)(.*))", file)
    return [len(matches)]


def line_length_calc(file="", toggle=5, col_toggle=False):
    """
    Calculates the number of occurrences of lines of different lengths. Lengths are rounded to the nearest 10
    :param toggle:  This dictates what the limit on the number of lengths.
                    A toggle of 5 will mean all lengths above toggle * 10 - 10 will be counted together
    :param file:    A string containing the java file that will be analysed
    :param col_toggle:  If this is set to true then the method returns a list of column names instead of the actual data
    :return data:   Returns a list containing the number of lines counted at each length
    :return col:    Returns a list containing the column names of each value in data
    """
    if col_toggle:
        col = []
        for x in range(toggle):
            temp_str = "LLC_" + str(x * 10)
            col.append(temp_str)
        return col

    file = [s.strip() for s in file.splitlines()]
    limit = toggle * 10 - 10
    lines = defaultdict(int)
    for x in file:
        line_length = len(x)
        rounded_length = int((line_length + 5) / 10) * 10
        # Everything above the limit is stored in the bucket allocated for the limit
        rounded_length = limit if rounded_length > limit else rounded_length
        lines[rounded_length] = lines[rounded_length] + 1

    data = []
    for x in range(toggle):
        data.append(lines[x * 10])
    return data


def accessor_metrics(file):
    """ Returns a list containing the relative frequency of 3 java access levels, public, private, protected"""
    public_match = len(re.findall(r"public", file))
    private_match = len(re.findall(r"private", file))
    protected_match = len(re.findall(r"protected", file))
    total_matches = public_match + private_match + protected_match
    data = [public_match/total_matches,
            private_match/total_matches,
            protected_match/total_matches]  # Converts to relative
    data = [100*x for x in data]    # Converts to a percentage
    return data


def comment_metric(file):
    """ Returns a list containing the number of 3 different types of java comments, single line, multi line, and doc"""
    single_comment = re.findall(r"//.*", file)
    multi_comment = re.findall(r"/\*(.*?)\*/", file, re.DOTALL)
    doc_comment = re.findall(r"/\*\*(.*?)\*\*/", file, re.DOTALL)
    multi_comment_len = len(multi_comment) - len(doc_comment) # every doc comment is a multi comment
    data = [len(single_comment), multi_comment_len, len(doc_comment)]
    return data


def space_metric(file):
    """ Returns a list containing the number of single and double spaces, as well as the number of tab spaces"""
    space = re.findall(r" ", file)
    db_space = re.findall(r"  ", file)
    tab_space = re.findall("\t", file)
    data = [len(space), len(db_space), len(tab_space)]
    return data


# ------------------------ Main Methods-----------------------------------------#
# These are the methods that are called from outside this file

def lizard_analysis(dir_path):
    """ Performs an analysis of the files in the dir_path directory using the lizard module"""
    print(lizard.__file__)
    data = lizard.main(["lizard.py", "-l", "java", dir_path])
    columns: List[str] = ["filename", "total_nloc", "avg_nloc", "avg_ccn", "avg_token", "function_cnt"]
    return data, columns


def get_tree_col():
    """ Returns the name of columns as a list, containing attributes calculated on the parsed AST from a java file"""
    columns = ["avg_var_length", "num_type1_var", "num_type2_var", "total_num_tokens"]
    return columns


def calculate_tree_attributes(tree):
    """ Calculates metrics on the given tree and returns data as a list"""
    avg_var_length, num_type1_matches, num_type2_matches = variable_name_style(tree)
    num_tokens = token_length(tree)
    data = [avg_var_length, num_type1_matches, num_type2_matches, num_tokens]

    return data


def get_raw_col():
    """ Returns the name of columns as a list, containing attributes calculated on the raw java file"""
    llc_col = line_length_calc("", 5, True)
    accessor_col = ['rel_pub', 'rel_priv', 'rel_prot']
    comment_col = ['sin_comm', 'multi_comm', 'doc_comm']
    space_col = ['sin_space', 'db_space', 'tab']
    columns = ['ternary'] + llc_col + accessor_col + comment_col + space_col
    return columns


def calculate_raw_attributes(file):
    """ Calculates metrics on the given file and returns data as a list"""
    tern_data = ternary_op(file)
    llc_data = line_length_calc(file, 5, False)
    accessor_data = accessor_metrics(file)
    comment_data = comment_metric(file)
    space_data = space_metric(file)
    data = tern_data + llc_data + accessor_data + comment_data + space_data
    return data
