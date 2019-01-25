import javalang
import os
import shutil

dir = os.listdir("jfiles")

tokendir = os.listdir("tokenFiles")


code = '''public class HelloWorld {

    public static void main(String[] args) {
        // Prints "Hello, World" to the terminal window.
        System.out.println("Hello, World");
    }

}
'''
# try using the os module to open a file

# for filename in tokendir:
#     if str(filename) not in dir:
#         print(filename)
for filename in dir:
    address = "jfiles/" + str(filename)
    file = open(address, "r")
    try:
        tree = javalang.parse.parse("".join(file.readlines()))
    except javalang.parser.JavaSyntaxError as inst:
        print(str(filename) + " couldnt compile")
        print(inst)

    tokenaddress = "tokenFiles/"+str(filename) + ".txt"
    tokenfile = open(tokenaddress, "w")

    # tokenfile.write(tree.types)
    for path,node in tree:
        # tokenfile.write(str(path) + "\n")
        tokenfile.write(str(type(node))[22:-2] + " ")
        if "name" in node.attrs:
            tokenfile.write("name= " + str(node.name) + " ")
        if "value" in node.attrs:
            tokenfile.write("value= " + str(node.value) + " ")
        tokenfile.write("\n")
    # tokenfile.write(str(node.attrs) + " type = " + "\n\n")

# print file.readlines()
