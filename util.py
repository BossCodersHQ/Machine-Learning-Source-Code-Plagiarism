# This file defines a number of utility methods used throughout the project
import tkinter as tk
import math
import numpy as np

STOPFLAG = False


def print_tk(outbox, str):
    if outbox is not None:
        outbox.insert(tk.INSERT, str)
        outbox.see(tk.END)
        outbox.update_idletasks()
    # else:
        # print(str)


def get_node_line(list, start, end):
    if start < end:
        length = end - start + 1
        for i in range(length):
            line_number = list[start + i].line
            # print(line_number)
            if line_number is not None:
                return line_number
    else:
        length = start - end + 1
        for i in range(length):
            line_number = list[start - i].line
            # print(line_number)
            if line_number is not None:
                return line_number
    return None


def in_range(num, start, end):
    """ Checks to see if a number is between 2 other numbers"""
    if start >= num >= end:
        return True
    return False


def euclid_dist(vector_1, vector_2):
    """ Calculates the euclidean distance between a list containing two of vectors"""
    temp = 0
    for v1, v2 in zip(vector_1, vector_2):
        if not np.isnan(v1) or not np.isnan(v2):
            temp += (v2 - v1) ** 2
    return math.sqrt(temp)


def cosine_sim(vector_1, vector_2):
    """ Calculates the cosine similarity between 2 vectors stored as a list of numbers"""
    dot_prod = 0
    for v1, v2 in zip(vector_1, vector_2):
        if not np.isnan(v1) or not np.isnan(v2):
            dot_prod += v2 * v1

    ans = dot_prod / (absolute(vector_1) * absolute(vector_2))

    return ans


def absolute(vector):
    """ Calculates the absolute value of a vector stored as a list of numbers"""
    temp = 0
    for v in vector:
        if not np.isnan(v):
            temp += v ** 2
    return math.sqrt(temp)
