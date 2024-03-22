import javalang
import os
import sys  # used for system exceptions
import time  # used to record how long methods take to run
import itertools    # used for combinations
import util
import pickle
import operator
import attributes
import constants
import math
from results import Result
import config
from collections import defaultdict

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

import pandas as pd
import numpy as np


def create_df(lizard_data, lizard_col, file_data, file_columns, outbox):

    util.print_tk(outbox, "Creating Dataframes\n")
    lizard_df = pd.DataFrame(lizard_data, columns=lizard_col)
    lizard_df.set_index("filename", inplace=True)

    raw_tree_df = pd.DataFrame(file_data, columns=file_columns)
    raw_tree_df.set_index("filename", inplace=True)

    attribute_df = pd.concat([lizard_df, raw_tree_df], axis=1, sort=True).astype(float)
    attribute_df.reset_index(inplace=True)   # gets rid of filename index
    attribute_df.rename(columns={"index": "filename"}, inplace=True)

    full_df_col = list(attribute_df)     # gets the column values from full dataframe
    full_df_rows = attribute_df.values.tolist()   # getting all the rows from the full dataframe

    util.print_tk(outbox, "Computing combinations\n")
    # Gets all combinations of the attributes of each file
    final_df_list = []
    for file1_att, file2_att in itertools.combinations(full_df_rows, 2):
        if util.STOPFLAG:
            break      # Used to exit function
        filename_1 = file1_att[0]
        filename_2 = file2_att[0]
        # Sets an order to the filenames to make it easier to access specific rows later from the dataframe
        filenames = [filename_1, filename_2] if filename_1 < filename_2 else [filename_2, filename_1]
        data = []
        for i, j in zip(file1_att[1:], file2_att[1:]):
            if i != 0 or j != 0:
                data.append(abs(i - j))
            else:
                data.append(np.nan)
        final_df_list.append(filenames + data)

    # Adds column headings to rows and creates a final dataframe
    final_df_col = ["filename_1_", "filename_2_"] + full_df_col[1:]
    final_df = pd.DataFrame(final_df_list, columns=final_df_col)
    final_df.set_index(['filename_1_', 'filename_2_'], inplace=True)
    # final_df = final_df.reindex(sorted(final_df.columns), axis=1)   # reorders columns based on alphabetic order
    return final_df


def main(source_dir, output_dir, outbox):

    source_dir = source_dir.split("/")[-1] + "/"
    print(source_dir)
    start = time.time()  # #start recording how long program takes
    try:
        javadir = os.listdir(source_dir)  # directory where all java files will be stored
    except FileNotFoundError as inst:
        util.print_tk(outbox, "Incorrect Directory Entered\n")
        return 0

    util.print_tk(outbox, "Reading Files..\n")

    files = []
    file_map = {}
    tree_map = {}  # Stores all trees created from the all the files in a separate dictionary
    lizard_data, lizard_col = attributes.lizard_analysis(source_dir)
    file_data = []
    file_columns = ["filename"] + attributes.get_raw_col() + attributes.get_tree_col()

    util.print_tk(outbox, "Calculating attributes for files...\n")

    for filename in javadir:
        print(filename)
        if filename[-5:] != ".java":    # Ensures that the current file is a java file
            continue
        address = source_dir + str(filename)
        try:

            file = open(address, "r")
            # files[str(filename)] = file
            files.append(str(filename))

            temp = [source_dir + filename]
            text = "".join(file.readlines())
            file_map[filename] = text
            data_raw = attributes.calculate_raw_attributes(text)

            tree = javalang.parse.parse(text)
            data_tree = attributes.calculate_tree_attributes(tree)

            temp = temp + data_raw + data_tree
            file_data.append(temp)

        except FileNotFoundError:
            util.print_tk(outbox, "File " + str(filename) + " was not found\n")
        except javalang.parser.JavaSyntaxError as inst:
            util.print_tk(outbox, str(filename) + " couldn't compile\n")

    score_map = {}  # Map used to store the scores of each pair of files
    distro_map = defaultdict(int)   # Map used to store the distribution of scores

    # Load Random Forest Model
    rf_regressor = pickle.load(open(config.get_rf_model_path(), 'rb'))

    test_df = create_df(lizard_data, lizard_col, file_data, file_columns, outbox)
    test_df = test_df.fillna(-1)

    pred_rf = rf_regressor.predict(test_df.values)

    test_df['similarity'] = pred_rf * 100
    final_df = test_df[test_df['similarity'] > constants.SIMILARITY_THRESHOLD]
    final_df = final_df[['similarity']]
    final_df = final_df.reset_index()
    final_df = final_df.sort_values('similarity', ascending=False)

    score_list = final_df.values.tolist()
    dir_length = len(source_dir)
    sorted_scores = []
    for data in score_list:
        filename1 = data[0][dir_length:]
        filename2 = data[1][dir_length:]
        score = int(data[2] * 100) / 100
        sorted_scores.append(((filename1, filename2), score))

        rounded_score = int(math.ceil(score / 10.0)) * 10
        distro_map[rounded_score] += 1

    sorted_distro = sorted(distro_map.items(), key=operator.itemgetter(0), reverse=True)

    end = time.time()  # stop recording time
    util.print_tk(outbox, "Execution time: " + str(end - start) + " seconds")
    if util.STOPFLAG:
        util.print_tk(outbox, "Comparisons interrupted\n")
        util.STOPFLAG = False
    else:
        util.print_tk(outbox, "--Finished Comparisons--\n")

    message = """
    These are the results computed using the application of machine learning to attribute counting. The model used for
    these scores was a trained random forest model. Each score is presented as a percentage where each percentage 
    represents the average similarity between files. This means that extending one file will not affect the score."""

    res = Result(files, message, output_dir, sorted_scores, sorted_distro, "ml", file_map)
    res.print_html()

    # h = res.get_hm()


