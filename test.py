import pandas as pd
import numpy as np
import re
# data = [[113, 54, 10.5, 300, 2],
#         [157, 25, 3, 185, 6],
#         [44, 19, 3, 120, 2],
#         [81, 17.5, 2.5, 130]]
#
# df = pd.DataFrame(data,columns=["NLOC", "avg.nloc","avg.ccn","avg.token","function_cnt"])
# print(df)
#
# '{module.average_nloc:10.1f}{module.average_cyclomatic_complexity:8.1f}{module.average_token_count:11.1f}'
from collections import defaultdict
import operator

air_file = open("jfiles/ArrayExamples.java", "r")
air_file = "".join(air_file.readlines())


# file = [s.strip() for s in file.splitlines()]


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


a = accessor_metrics(air_file)
d = comment_metric(air_file)
y = space_metric(air_file)
