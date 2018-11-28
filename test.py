import javalang
code = '''public class HelloWorld {

    public static void main(String[] args) {
        // Prints "Hello, World" to the terminal window.
        System.out.println("Hello, World");
    }

}
'''
tree = javalang.parse.parse(code)
print tree.types
