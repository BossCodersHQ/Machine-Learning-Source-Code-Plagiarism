import javalang
import os
import util
import shutil
import re
import sys  # used for system exceptions
import inspect  # used to check objects for all methods
import time  # used to record how long methods take to run
import itertools  # used for combinations

import nodeutil  # contains util methods
from quickGST import main as quick_gst
import attributes
import math
from scipy import stats
import constants
from tqdm import tqdm

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

import pandas as pd
import numpy as np

from bs4 import BeautifulSoup

start = time.time()  # #start recording how long program takes

SPLIT_DF = 50000

# curr_directory = "jfiles/"  # Make sure this is also the name of the judgements file that will be used
curr_directory = constants.SOCO_A1
df_name = "soco_a1"

javadir = os.listdir(curr_directory)  # directory where all java files will be stored
num_files = len(javadir)


# files = {}      # Stores all file names
files = []  # Stores al file names without storing files
treeMap = {}  # Stores all trees created from the all the files in a separate dictionary:
lizard_data, lizard_col = attributes.lizard_analysis(curr_directory)
file_data = []
error_msgs = {}
faulty_files = []
file_columns = ["filename"] + attributes.get_raw_col() + attributes.get_tree_col()

# progress_count = 0
# ten_percent = int(num_files / 10)
# iteration = 1
log = open("logs/log.txt", "w+")
# Loops through all files in the given javadir directory
# Each file opened then raw attributes calculated first. THis is done to ensure that raw attributes are calculated for
# every file. Next tree attributes are calculated
for filename in tqdm(javadir):
    address = curr_directory + str(filename)
    try:
        file = open(address, "r")
        # files[str(filename)] = file

        temp = [curr_directory + filename]
        text = "".join(file.readlines())

        # progress_count += 1
        # if progress_count >= ten_percent:
        #
        #     progress_count = 0
        #     print(iteration*10, "  more completed")
        #     iteration += 1

        data_raw = attributes.calculate_raw_attributes(text)

        # Done afterwards so that the raw attributes can be calculated even if the code can't compile
        tree = javalang.parse.parse(text)
        data_tree = attributes.calculate_tree_attributes(tree)

        temp = temp + data_raw + data_tree
        file_data.append(temp)
        files.append(str(filename))
        # treeMap[filename] = tree
    except FileNotFoundError:
        print("File " + str(filename) + " was not found")
    except javalang.parser.JavaSyntaxError as inst:
        print(str(filename) + " couldn't compile")
        faulty_files.append(filename)
        error_msgs[filename] = 1
    except javalang.tokenizer.LexerError as inst:
        error_msgs[filename] = 2
        continue
    except UnicodeDecodeError as inst:
        error_msgs[filename] = 3
        continue
    except AttributeError as inst:
        error_msgs[filename] = 4
        continue
    except Exception as inst:
        print(filename, type(inst), inst)
        error_msgs[filename] = 5

msg = str(len(files)) + " have been scanned."
print(msg)
#
# # for name in faulty_files:
# #     msg = name + " couldn't compile"
# #     log.write(msg)
# # for name, msg in error_msgs.items():
# #     msg = name + " had the error " + str(msg)
# #     log.write(msg)
# --------------------------------------------------#
# ----------------- Working with Data Frames --------#

print("Creating Data frames")
lizard_df = pd.DataFrame(lizard_data, columns=lizard_col)
lizard_df.set_index("filename", inplace=True)

raw_tree_df = pd.DataFrame(file_data, columns=file_columns)
raw_tree_df.set_index("filename", inplace=True)

attribute_df = pd.concat([lizard_df, raw_tree_df], axis=1, sort=True).astype(float)
attribute_df.reset_index(inplace=True)  # gets rid of filename index
attribute_df.rename(columns={"index": "filename"}, inplace=True)
# Drops Nan values
# Uncomment # @then gets rid of anomalies by classifying everything greater than 3 standard deviations away from the
# mean as an anomaly
attribute_df.dropna(inplace=True)
# attribute_df = attribute_df[(np.abs(stats.zscore(attribute_df.iloc[:, 1:])) < 3).all(axis=1)]
attribute_df.drop("num_type4_var", axis=1, inplace=True)

#-------------------------------------------------------#

attribute_df = pd.read_csv("dataframes/attribute_df_soco_a1.csv", header=0)
attribute_df.drop("Unnamed: 0",axis=1, inplace=True)

#-------------------------------------------------------#

full_df_col = list(attribute_df)  # gets the column values from full data frame
full_df_rows = attribute_df.values.tolist()  # getting all the rows from the full data frame

# Calculating scores using improved GST for every pair of files
score_map = quick_gst(curr_directory[:-1], None, None)

print("getting combinations")

# List thats used to store all lists's containing attributes on each pair of files
final_df_list = []

final_df_col = ["filename_1_", "filename_2_"] + full_df_col[1:] + ["gst_sim", "euclid_dist", "cosine_dist"]

size_count = 0  # Used as a counter to ensure the length of the list doesnt exceed the available size in memory
iteration_no = 0

n = len(attribute_df)
total_comparisons = (n * (n - 1)) / 2
ten_percent = math.ceil(total_comparisons/10)
progress_counter = 0
progress_iter = 0

