from buildTree import BPlusTree, Node, Leaf

class removeTree(BPlusTree):
    def __init__(self, maximum=2):
        super(BPlusTree, self).__init__()
        self.root = Leaf()
        self.maximum: int = maximum if maximum > 2 else 2
        self.minimum: int = self.maximum // 2
        self.depth = 0

        self.file_path = "../data/"
        self.table_path = self.file_path + "schemas.txt"
        self.TabeNames: str
        self.attribute = []
        self.typeOfAtt = []
        self.pagePool = []
        self.keyAttr: str

    def delete(self, key, node: Node = None):
        if node is None:
            node = self.find(key)
        del node[key]

        if len(node.keys) < self.minimum:
            if node == self.root:
                if len(self.root.keys) == 0 and len(self.root.values) > 0:
                    self.root = self.root.values[0]
                    self.root.parent = None
                    self.depth -= 1
                return

            elif not node.borrow_key(self.minimum):
                node.fusion()
                self.delete(key, node.parent)

    def deleteAll(self):
        self.removePage()     # remove all pages form index file
        del self.root         # delete the root node of the tree
        self.root = Node()
        self.delDirectory(self.TabeNames, self.keyAttr)    # remove the tree information from directory.txt

if __name__ == '__main__' :
    removeTree = removeTree()
    removeTree.addSpecValueFromFile("Suppliers", "sid")
    removeTree.displayTree()
    #removeTree.displayTree()
    removeTree.deleteAll()
    removeTree.displayTree()