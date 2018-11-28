import javalang
filename = "jfiles/forloop.java"
file = open(filename, "r")
code = '''public class HelloWorld {

    public static void main(String[] args) {
        // Prints "Hello, World" to the terminal window.
        System.out.println("Hello, World");
    }

}
'''
try:
    tree = javalang.parse.parse("".join(file.readlines()))
    tokenfile = open("tokenFiles/testfile.txt", "w")

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
except javalang.parser.JavaSyntaxError as inst:
    print("The file you entered was not a correct java file")
# print file.readlines()