for file1_att, file2_att in itertools.combinations(full_df_rows, 2):
    progress_counter += 1
    if progress_counter >= ten_percent:
        progress_counter = 0
        progress_iter += 10
        print("Completed " + str(progress_iter) + "%")

    filename_1 = file1_att[0].replace(curr_directory, "")
    filename_2 = file2_att[0].replace(curr_directory, "")

    sys.stdout.write("\033[K")

    # Sets an order to the filenames to make it easier to access specific rows later from the dataframe
    filenames = [filename_1, filename_2] if filename_1 < filename_2 else [filename_2, filename_1]
    data = []

    # Looks through all attribute values for each file to see if there is any 0s present. If not then the difference of
    # each file is calculates( file 1 attributes - file 2 attributes).
    for i, j in zip(file1_att[1:], file2_att[1:]):
        if i == 0 and j == 0:
            data.append(np.nan)
        else:
            temp = abs(i - j)
            if temp == 0:
                temp -= math.sqrt(i)
            else:
                avg = (i + j) / 2.0
                temp -= math.log(avg)
            data.append(temp)

    # Adds the calculated greedy string tiling similarity score between files and adds them to the data list
    try:
        f1 = filename_1.replace(curr_directory, "")
        f2 = filename_2.replace(curr_directory, "")
        gst_sim = score_map[f1, f2] if f1 <= f2 else score_map[f2, f1]
    except KeyError as ke:
        gst_sim = 0.0
    except Exception as inst:
        gst_sim = np.nan

    data.append(gst_sim)

    # Calculating distance metrics----------------#
    euclid_dist = util.euclid_dist(file1_att[1:], file2_att[1:])
    cosine_sim = util.cosine_sim(file1_att[1:], file2_att[1:])
    # ----------------------------------------------#

    # Adding full row to the a list containing all rows
    final_df_list.append(filenames + data + [euclid_dist, cosine_sim])

    size_count += 1     # Incrementing count variable

    # Once the size of the data frame has reached a specific size then the list is written to a data frame which is then
    # written to a new file.
    if size_count >= SPLIT_DF:
        filename = "dataframes/" + df_name + "_part_" + str(iteration_no) + ".csv"
        iteration_no += 1
        size_count = 0

        final_df = pd.DataFrame(final_df_list, columns=final_df_col)
        final_df.set_index(['filename_1_', 'filename_2_'], inplace=True)

        final_df.to_csv(filename, index=True)
        final_df_list = []

if len(final_df_list) != 0:
    # Adds column headings to rows and creates a final dataframe
    filename = "dataframes/" + df_name + "_part_" + str(iteration_no) + ".csv"
    final_df = pd.DataFrame(final_df_list, columns=final_df_col)
    final_df.set_index(['filename_1_', 'filename_2_'], inplace=True)
    final_df.to_csv(filename, index=True)





# final_df['similarity'] = 0  # initialises similarity column. This is used to classify files


# # ----------------------- Computing Similarity Scores ---------------------#
#
# # Uses Beautiful soup to parse html file generated by Jplag to a base for similarity scores
# addr = "judgements/jplag/" + curr_directory[:-1] + ".html"
# html_file = open(addr, 'r')
# soup = BeautifulSoup(html_file, 'html.parser')
#
# x = soup.find_all('table')  # Fins all tables in the html document
# tr = x[2].find_all('tr')    # Gets table with average similarity scores. Uses x[3] for max similarity scores
#
# # Stores all similarity scores in a dictionary.
# sim_score = {}
# for td in tr:
#     td = td.find_all('td')
#     file_1 = curr_directory + td[0].string
#     file_2 = curr_directory + td[2].a.string
#     score = td[2].font.string[1:-2]
#     key = (file_1, file_2) if file_1 < file_2 else (file_2, file_1)  # Uses the same order previously created
#     sim_score[key] = float(score) / 100     # converts percentage  score to a decimal score inbetween 0 and 1
#
#
# # Opens up the correct judgements for the training set
# f = open(constants.SOCO_JUDGEMENTS, "r")
# pairings = []
# for line in f:
#     pair = line.split(" ")
#     pair[0] = curr_directory + pair[0]
#     pair[1] = curr_directory + pair[1][:-1]
#     t = (pair[0], pair[1]) if pair[0] < pair[1] else (pair[1], pair[0])
#     pairings.append(t)
#
# for pair, val in sim_score.items():
#     if pair in pairings:
#         val *= 1.7
#         val = 1.0 if val > 1.0 else val
#     else:
#         val *= 0.5
#     try:
#         final_df.loc[[pair], ["similarity"]] = val
#     except KeyError as ke:
#         continue
#
#
# successful = []
# errors = []
# # The following loop checks if any of the files are known to be copied, if so it sets their similarity score to 1
# # for pair in pairings:
# #     try:
# #         final_df.loc[[pair], ["similarity"]] = final_df.loc[[pair], ["similarity"]] * 1.5
# #         successful.append(pair)
# #     except KeyError as ke:
# #         errors.append(pair)
# #         continue
#
#
# # train, test = train_test_split(final_df)
# # rf_classifier = RandomForestClassifier(n_estimators=100)
# # k_classifier = KNeighborsClassifier()
#
# # rf_classifier.fit(train.drop(['similarity'], axis=1), train['similarity'].values.ravel())
#
# # print to file
# # final_df.to_csv("dataframes/soco_train__.csv", index=True)
#
#

log.close()
end = time.time()  # stop recording time
print("Execution time: " + str(end - start) + " seconds")
