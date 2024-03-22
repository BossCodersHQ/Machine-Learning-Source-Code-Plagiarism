import javalang
import os
import shutil
import re
import sys
import inspect
import nodeutil
import config


MIN_MATCH_LENGTH = 9
MIN_NUM_LINE_MATCHES = 4


def greedyTiling( treeA, treeB ) -> float:
    """
    Greedy tiling algorithm to find the longest common subsequence of two lists of tokens.
    Returns a score based on the number of matches found."""
    treelistA = nodeutil.convertToList(treeA)
    treelistB = nodeutil.convertToList(treeB)
    tiles = []
    while True:
        maxMatch = MIN_MATCH_LENGTH
        matches = []
        unmarkedTokensA = [x for x in treelistA if not x.marked]
        unmarkedTokensB = [x for x in treelistB if not x.marked]
        for indexA, tokenA in enumerate(unmarkedTokensA):
            for indexB, tokenB in enumerate(unmarkedTokensB):
                currentLineNum = []
                j = 0
                matchList = []
                while unmarkedTokensA[indexA + j] == unmarkedTokensB[indexB + j]:
                    tuple = (unmarkedTokensA[indexA + j],unmarkedTokensB[indexB + j])

                    # checking if the tokens line numbers have already been recorded. If they havent then they are recorded
                    if (tuple[0].line,tuple[1].line) not in currentLineNum:
                        currentLineNum.append((tuple[0].line,tuple[1].line))

                    matchList.append(tuple)
                    j += 1

                    # if the next iteration would cause a loop out of bounds exception
                    if (indexA + j) >= len(unmarkedTokensA) or (indexB + j) >= len(unmarkedTokensB):
                        break

                if j == maxMatch and len(currentLineNum)>MIN_NUM_LINE_MATCHES:
                    matches.append(matchList)
                elif (j>maxMatch) and len(currentLineNum)>MIN_NUM_LINE_MATCHES:
                    matches = []
                    matches.append(matchList)
                    maxMatch = j
        for match in matches:
            for i in range(0,len(match)):
                match[i][0].marked = True
                match[i][1].marked = True
            tiles.append(match)

        if maxMatch <= MIN_MATCH_LENGTH:
            break
    
    return calculateScore(tiles, treelistA, treelistB)


def calculateScore(matchlist, treelistA, treelistB):
    """ Calculates similarity score for 2 ast's based on the matches """
    lengthA = len(treelistA)
    lengthB = len(treelistB)
    count = 0
    for match in matchlist:
        for token in match:
            count += 1
    score = (2 * count) / (lengthA + lengthB)
    return score