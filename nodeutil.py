from javalang.ast import Node


#   tests for 2 nodes with equal types
def typeEquals(node1, node2):
    if type(node1) is not type(node2):
        return False
    return True


def convert_to_list(tree):
    treelist = []
    for path, node in tree:
        treelist.append(NodeContainer(node))
    return treelist


def hash_token_list(token_list):
    total = 0
    for token in token_list:
        total += hash(token.type)
    return total


def nc_equals(list_1: list, list_2: list) -> bool:
    for val_1, val_2 in zip(list_1, list_2):
        if val_1.type != val_2.type:
            return False
        else:
            continue
    return True

class NodeContainer(object):
    """A generic container to hold a node from the Abstract syntax tree.
        Nodes can have the attributes and methods listed:

    Attributes:
        type: A string representing the node's type.
        position: An int representing the position of the node in the source code.

    Methods:
        equals(NodeContainer): Method to check whether the node containers are equal
    """

    def __init__(self, node):
        self.marked = False
        if isinstance(node, Node):
            self.type = type(node).__name__
            self.position = getattr(node, "position")
            self.line = None
            self.column = None
            if self.position is not None:
                self.line = self.position[0]
                self.column = self.position[1]
            self.node = node
        else:
            self.type = None
            self.position = None
            self.node = None
            print("Error node hasnt been defined: " + str(node))

    # method to check for equality when the "==" operators are used on the NodeContainer class
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, NodeContainer):
            if self.type == other.type:
                return True
        return False

    #   defines what should be outputted when printing thre node
    def __repr__(self):
        string = "(" + str(self.type) + ", Line: " + str(self.line) + " col: " + str(self.column) + ")"
        return string

    def hash(self):
        return hash(self.type)
