import re

str = "minVal = a < b ? a : b;"
x = re.findall("(.+)=(.+)?(.+):(.+)", str)
print(x)