import javalang
import os
import shutil
import re
import sys      # used for system exceptions
import inspect  # used yo check objects for all methods
import nodeutil # contains util methods
import constants


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


#   returns a score given 2 files
def greedy_tiling(tree_a, tree_b):

    treelist_a = nodeutil.convertToList(tree_a)
    treelist_b = nodeutil.convertToList(tree_b)
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
                j = 0
                matchList = []
                while unmarked_tokens_a[indexA + j] == unmarked_tokens_b[indexB + j]:
                    # print("hello")
                    tuple = (unmarked_tokens_a[indexA + j],unmarked_tokens_b[indexB + j])

                    # checking if the tokens line numbers have already been recorded. If they haven't then they are
                    # recorded
                    if (tuple[0].line,tuple[1].line) not in current_line_num:
                        current_line_num.append((tuple[0].line,tuple[1].line))

                    matchList.append(tuple)
                    j += 1

                    #   if the next iteration would cause a loop out of bounds exception
                    if (indexA + j) >= len(unmarked_tokens_a) or (indexB + j) >= len(unmarked_tokens_b):
                        break

                if j == max_match and len(current_line_num)>minNumLineMatches:
                    matches.append(matchList)
                elif (j>max_match) and len(current_line_num)>minNumLineMatches:
                    matches = []
                    matches.append(matchList)
                    max_match = j
        for match in matches:
            for i in range(0,len(match)):
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

# treelist = []
# treelist2 = []
# strin = "^[a-zA-Z0-9]*(_[a-zA-Z0-9]*)+"
#
# try:
#     add1 = constants.SOCO_TRAIN + "003.java"
#     add2 = constants.SOCO_TRAIN + "004.java"
#     file1 = open(add1, "r")
#     file2 = open(add2, "r")
# except FileNotFoundError:
#     print("File was not found")
# except:
#     print (sys.exc_info()[0])
# try:
#     tree = javalang.parse.parse("".join(file1.readlines()))
#     tree2 = javalang.parse.parse("".join(file2.readlines()))
#
#     # tree = javalang.parse.parse(code)
#     # tree2 = javalang.parse.parse(code2)
#
#     for path, node in tree:
#         #   checking for one attribute
#         # if (type(node) == javalang.tree.LocalVariableDeclaration):
#         #     list = [method_name for method_name in dir(node) if callable(getattr(node, method_name))]
#         #     # print(node)
#         #     print(getattr(getattr(node,'type'),'name'))
#         #     var = str(getattr(getattr(node,'declarators')[0],'name'))
#         #     x = re.search(strin,var)
#         #     print(x)
#         #     print(getattr(getattr(node,'declarators')[0],'name'))
#         treelist.append(NodeContainer(node))
#     for path,node in tree2:
#         treelist2.append(NodeContainer(node))
#
#     list = greedyTiling(treelist,treelist2)
#     score = calculateScore(list,treelist,treelist2)
#     # for x in list:
#     #     print()
#     #     print("LIST")
#     #     print()
#     #     for y in x:
#     #         print(str(y[0]) + " |\t"+str(y[1]))
#     print("Similarity Score: "+ str(score))
#     print("Number of Matches: " + str(len(list)))
#
#     # count = 0
#     # for x in treelist:
#     #     print(dir(x))
#     #     print(getattr(x,"position"))
#     #     print()
#     #     count += 1
#     #     if count>2:
#     #         break
#
# except javalang.parser.JavaSyntaxError as inst:
#     print(inst)
