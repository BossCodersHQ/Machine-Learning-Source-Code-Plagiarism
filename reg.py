import re
import lizard
import os
import sys
import re
import sys
import pandas as pd
import numpy as np

str = "minVal = a < b ? a : b;"
x = re.findall(r'(^[_a-zA-Z0-9]*( *)=(.*?)[\?](.*?):( *)(.*))', str)
print(lizard.__file__)
path = os.path.dirname(os.path.realpath(__file__)) + "/jfiles2/"
data = lizard.main(["lizard.py", "-l", "java", "jfiles/"])
df = pd.DataFrame(data,
                  columns=["Filename", "total.nloc", "avg.nloc", "avg.ccn", "avg.token", "function_cnt"])
print(df)
# argv = ["lizard.py", "-l", "java", path]
# print(lizard.main(["lizard.py", "-l", "java", "--csv", path]))
# print(lizard.print_extension_results())
# for x in lizard.analyze(path):
#     # average_nloc = str(x.average_nloc)
#     print(x)
# # print(lizard.analyze("jfiles/"))
# x = os.popen("lizard -l java jfiles2/").read()
"""Command-line entrance to Lizard.

Args:
    argv: Arguments vector; if None, sys.argv by default.
"""
# options = lizard.parse_args(argv)
# printer = lizard.print_result
# schema = lizard.OutputScheme(options.extensions)
# if schema.any_silent():
#     printer = lizard.silent_printer
# if options.input_file:
#     options.paths = auto_read(options.input_file).splitlines()
# result = lizard.analyze(
#     options.paths,
#     options.exclude,
#     options.working_threads,
#     options.extensions,
#     options.languages)
# warning_count = printer(result, options, schema, lizard.AllResult)
# # lizard.print_extension_results(options.extensions)
# list(result)
# print(warning_count)
# if 0 <= options.number < warning_count:
#     sys.exit(1)
