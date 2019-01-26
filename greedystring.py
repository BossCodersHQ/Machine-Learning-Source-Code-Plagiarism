import javalang
import os
import shutil
import re
import sys #used for system exceptions


code = '''public class HelloWorld {

    public static void main(String[] args) {
        // Prints "Hello, World" to the terminal window.
        Integer blow;
        int int_32_temp = 12;
        bool boy_bye = true;
        String out =  "Hello World";
        System.out.println(out);
    }

}
'''

code2 = '''

//class to print out the helloworld class
public class HelloWorld {

    public static void main(String[] args) {
        printHello();
    }

    public static void printHello(){
        //prints out helloworld
        System.out.println("Hello, World");
    }

}
'''
minMatchLength = 9
def greedyTiling( treelistA, treelistB):
    tiles = []
    markedTokensA = []
    markedTokensB = []
    while True:
        maxMatch = minMatchLength
        matches = []
        unmarkedTokensA = [x for x in treelistA if x in treelistA and x not in markedTokensA]
        unmarkedTokensB = [x for x in treelistB if x in treelistB and x not in markedTokensB]
        for indexA, tokenA in enumerate(unmarkedTokensA):
            for indexB, tokenB in enumerate(unmarkedTokensB):
                j = 0
                tempList = []
                while unmarkedTokensA[indexA + j] == unmarkedTokensB[indexB + j]:
                    # print("hello")
                    tempList.append(unmarkedTokensA[indexA + j])
                    j = j + 1
                    if (indexA + j) >= len(unmarkedTokensA):
                        # print("breaking")
                        break
                    if (indexB + j) >= len(unmarkedTokensB):
                        # print("breaking2")
                        break
                # print("goodbye")
                if j == maxMatch:
                    # print("max match found")
                    matches.append(tempList)
                elif (j>maxMatch):
                    matches = []
                    matches.append(tempList)
                    maxMatch = j
        for match in matches:
            for i in range(0,len(match)):
                markedTokensA.append(match[i])
                markedTokensB.append(match[i])
            tiles.append(match)
        if maxMatch <= minMatchLength:
            break
    return tiles

treelist = []
treelist2 = []
strin = "^[a-zA-Z0-9]*(_[a-zA-Z0-9]*)+"

try:
    file1 = open("jfiles/AirlineProblem.java", "r")
    file2 = open("jfiles/ArrayExamples.java", "r")
except FileNotFoundError:
    print("File was not found")
except:
    print (sys.exc_info()[0])
try:
    tree = javalang.parse.parse("".join(file1.readlines()))
    tree2 = javalang.parse.parse("".join(file2.readlines()))
    for path, node in tree:
        #   checking for one attribute
        # if (type(node) == javalang.tree.LocalVariableDeclaration):
        #     list = [method_name for method_name in dir(node) if callable(getattr(node, method_name))]
        #     # print(node)
        #     print(getattr(getattr(node,'type'),'name'))
        #     var = str(getattr(getattr(node,'declarators')[0],'name'))
        #     x = re.search(strin,var)
        #     print(x)
        #     print(getattr(getattr(node,'declarators')[0],'name'))
        treelist.append(str(type(node)))
    for path,node in tree2:
        treelist2.append(str(type(node)))

    print("printing tree 1:")
    for x in treelist:
        print(str(x))
    print("printing tree 2:")
    for x in treelist2:
        print(str(x))
    print()

    list = greedyTiling(treelist,treelist2)
    for x in list:
        print()
        print("LIST")
        print()
        for y in x:
            print(y)

    # for x in list:
    #     print(str(x) + "\n")

except javalang.parser.JavaSyntaxError as inst:
    print(inst)
