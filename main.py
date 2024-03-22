from typing import List
import javalang
import os
import shutil
import re
import sys
import inspect
import time

import nodeutil
from greedystring import greedyTiling
import attributes
import config
from pathlib import Path

import pandas as pd
import numpy as np
import logging

LOGGER = logging.getLogger(__name__)



def main():
    start = time.time()
    config.initialise_logging()
    java_files = get_training_data(config.get_training_directory())

    if not java_files:
        return

    files = load_files(java_files)
    
    

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
            sys.stdout.flush()
            tree = javalang.parse.parse(text)
        except javalang.parser.JavaSyntaxError as inst:
            print(str(filename) + " couldn't compile")
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

def get_training_data(directory: str) -> List[str]:
    """Get list of training data files from directory"""
    dir_path = Path(directory)
    try:
        dir_path.exists()
        return os.listdir(directory)
    except Exception as e:
        LOGGER.error(f"Unable to get training data Error: {e}")
        raise e
    
def load_files(files: List[str]) -> dict:
    """Load files into memory"""
    files = {}
    for path in files:
        try:
            file = open(path, "r")
        except FileNotFoundError as e:
            print(f"File [{path}] not found: [{e}]")
        except Exception as e:
            raise e
        files[path] = file

    LOGGER.info(f"Found [{len(files)}] files")

if __name__ == "__main__":
    main()

