import javalang
import re

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
    return len(tree)


def raw_text_attributes(file):
    ternary_op = re.findall(r"([_a-zA-Z0-9]*( *)=(.*?)[\?](.*?):( *)(.*))", file)
    return len(ternary_op),ternary_op
