import javalang
import os
import shutil
import re

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
treelist = []
treelist2 = []
strin = "^[a-zA-Z0-9]*(_[a-zA-Z0-9]*)+"
try:
    tree = javalang.parse.parse(code)
    tree2 = javalang.parse.parse(code2)
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
        print(str(x) + "\n")
    print("printing tree 2:")
    for x in treelist2:
        print(str(x) + "\n")

    count =0
    start = False
    maximalMatches = []
    list = []
    for node in treelist:
        for node2 in treelist2:
            if node == node2:
                start = True
                count + 1;
                maximalMatches.append(node2)
            else:
                if start == True:
                    treelist = [x for x in treelist if x not in maximalMatches]
                    treelist2 = [x for x in treelist2 if x not in maximalMatches]
                    count = 0
                    start = False
                    list.append(maximalMatches)
                    maximalMatches = []
    for x in list:
        print(str(x) + "\n")

except javalang.parser.JavaSyntaxError as inst:
    print(inst)
