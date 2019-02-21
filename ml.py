import javalang
import os
import shutil
import re
import sys  # used for system exceptions
import inspect  # used to check objects for all methods
import time  # used to record how long methods take to run
import itertools    # used for combinations

import nodeutil  # contains util methods
from greedystring import greedy_tiling
import attributes
import constants

import pandas as pd
import numpy as np

start = time.time()  # #start recording how long program takes

currDirectory = "jfiles2/"
# currDirectory = constants.SOCO_TRAIN

# try using the os module to open a file
javadir = os.listdir(currDirectory)  # directory where all java files will be stored

files = {}      # Stores all file names
treeMap = {}    # Stores all trees created from the all the files in a seperate dictionary: treeMap
lizard_data, lizard_col = attributes.lizard_analysis(currDirectory)
file_data = []
faulty_files = []
file_columns = ["filename"] + attributes.get_raw_col() + attributes.get_tree_col()

# Loops through all files in the given javadir directory
# Each file opened then raw attributes calculated first. THis is done to ensure that raw attributes are calculated for
# every file. Next tree attributes are calculated
for filename in javadir:
    address = currDirectory + str(filename)
    try:
        file = open(address, "r")
        files[str(filename)] = file

        temp = [currDirectory + filename]
        text = "".join(file.readlines())
        data_raw = attributes.calculate_raw_attributes(text)

        tree = javalang.parse.parse(text)
        data_tree = attributes.calculate_tree_attributes(tree)

        temp = temp + data_raw + data_tree
        file_data.append(temp)

        treeMap[filename] = tree
    except FileNotFoundError:
        print("File " + str(filename) + " was not found")
    except javalang.parser.JavaSyntaxError as inst:
        print(str(filename) + " couldn't compile")
        faulty_files.append(filename)
        print(inst)
    except:
        print(sys.exc_info()[0])

print(len(files))

lizard_df = pd.DataFrame(lizard_data, columns=lizard_col)
lizard_df.set_index("filename", inplace=True)

raw_tree_df = pd.DataFrame(file_data, columns=file_columns)
raw_tree_df.set_index("filename", inplace=True)

attribute_df = pd.concat([lizard_df, raw_tree_df], axis=1, sort=True).astype(float)
attribute_df.reset_index(inplace=True)   # gets rid of filename index

full_df_col = list(attribute_df)     # gets the column values from full dataframe
full_df_rows = attribute_df.values.tolist()   # getting all the rows from the full dataframe

# Gets all combinations of the attributes of each file
final_df_list = []
for file1_att, file2_att in itertools.combinations(full_df_rows, 2):
    final_df_list.append(list(file1_att) + list(file2_att))

# Adds column headings to rows and creates a final dataframe
final_df_col = [col + "_1_" for col in full_df_col] + [col + "_2_" for col in full_df_col]
final_df = pd.DataFrame(final_df_list, columns=final_df_col)
final_df.set_index(['filename_1_', 'filename_2_'], inplace=True)
final_df = final_df.reindex(sorted(final_df.columns), axis=1)   # reorders columns based on alphabetic order
final_df['similarity'] = 0  # initialises similarity column. This is used to classify files

f = open(constants.SOCO_JUDGEMENTS, "r")
pairings = []
for line in f:
    pair = line.split(" ")
    pair[0] = currDirectory + pair[0]
    pair[1] = currDirectory + pair[1][:-1]
    pairings.append(tuple(pair))

# The following loop checks if any of the files are known to be copied, if so it sets their similarity score to 1
for pair in pairings:
    try:
        final_df.loc[[pair], ["similarity"]] = 1
    except KeyError as ke:
        continue

# # print to file
# final_df.to_csv("dataframes/SOCO_TRAIN.csv", index = False)
# print(df)

tuplelist = []

# for filename, tree in treeMap.items():
#     x = (filename, attributes.variable_name_style(tree))
#     tuplelist.append(x)
#     print(x)

end = time.time()  # stop recording time
print("Execution time: " + str(end - start) + " seconds")
