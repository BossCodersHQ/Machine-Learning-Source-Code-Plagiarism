import javalang
import os
import shutil
import re
import sys      # used for system exceptions
import inspect  # used yo check objects for all methods
import nodeutil # contains util methods
import constants
import time  # used to record how long methods take to run
import itertools
from collections import defaultdict

minMatchLength = 9
minNumLineMatches = 4  # The number of different lines that a match has to be found on

# # Calculates similarity score for 2 ast's based on the matches
# def calculateScore(matchlist, treelistA, treelistB):
#     lengthA = len(treelistA)
#     lengthB = len(treelistB)
#     count = 0
#     for match in matchlist:
#         for token in match:
#             count += 1
#     score = (2 * count) / (lengthA + lengthB)
#     return score


def create_hashtable(token_list):
    hmap = defaultdict(list)
    for index in range(len(token_list) - minMatchLength):
        temp = token_list[index:index+minMatchLength]
        key = nodeutil.hash_token_list(temp)
        hmap[key].append((temp, index))
    return hmap


def imp_greedy_tiling(filename_1, filename_2, hash_map, tree_map):
    # for x in hash_map[filename_1].items():
    #     print(x)
    map_1 = hash_map[filename_1]
    tokens_1 = tree_map[filename_1]
    map_2 = hash_map[filename_2]
    tokens_2 = tree_map[filename_2]

    if len(tokens_1) > len(tokens_2):
        map_1, map_2 = map_2, map_1     # Makes sure map_1 is the smallest map
        tokens_1, tokens_2 = tokens_2, tokens_1

    tiles = []

    while True:
        # print("Starting Run Through all over again")
        max_match = minMatchLength
        matches = []
        # c = 0
        for key in map_1:
            # c+=1
            # print("On key " +str(c) + " out of " + str(len(map_1)))
            if len(map_2[key]) == 0:
                continue
            for map_1_val, index_1 in map_1[key]:
                if tokens_1[index_1].marked:
                    # print("marked token found")
                    continue

                #  Else
                for map_2_val, index_2 in map_2[key]:
                    if tokens_2[index_2].marked:
                        # print("marked token found")
                        continue

                    # Using nc_equals method to compare 2 lists containing NodeContainers
                    # if nodeutil.nc_equals(map_1_val, map_2_val):/
                    #
                    #     print("match found at  i1 : " + str(index_1) + " i2: " + str(index_2))
                    #     # print(tokens_1[index_1])
                    #     # print(tokens_2[index_2])
                    end_flag = False
                    extend_flag = False                 # When true indicates looking for a larger max match
                    # print("clearing match_list")
                    match_list = []  # Stores a list of maximal matches for each iteration
                    pointer_1 = index_1 + max_match - 1
                    pointer_2 = index_2 + max_match - 1

                    # Token by token comparison
                    # Once verified attempts to extend match
                    while not end_flag:
                        # print(str(index_1) + " " + str(index_2))
                        if pointer_1 >= len(tokens_1) - 1 or pointer_2 >= len(tokens_2) - 1:
                            end_flag = True
                            # print("changing " + str(pointer_1) + " " + str(pointer_2))
                        if not end_flag and tokens_1[pointer_1].marked and tokens_2[pointer_2].marked:
                            end_flag = True

                        if not end_flag and tokens_1[pointer_1] == tokens_2[pointer_2]:
                            if extend_flag:
                                pointer_1 += 1
                                pointer_2 += 1
                                # Checks to see if its the end of the file
                                # if pointer_1 == len(tokens_1)-1 or pointer_2 == len(tokens_2)-1:
                                #     end_flag = True
                            else:
                                pointer_1 -= 1
                                pointer_2 -= 1

                                # Only when its confirmed that the match is the same can we then start to
                                # extend the match
                                if pointer_1 < index_1 and pointer_2 < index_2:
                                    extend_flag = True
                                    pointer_1 = index_1 + max_match + 1
                                    pointer_2 = index_2 + max_match + 1

                                    if pointer_1 >= len(tokens_1)-1 or pointer_2 >= len(tokens_2)-1:
                                        end_flag = True     # pointer is at the last index in list at this point
                                    # print(str(pointer_1) + " " + str(len(tokens_1)) + " " + str(pointer_2) )
                                    # Match is longer than the previous max match
                                    if not end_flag and tokens_1[pointer_1] == tokens_2[pointer_2]:
                                        if tokens_1[pointer_1].marked or tokens_2[pointer_2].marked:
                                            # match = (index_1, pointer_1-1, index_2, pointer_2-1)
                                            # match_list.append(match)
                                            end_flag = True
                                        else:
                                            # If there is definatley a match longer than the current maximal match then
                                            # the match_list array is cleared to accomodate a new set of longer matches
                                            # print("clearing match_list\n\n\n")
                                            match_list = []
                                    # Match is the same length as the current max match
                                    else:
                                        # if not tokens_1[pointer_1].marked and not tokens_2[pointer_2].marked:
                                        #     match = (index_1, pointer_1-1, index_2, pointer_2-1)
                                        #     match_list.append(match)
                                        end_flag = True
                        else:
                            end_flag = True

                            if extend_flag:
                                # print("Ending")
                                # print("adding to match")
                                # print(tokens_1[index_1:pointer_1-1])
                                # print(tokens_2[index_2:pointer_2-1])
                                # match = ( tokens_1[index_1:pointer_1-1], tokens_2[index_2:pointer_2-1])
                                match = (index_1, pointer_1-1, index_2, pointer_2-1)
                                match_list.append(match)
                                matches = match_list
                                max_match = pointer_1-1 - index_1 + 1

        # print(max_match)
        # print(matches)
        for match in matches:
            start_1, end_1, start_2, end_2 = match
            match_length = end_1 - start_1 + 1
            # print("marking token")
            for i in range(match_length):
                tokens_1[start_1 + i].marked = True
                tokens_2[start_2 + i].marked = True
            tiles.append(match)

        if max_match == minMatchLength:
            break

    len_1 = len(tokens_1)
    len_2 = len(tokens_2)
    count = 0

    for match in tiles:
        count += match[1] - match[0]
    score = (2 * count) / (len_1 + len_2)
    # print(tiles)
    return score


