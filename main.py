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


javadir = os.listdir(currDirectory)  # directory where all java files will be stored

# try using the os module to open a file

# for filename in tokendir:
#     if str(filename) not in dir:
#         print(filename)


# files = []
# for filename in javadir:
#     address = constants.SOCO_TRAIN + str(filename)
#     try:
#         file = open(address, "r")
#     except FileNotFoundError:
#         print("File "+str(filename)+" was not found")
#     except:
#         print (sys.exc_info()[0])
#
#     files.append(file)   #   adds file to the list of all files
#
#     try:
#         tree = javalang.parse.parse("".join(file.readlines()))
#     except javalang.parser.JavaSyntaxError as inst:
#         print(str(filename) + " couldnt compile")
#         print(inst)
# print(len(files))

files = {}
for filename in javadir:
    address = currDirectory + str(filename)
    try:
        file = open(address, "r")
    except FileNotFoundError:
        print("File " + str(filename) + " was not found")
    except:
        print(sys.exc_info()[0])

    files[str(filename)] = file

print(len(files))

#     tokenaddress = "tokenFiles/"+str(filename) + ".txt"
#     tokenfile = open(tokenaddress, "w")
#
#     # tokenfile.write(tree.types)
#     for path,node in tree:
#         # tokenfile.write(str(path) + "\n")
#         tokenfile.write(str(type(node))[22:-2] + " ")
#         if "name" in node.attrs:
#             tokenfile.write("name= " + str(node.name) + " ")
#         if "value" in node.attrs:
#             tokenfile.write("value= " + str(node.value) + " ")
#         tokenfile.write("\n")
#     # tokenfile.write(str(node.attrs) + " type = " + "\n\n")
#
# # print file.readlines()

# Calculates similarity score for 2 AST's based on the matches

#  Stores all trees created from the all the files in a seperate dictionary: treeMap
treeMap = {}
# lizard_data, lizard_col = attributes.lizard_analysis(currDirectory)
# file_data = []
# faulty_files = []
# file_columns = ["filename"] + attributes.get_raw_col() + attributes.get_tree_col()
for filename, file in files.items():
    try:
        # temp = [currDirectory + filename]
        text = "".join(file.readlines())
        # data_raw = attributes.calculate_raw_attributes(text)

        tree = javalang.parse.parse(text)
        # data_tree = attributes.calculate_tree_attributes(tree)

        # temp = temp + data_raw + data_tree
        # file_data.append(temp)

    except javalang.parser.JavaSyntaxError as inst:
        print(str(filename) + " couldn't compile")
        # faulty_files.append(filename)
        print(inst)
    treeMap[filename] = tree
# # for x in file_data:
# #     print(x)
# lizard_df = pd.DataFrame(lizard_data, columns=lizard_col)
# lizard_df.set_index("filename", inplace=True)
#
# raw_tree_df = pd.DataFrame(file_data, columns=file_columns)
# raw_tree_df.set_index("filename", inplace=True)
#
# attribute_df = pd.concat([lizard_df, raw_tree_df], axis=1, sort=True).astype(float)
# attribute_df.reset_index(inplace=True)   # gets rid of filename index
#
# full_df_col = list(attribute_df)     # gets the column values from full dataframe
# full_df_rows = attribute_df.values.tolist()   # getting all the rows from the full dataframe
#
# final_df_list = []
# for file1_att, file2_att in itertools.combinations(full_df_rows, 2):
#     final_df_list.append(list(file1_att) + list(file2_att))
#
# final_df_col = [col + "_1_" for col in full_df_col] + [col + "_2_" for col in full_df_col]
# final_df = pd.DataFrame(final_df_list, columns=final_df_col)
# final_df.set_index(['filename_1_', 'filename_2_'], inplace=True)
# final_df['similarity'] = 0
#
# f = open(constants.SOCO_JUDGEMENTS, "r")
# pairings = []
# for line in f:
#     pair = line.split(" ")
#     pair[0] = currDirectory + pair[0]
#     pair[1] = currDirectory + pair[1][:-1]
#     pairings.append(tuple(pair))
# # print(pairings)
# # The following loop checks if any of the files are known to be copied, if so it sets their similarity score to 1
# for pair in pairings:
#     try:
#         final_df.loc[[pair], ["similarity"]] = 1
#     except KeyError as ke:
#         continue
#
# final_df.to_csv("dataframes/SOCO_TRAIN.csv", index = False)
# print(df)

# for x in pairings:
#     print(x)


#  2 loops used to go through all pairings of files and perform a structure based method on all of then_statement
#  The scores are stored in the score map
scoreMap = {}
print(treeMap)
# -------------------  Greedy String Tiling  ---------------------#
for filename_1, tree_1 in treeMap.items():
    for filename_2, tree_2 in treeMap.items():

        # checks if comparing the same files. If so the current tree is skipepd
        if filename_1 == filename_2:
            continue

        # the next section ensures that the key for 2 trees in the score map will be the same no matter
        # which tree is tree_1 / tree_2
        hash1 = hash(filename_1)
        hash2 = hash(filename_2)
        if hash1 >= hash2 :
            key = (filename_1, filename_2)
        else:
            key = (filename_2, filename_1)

        # checking if the score for the set of files has already been calculated. If so move onto next file
        if key in scoreMap:
            continue

        score = greedy_tiling(tree_1, tree_2)
        # print(score)
        print("Comparing " + filename_1 + "-" + filename_2 + ": "+str(score))
        scoreMap[key] = score

f = open("result.txt","w")
for key,score in scoreMap.items():
    if score > constants.SIMILARITY_THRESHOLD:
        f.write("Similarity Score for " + str(key) + " is : "+ str(score))

# ----------------  End of Greedy String Tiling  ----------------#
tuplelist = []

# for filename, tree in treeMap.items():
#     x = (filename, attributes.variable_name_style(tree))
#     tuplelist.append(x)
#     print(x)

end = time.time()  # stop recording time
print("Execution time: " + str(end - start) + " seconds")
