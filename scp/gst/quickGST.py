import os
import operator
import math
import time  # used to record how long methods take to
from collections import defaultdict
import itertools

import javalang

import copy
import nodeutil  # contains util methods
import constants
import util
import sys
from results import Result





def quick_gst(filename_1:str, filename_2:str, hash_map:dict, tree_map:dict) -> int:
    # Makes sure map_1 is the smallest map as this is the map which has to be traveresed fully.
    # Map_2 only has to be accessed through a hash map (access time of O(1))
    if len(tree_map[filename_1]) > len(tree_map[filename_2]):
        filename_1, filename_2 = filename_2, filename_1
        map_1 = hash_map[filename_2]
        map_2 = hash_map[filename_1]
        tokens_1 = tree_map[filename_2]
        tokens_2 = tree_map[filename_1]
    else:
        map_1 = hash_map[filename_1]
        tokens_1 = tree_map[filename_1]
        map_2 = hash_map[filename_2]
        tokens_2 = tree_map[filename_2]

    tiles = []  # Will store all matches by the end of the following while loop

    # Each while loops find a group of matches with a token length of n
    # Every iteration the value of n becomes smaller by at the least 1
    while True:
        # print("Starting Run Through all over again")
        max_match = constants.MIN_MATCH_LENGTH
        matches = []
        # c = 0
        for key in map_1:
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

                    end_flag = False
                    extend_flag = (
                        False  # When true indicates looking for a larger max match
                    )
                    match_list = (
                        []
                    )  # Stores a list of maximal matches for each iteration
                    pointer_1 = index_1 + max_match - 1
                    pointer_2 = index_2 + max_match - 1

                    # Token by token comparison
                    # Once verified attempts to extend match
                    while not end_flag:
                        # print(str(index_1) + " " + str(index_2))
                        if pointer_1 >= len(tokens_1) or pointer_2 >= len(tokens_2):
                            end_flag = True
                        if (
                            not end_flag
                            and tokens_1[pointer_1].marked
                            and tokens_2[pointer_2].marked
                        ):
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

                                    if (
                                        pointer_1 >= len(tokens_1) - 1
                                        or pointer_2 >= len(tokens_2) - 1
                                    ):
                                        end_flag = True  # pointer is at the last index in list at this point
                                    # Match is longer than the previous max match
                                    if (
                                        not end_flag
                                        and tokens_1[pointer_1] == tokens_2[pointer_2]
                                    ):
                                        if (
                                            tokens_1[pointer_1].marked
                                            or tokens_2[pointer_2].marked
                                        ):
                                            end_flag = True
                                        else:
                                            # If there is definatley a match longer than the current maximal match then
                                            # the match_list array is cleared to accomodate a new set of longer matches
                                            match_list = []
                                    # Match is the same length as the current max match
                                    else:
                                        end_flag = True
                        else:
                            end_flag = True

                            if extend_flag:
                                match = (index_1, pointer_1 - 1, index_2, pointer_2 - 1)
                                match_list.append(match)
                                matches = match_list
                                max_match = pointer_1 - 1 - index_1 + 1

        for match in matches:
            start_1, end_1, start_2, end_2 = match
            match_length = end_1 - start_1 + 1
            # print("marking token")
            line_flag = True

            lines_1 = (
                util.get_node_line(tokens_1, start_1, end_1),
                util.get_node_line(tokens_1, end_1, start_1),
            )
            lines_2 = (
                util.get_node_line(tokens_2, start_2, end_2),
                util.get_node_line(tokens_2, end_2, start_2),
            )
            for i in range(match_length):
                tokens_1[start_1 + i].marked = True
                tokens_2[start_2 + i].marked = True

            if filename_1 <= filename_2:
                tiles.append((match, lines_1, lines_2))
            else:
                tiles.append((match, lines_2, lines_1))

        if max_match == constants.MIN_MATCH_LENGTH:
            break

    len_1 = len(tokens_1)
    len_2 = len(tokens_2)
    count = 0

    for match in tiles:
        count += match[0][1] - match[0][0] + 1
    score = (2 * count) / (len_1 + len_2)

    nodeutil.unmark_tokens(tokens_1)
    nodeutil.unmark_tokens(tokens_2)

    return score, tiles