#   returns a score given 2 files
def greedy_tiling(tree_a, tree_b):

    treelist_a = nodeutil.convert_to_list(tree_a)
    treelist_b = nodeutil.convert_to_list(tree_b)
    tiles = []
    previousLine = 0

    currentLineMatches = 0
    while True:
        max_match = minMatchLength
        matches = []
        unmarked_tokens_a = [x for x in treelist_a if not x.marked]
        unmarked_tokens_b = [x for x in treelist_b if not x.marked]
        for indexA, tokenA in enumerate(unmarked_tokens_a):
            for indexB, tokenB in enumerate(unmarked_tokens_b):
                current_line_num = []
                j = 0   # used as a counter to extend matches
                match_list = []
                while unmarked_tokens_a[indexA + j] == unmarked_tokens_b[indexB + j]:
                    # print("hello")
                    tuple = (unmarked_tokens_a[indexA + j], unmarked_tokens_b[indexB + j])

                    # checking if the tokens line numbers have already been recorded. If they haven't then they are
                    # recorded
                    if (tuple[0].line, tuple[1].line) not in current_line_num:
                        current_line_num.append((tuple[0].line, tuple[1].line))

                    match_list.append(tuple)
                    j += 1

                    #   if the next iteration would cause a loop out of bounds exception
                    if (indexA + j) >= len(unmarked_tokens_a) or (indexB + j) >= len(unmarked_tokens_b):
                        break

                if j == max_match and len(current_line_num)>minNumLineMatches:
                    matches.append(match_list)
                elif (j > max_match) and len(current_line_num)>minNumLineMatches:
                    matches = []
                    matches.append(match_list)
                    max_match = j
        for match in matches:
            for i in range(0, len(match)):
                match[i][0].marked = True
                match[i][1].marked = True
            tiles.append(match)

        if max_match <= minMatchLength:
            break

    lengthA = len(treelist_a)
    lengthB = len(treelist_b)
    count = 0

    for match in tiles:
        for token in match:
            count += 1
    score = (2 * count) / (lengthA + lengthB)

    return score


if __name__ == '__main__':
    # def main(curr_directory="jfiles2/"):
    start = time.time()  # #start recording how long program takes

    curr_directory = "jfiles/"
    # currDirectory = constants.SOCO_TRAIN

    javadir = os.listdir(curr_directory)  # directory where all java files will be stored

    files = []
    error_msgs = {}
    faulty_files = []
    tree_map = {}  # Stores all trees created from the all the files in a separate dictionary
    hash_map = {}

    for filename in javadir:
        address = curr_directory + "/" + str(filename)
        try:
            file = open(address, "r")
            # files[str(filename)] = file
            files.append(str(filename))

            text = "".join(file.readlines())

            tree = javalang.parse.parse(text)
            tokens = nodeutil.convert_to_list(tree)     # Creates a list of tokens from the tree

            tree_map[filename] = tokens
            hash_map[filename] = create_hashtable(tokens)

        except FileNotFoundError:
            print("File " + str(filename) + " was not found")
        except javalang.parser.JavaSyntaxError as inst:
            print(str(filename) + " couldn't compile")
            faulty_files.append(filename)
        # except Exception as inst:
        #     error_msgs[filename] = str(inst)

    #  2 loops used to go through all pairings of files and perform a structure based method on all of then_statement
    #  The scores are stored in the score map
    score_map = {}

    for filename_1, filename_2 in itertools.combinations(tree_map, 2):

        # the next section ensures that the key for 2 trees in the score map will be the same no matter
        # which tree is tree_1 / tree_2
        hash1 = hash(filename_1)
        hash2 = hash(filename_2)
        if hash1 >= hash2:
            key = (filename_1, filename_2)
        else:
            key = (filename_2, filename_1)

        # tree_1 = tree_map[filename_1]
        # tree_2 = tree_map[filename_2]
        #
        # score = greedy_tiling(tree_1, tree_2)
        score = imp_greedy_tiling(filename_1, filename_2, hash_map, tree_map)

        print("Comparing " + filename_1 + "-" + filename_2 + ": " + str(score))
        score_map[key] = score

    # f = open("result.txt", "w")
    # for key, score in score_map.items():
    #     if score > constants.SIMILARITY_THRESHOLD:
    #         f.write("Similarity Score for " + str(key) + " is : " + str(score))

    end = time.time()  # stop recording time
    print("Execution time: " + str(end - start) + " seconds")



