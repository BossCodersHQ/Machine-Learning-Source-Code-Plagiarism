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
from spellchecker import SpellChecker
import re
#%%
print("hello")
#%%

file = open("jfiles/GenericList.java", "r")
file = "".join(file.readlines())
import time

from tqdm import tqdm
# x =[i for i in range(10)]
# for i in tqdm(x):
#     time.sleep(3)
x = pd.read_csv("dataframes/attribute_df_soco_a1.csv", header=0)
# type1 = "^[_a-z0-9]+"
# type2 = "^[a-z0-9]+(?:[A-Z]+[a-z0-9]*)+"
# type3 = "^[_A-Z0-9]+"
#
# word = "test_variable2_vaeg"
# word2 = "stringCoundtGhana"
# word3 = "CONSTANT2_VAR23FAR"
#
# new_word = re.split(r'[^a-zA-Z]', word)
# new_word2 = re.split(r'([A-Z]?[a-z]*)', word2)
# new_word3 = re.split(r'[^A-Z]', word3)

# new_word = [i for i in new_word if i != '']