def main(source_dir, output_dir, outbox):

    start = time.time()  # #start recording how long program takes
    try:
        # Reading all files in the source directory
        javadir = os.listdir(
            source_dir
        )  # directory where all java files will be stored
    except FileNotFoundError as inst:
        util.print_tk(outbox, "Incorrect Directory Entered\n")
        # exit()
        return 0

    util.print_tk(outbox, "Reading Files..\n")

    files = []
    file_map = {}
    error_msgs = {}
    faulty_files = []
    tree_map = (
        {}
    )  # Stores all trees created from the all the files in a separate dictionary
    hash_map = {}
    util.print_tk(outbox, "Setting up hash table of files...\n")

    for filename in javadir:
        if filename[-5:] != ".java":  # Ensures that the current file is a java file
            continue

        if source_dir[-1] != "/":
            address = source_dir + "/" + str(filename)
        else:
            address = source_dir + str(filename)

        try:
            file = open(address, "r")

            text = "".join(file.readlines())
            file_map[filename] = text

            tree = javalang.parse.parse(text)
            tokens = nodeutil.convert_to_list(
                tree
            )  # Creates a list of tokens from the tree

            tree_map[filename] = tokens
            hash_map[filename] = create_hashtable(tokens)

            files.append(str(filename))

        except FileNotFoundError:
            util.print_tk(outbox, "File " + str(filename) + " was not found\n")
        except javalang.parser.JavaSyntaxError as inst:
            util.print_tk(outbox, str(filename) + " couldn't compile\n")
            faulty_files.append(filename)
        except javalang.tokenizer.LexerError as inst:
            continue
        except UnicodeDecodeError as inst:
            continue
        except Exception as inst:
            print(filename, type(inst), inst)
            continue

    #  2 loops used to go through all pairings of files and perform a structure based method on all of then_statement
    #  The scores are stored in the score map
    score_map = {}  # Map used to store the scores of each pair of files
    distro_map = defaultdict(int)  # Map used to store the distribution of scores
    tile_map = {}

    for filename_1, filename_2 in itertools.combinations(tree_map, 2):
        # Ensure the key for 2 trees in the score map will be the same no matter

        if util.STOPFLAG:
            break  # Used to exit function

        if filename_1 <= filename_2:
            key = (filename_1, filename_2)
        else:
            key = (filename_2, filename_1)

        score, tiles = quick_gst(filename_1, filename_2, hash_map, tree_map)
        score = score * 100

        str_score = "%.2f" % score  # rounds score too 2 dp to display

        util.print_tk(
            outbox,
            "Compared " + filename_1 + "-" + filename_2 + ": " + str_score + "%\n",
        )
        score_map[key] = score

        if score > constants.SIMILARITY_THRESHOLD:
            tile_map[key] = tiles

        rounded_score = int(math.ceil(score / 10.0)) * 10
        distro_map[rounded_score] += 1

    if output_dir == None:
        return score_map

    sorted_scores = sorted(score_map.items(), key=operator.itemgetter(1), reverse=True)
    sorted_distro = sorted(distro_map.items(), key=operator.itemgetter(0), reverse=True)

    end = time.time()  # stop recording time
    util.print_tk(outbox, "Execution time: " + str(end - start) + " seconds")
    if util.STOPFLAG:
        util.print_tk(outbox, "Comparisons interrupted\n")
        util.STOPFLAG = False
    else:
        util.print_tk(outbox, "--Finished Comparisons--\n")

    message = """
    These are the results computed using an improved version of the Greedy String Tiling. Each score is presented as a 
    percentage where each percentage represents the average similarity between files. This means that extending one file
    will not affect the score."""

    if output_dir is not None:
        res = Result(
            files,
            message,
            output_dir,
            sorted_scores,
            sorted_distro,
            "quick_gst",
            file_map,
            tile_map,
        )
        res.print_html()

    # h = res.get_hm()



def create_hashtable(token_list):
    hmap = defaultdict(list)
    for index in range(len(token_list) - constants.MIN_MATCH_LENGTH):
        temp = token_list[index : index + constants.MIN_MATCH_LENGTH]
        key = nodeutil.hash_token_list(temp)
        hmap[key].append((temp, index))
    return hmap