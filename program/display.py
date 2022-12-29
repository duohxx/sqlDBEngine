from buildTree import BPlusTree, Node, Leaf
from relAlg import table, DataBaseFactory, relationalAlgebraOperations, BpTreeRelAlg

class displayTree(BPlusTree):
    def __init__(self, maximum = 2):
        super(BPlusTree, self).__init__()
        self.root = Leaf()
        self.maximum: int = maximum if maximum > 2 else 2
        self.minimum: int = self.maximum // 2
        self.depth = 0

        self.file_path = "../data/"
        self.table_path = self.file_path + "schemas.txt"
        self.TabeNames = []
        self.attribute = []
        self.typeOfAtt = []
        self.pagePool = []
        self.ValuePair = {}

    def displayTree(self, node=None, file=None, _prefix="", _last=True, f=None):
        """Prints the keys at each level."""
        if node is None:
            node = self.root
        if type(node) is Node:
            if node.parent is None:
                displayCont = []
                j = 0  # the index of node.keys.
                for child in node.values:
                    if child.keys[-1] >= node.keys[j]:
                        displayCont += [node.keys[j]]
                        j += 1
                    displayCont += [child.address]
                print(_prefix, "`- " if _last else "|- ", "<", node.address, ">",
                      "<Node>: <Nil>", [displayCont], sep="", file=file)
            else:
                displayCont = []
                j = 0  # the index of node.keys.
                for child in node.values:
                    # displayCont += [child.address]
                    if child.keys[-1] >= node.keys[j]:
                        displayCont += [node.keys[j]]
                        j += 1
                    displayCont += [child.address]
                print(_prefix, "`- " if _last else "|- ", "<", node.address, ">",
                      "<Node>: ", " <", node.parent.address, ">", [displayCont],
                      sep="", file=file)
        else:
            displayCont = []
            for i, data in enumerate(node.keys):
                displayCont += [data, [node.values[i]]]
            if node.prev is None:
                print(_prefix, "`- " if _last else "|- ", "<", node.address, ">", "<Leaf>: ",
                      " <Nil>", " <", node.next.address, "> ", displayCont, sep="", file=file)
            elif node.next is None:
                print(_prefix, "`- " if _last else "|- ", "<", node.address, ">", "<Leaf>: ",
                      " <", node.prev.address, "> ", "<Nil> ", displayCont, sep="", file=file)
            else:
                print(_prefix, "`- " if _last else "|- ", "<", node.address, ">", "<Leaf>: ",
                      " <", node.prev.address, ">", " <", node.next.address, "> ", displayCont, sep="", file=file)
        _prefix += "   " if _last else "|  "

        if type(node) is Node:
            # Recursively print the key of child nodes (if these exist).
            for i, child in enumerate(node.values):
                _last = (i == len(node.values) - 1)
                self.displayTree(child, file, _prefix, _last)

class displayTable(table):
    def __init__(self):
        super(table, self).__init__()

    def printTable(self):
        print()
        print(self.attribute)
        for data in self.valueTuple:
            print(data)


if __name__ == '__main__':

    bplustree = displayTree()
    bplustree.addSpecValueFromFile("Supply", "pid")
    bplustree.displayTree()

    dataBase = DataBaseFactory()
    tableName = dataBase.getTableName()  # get all names of tables of this database
    operand = relationalAlgebraOperations()

    Suppliers = dataBase.createTable(tableName[0])  # Suppliers
    Products = dataBase.createTable(tableName[1])  # Products
    Catalogs = dataBase.createTable(tableName[2])  # Catalogs
    Products.printTable()




