import javalang
import os
import shutil
import re
import sys  # used for system exceptions
import inspect  # used to check objects for all methods
import time  # used to record how long methods take to run

import nodeutil  # contains util methods
from greedystring import greedyTiling
import attributes
import constants

import pandas as pd
import numpy as np

start = time.time()  # #start recording how long program takes

currDirectory = "jfiles/"
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

# Calculates similarity score for 2 ast's based on the matches

#  Stores all trees created from the all the files in a seperate dictionary: treeMap
treeMap = {}
for filename, file in files.items():
    try:
        text = "".join(file.readlines())
        print(str(filename) + ": "+str(attributes.raw_text_attributes(text)))
        tree = javalang.parse.parse(text)
    except javalang.parser.JavaSyntaxError as inst:
        print(str(filename) + " couldnt compile")
        print(inst)
    treeMap[filename] = tree

#  2 loops used to go through all pairings of files and perform a structure based method on all of then_statement
#  The scores are stored in the score map
scoreMap = {}

# -------------------  Greedy String Tiling  ---------------------#
# for filename_1, tree_1 in treeMap.items():
#     for filename_2, tree_2 in treeMap.items():
#
#         # checks if comparing the same files. If so the current tree is skipepd
#         if filename_1 == filename_2:
#             continue
#
#         # the next section ensures that the key for 2 trees in the score map will be the same no matter
#         # which tree is tree_1 / tree_2
#         hash1 = hash(filename_1)
#         hash2 = hash(filename_2)
#         if hash1 >= hash2 :
#             key = (filename_1, filename_2)
#         else:
#             key = (filename_2, filename_1)
#
#         # checking if the score for the set of files has already been calculated. If so move onto next file
#         if key in scoreMap:
#             continue
#
#         score = greedyTiling(tree_1,tree_2)
#         print("Comparing " + filename_1 + "-" + filename_2 + ": "+str(score))
#         scoreMap[key] = score

# f = open("result.txt","w")
# for key,score in scoreMap.items():
#     if score > constants.SIMILARITY_THRESHOLD:
#         f.write("Similarity Score for " + str(key) + " is : "+ str(score))
#
# ----------------  End of Greedy String Tiling  ----------------#
tuplelist = []

# for filename, tree in treeMap.items():
#     x = (filename, attributes.variable_name_style(tree))
#     tuplelist.append(x)
#     print(x)

end = time.time()  # stop recording time
print("Execution time: " + str(end - start) + " seconds")
