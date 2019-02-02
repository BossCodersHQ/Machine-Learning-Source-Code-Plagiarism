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
def greedyTiling( treeA, treeB ):

    treelistA = nodeutil.convertToList(treeA)
    treelistB = nodeutil.convertToList(treeB)
    tiles = []
    previousLine = 0

    currentLineMatches = 0
    while True:
        maxMatch = minMatchLength
        matches = []
        unmarkedTokensA = [x for x in treelistA if not x.marked]
        unmarkedTokensB = [x for x in treelistB if not x.marked]
        for indexA, tokenA in enumerate(unmarkedTokensA):
            for indexB, tokenB in enumerate(unmarkedTokensB):
                currentLineNum = []
                j = 0
                matchList = []
                while unmarkedTokensA[indexA + j] == unmarkedTokensB[indexB + j]:
                    # print("hello")
                    tuple = (unmarkedTokensA[indexA + j],unmarkedTokensB[indexB + j])

                    #   checking if the tokens line numbers have already been recorded. If they havent then they are recorded
                    if (tuple[0].line,tuple[1].line) not in currentLineNum:
                        currentLineNum.append((tuple[0].line,tuple[1].line))

                    matchList.append(tuple)
                    j += 1

                    #   if the next iteration would cause a loop out of bounds exception
                    if (indexA + j) >= len(unmarkedTokensA) or (indexB + j) >= len(unmarkedTokensB):
                        break

                if j == maxMatch and len(currentLineNum)>minNumLineMatches:
                    matches.append(matchList)
                elif (j>maxMatch) and len(currentLineNum)>minNumLineMatches:
                    matches = []
                    matches.append(matchList)
                    maxMatch = j
        for match in matches:
            for i in range(0,len(match)):
                match[i][0].marked = True
                match[i][1].marked = True
            tiles.append(match)

        if maxMatch <= minMatchLength:
            break

    lengthA = len(treelistA)
    lengthB = len(treelistB)
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
