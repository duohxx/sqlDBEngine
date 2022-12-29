import random  # for demo test
import os
import re
import json
import sys

splits = 0
parent_splits = 0
fusions = 0
parent_fusions = 0
numOfNode = -1
valueIndex = 0


class Node(object):

    def __init__(self, parent=None):
        self.keys: list = []
        self.values: list[Node] = []
        global numOfNode
        numOfNode += 1
        self.address: list = "pg" + str(numOfNode).zfill(3) + ".txt"
        self.parent: Node = parent

    def index(self, key):
        for i, item in enumerate(self.keys):
            if key < item:
                return i

        return len(self.keys)

    def __getitem__(self, item):
        return self.values[self.index(item)]

    def __setitem__(self, key, value):
        i = self.index(key)
        self.keys[i:i] = [key]
        self.values.pop(i)
        self.values[i:i] = value


    def split(self):
        global splits, parent_splits, numOfNode
        splits += 1
        parent_splits += 1
        #numOfNode += 1
        left = Node(self.parent)

        mid = len(self.keys) // 2

        left.keys = self.keys[:mid]
        left.values = self.values[:mid + 1]
        left.address = "pg" + str(numOfNode).zfill(3) + ".txt"
        for child in left.values:
            child.parent = left

        key = self.keys[mid]
        self.keys = self.keys[mid + 1:]
        self.values = self.values[mid + 1:]

        return key, [left, self]

    def __delitem__(self, key):
        i = self.index(key)
        del self.values[i]
        if i < len(self.keys):
            del self.keys[i]
        else:
            del self.keys[i - 1]

    def fusion(self):
        global fusions, parent_fusions
        fusions += 1
        parent_fusions += 1

        index = self.parent.index(self.keys[0])
        # merge this node with the next node
        if index < len(self.parent.keys):
            next_node: Node = self.parent.values[index + 1]
            next_node.keys[0:0] = self.keys + [self.parent.keys[index]]
            for child in self.values:
                child.parent = next_node
            next_node.values[0:0] = self.values

        else:  # If self is the last node, merge with prev
            prev: Node = self.parent.values[-2]
            prev.keys += [self.parent.keys[-1]] + self.keys
            for child in self.values:
                child.parent = prev
            prev.values += self.values

    def borrow_key(self, minimum: int):
        index = self.parent.index(self.keys[0])
        if index < len(self.parent.keys):
            next_node: Node = self.parent.values[index + 1]
            if len(next_node.keys) > minimum:
                self.keys += [self.parent.keys[index]]

                borrow_node = next_node.values.pop(0)
                borrow_node.parent = self
                self.values += [borrow_node]
                self.parent.keys[index] = next_node.keys.pop(0)
                return True
        elif index != 0:
            prev: Node = self.parent.values[index - 1]
            if len(prev.keys) > minimum:
                self.keys[0:0] = [self.parent.keys[index - 1]]

                borrow_node = prev.values.pop()
                borrow_node.parent = self
                self.values[0:0] = [borrow_node]
                self.parent.keys[index - 1] = prev.keys.pop()
                return True

        return False


class Leaf(Node):
    def __init__(self, parent=None, prev_node=None, next_node=None):
        super(Leaf, self).__init__(parent)
        global numOfNode, valueIndex
        numOfNode += 1
        if valueIndex == 1:
            self.address = "pg" + str(numOfNode).zfill(3) + ".txt"
        else:
            self.address = "pg" + str(numOfNode).zfill(3) + ".txt"
        self.next: Leaf = next_node
        if next_node is not None:
            next_node.prev = self
        self.prev: Leaf = prev_node
        if prev_node is not None:
            prev_node.next = self

    def __getitem__(self, item):
        return self.values[self.keys.index(item)]

    def __setitem__(self, key, value):
        global numOfNode
        i = self.index(key)
        #numOfNode += 1
        #self.address = "pg" + str(numOfNode).zfill(3)
        if key not in self.keys:
            self.keys[i:i] = [key]
            self.values[i:i] = [value]
        else:
            self.values[i - 1] = value

    def split(self):
        global splits
        splits += 1
        left = Leaf(self.parent, self.prev, self)
        mid = len(self.keys) // 2

        left.keys = self.keys[:mid]
        left.values = self.values[:mid]

        self.keys: list = self.keys[mid:]
        self.values: list = self.values[mid:]

        # When the leaf node is split, set the parent key to the left-most key of the right child node.
        return self.keys[0], [left, self]

    def __delitem__(self, key):
        i = self.keys.index(key)
        del self.keys[i]
        del self.values[i]
        #del self.address

    def fusion(self):
        global fusions
        fusions += 1

        if self.next is not None and self.next.parent == self.parent:
            self.next.keys[0:0] = self.keys
            self.next.values[0:0] = self.values
        else:
            self.prev.keys += self.keys
            self.prev.values += self.values

        if self.next is not None:
            self.next.prev = self.prev
        if self.prev is not None:
            self.prev.next = self.next

    def borrow_key(self, minimum: int):
        index = self.parent.index(self.keys[0])
        if index < len(self.parent.keys) and len(self.next.keys) > minimum:
            self.keys += [self.next.keys.pop(0)]
            self.values += [self.next.values.pop(0)]
            self.parent.keys[index] = self.next.keys[0]
            return True
        elif index != 0 and len(self.prev.keys) > minimum:
            self.keys[0:0] = [self.prev.keys.pop()]
            self.values[0:0] = [self.prev.values.pop()]
            self.parent.keys[index - 1] = self.keys[0]
            return True

        return False


class BPlusTree(object):
    root: Node

    def __init__(self, maximum=2):
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

    def getAttr(self):
        return self.attribute

    def find(self, key) -> Leaf:
        """ find the leaf

        Returns:
            Leaf: the leaf which should have the key
        """
        node = self.root
        # Traverse tree until leaf node is reached.
        while type(node) is not Leaf:
            node = node[key]

        return node

    def __getitem__(self, item):
        return self.find(item)[item]

    def query(self, key):
        """Returns a value for a given key, and None if the key does not exist."""
        leaf = self.find(key)
        return leaf[key] if key in leaf.keys else None

    def getQueryCont(self, key):
        cont = self.query(key)
        #print(key)
        file = cont[0:-2]
        index = cont[-1]
        dataPath = "../data/" + self.TabeNames + "/" + file
        #print(dataPath)
        with open(dataPath, "r") as f:  # Open file
            data = json.load(f)
            #print(data[int(index)])
            return data[int(index)]

    def __setitem__(self, key, value, address=None, leaf=None):
        """Inserts a key-value pair after traversing to a leaf node. If the leaf node is full, split
              the leaf node into two.
              """
        global numOfNode
        if leaf is None:
            leaf = self.find(key)
        leaf[key] = value

        if len(leaf.keys) > self.maximum:
            self.insert_index(*leaf.split())

    def insert(self, key, value):
        """
        Returns:
            (bool,Leaf): the leaf where the key is inserted. return False if already has same key
        """
        leaf = self.find(key)

        if key in leaf.keys:
            return False, leaf
        else:
            self.__setitem__(key, value, leaf)
            return True, leaf

    def insert_index(self, key, values):
        """For a parent and child node,
                    Insert the values from the child into the values of the parent."""
        global numOfNode
        parent = values[1].parent
        if parent is None:
            values[0].parent = values[1].parent = self.root = Node()
            self.depth += 1
            self.root.keys = [key]
            self.root.values = values
            return

        parent[key] = values
        # If the node is full, split the  node into two.
        if len(parent.keys) > self.maximum:
            self.insert_index(*parent.split())
        # Once a leaf node is split, it consists of a internal node and two leaf nodes.
        # These need to be re-inserted back into the tree.

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

    def getSmallestKey(self, node=None) -> Leaf:
        if node is None:
            node = self.root
        while type(node) is Node:
            # Recursively till get the smallest one.
            node = node.values[0]
        return node

    def displayTree(self, node=None, file=None, _prefix="", _last=True, f = None):
        """Prints the keys at each level."""
        if node is None:
            node = self.root
        if type(node) is Node:
            if node.parent is None:
                displayCont = []
                j = 0    #the index of node.keys.
                for child in node.values:
                    if child.keys[-1] >= node.keys[j]:
                        displayCont += [node.keys[j]]
                        j += 1
                    displayCont += [child.address]
                print(_prefix, "`- " if _last else "|- ", "<",node.address, ">",
                      "<Node>: <Nil>", [displayCont],  sep="", file=file)
            else:
                displayCont = []
                j = 0  # the index of node.keys.
                for child in node.values:
                    # displayCont += [child.address]
                    if child.keys[-1] >= node.keys[j]:
                        displayCont += [node.keys[j]]
                        j += 1
                    displayCont += [child.address]
                print(_prefix,  "`- " if _last else "|- ", "<",node.address, ">",
                      "<Node>: ", " <", node.parent.address,  ">",[displayCont],
                        sep="", file=file)
        else:
            displayCont = []
            for i,data in enumerate(node.keys):
                displayCont += [data, [node.values[i]]]
            if node.prev is None:
                print(_prefix, "`- " if _last else "|- ", "<",node.address, ">", "<Leaf>: ",
                      " <Nil>", " <", node.next.address, "> ", displayCont, sep="",file=file)
            elif node.next is None:
                print(_prefix, "`- " if _last else "|- ", "<",node.address, ">", "<Leaf>: ",
                      " <", node.prev.address, "> ", "<Nil> ",displayCont, sep="", file=file)
            else:
                print(_prefix,  "`- " if _last else "|- ", "<",node.address, ">", "<Leaf>: ",
                      " <", node.prev.address, ">", " <", node.next.address, "> ", displayCont, sep="", file=file)
        _prefix += "   " if _last else "|  "

        if type(node) is Node:
            # Recursively print the key of child nodes (if these exist).
            for i, child in enumerate(node.values):
                _last = (i == len(node.values) - 1)
                self.displayTree(child, file, _prefix, _last)

    def SaveTreeStructure(self, node=None, file=None, _prefix="", _last=True, f = None):
        """Prints the keys at each level."""
        """Prints the keys at each level."""
        if node is None:
            node = self.root
        if type(node) is Node:
            if node.parent is None:
                displayCont = []
                j = 0    #the index of node.keys.
                for child in node.values:
                    if child.keys[-1] >= node.keys[j]:
                        displayCont += [node.keys[j]]
                        j += 1
                    displayCont += [child.address]
                f.write(str(_prefix) + "<" + ', '.join([node.address]) + ">" + "<Node>: <Nil> " +
                        ', '.join(displayCont) + "\n")
            else:
                displayCont = []
                j = 0  # the index of node.keys.
                for child in node.values:
                    # displayCont += [child.address]
                    if child.keys[-1] >= node.keys[j]:
                        displayCont += [node.keys[j]]
                        j += 1
                    displayCont += [child.address]
                f.write(str(_prefix) + "<" + ', '.join([node.address]) + ">" + "<Node>: " +
                        " <" + ', '.join([node.parent.address]) + ">" + ', '.join(displayCont) + "\n")

        else:
            displayCont = []
            for i,data in enumerate(node.keys):
                displayCont += [data, node.values[i]]
            if node.prev is None:
                f.write(str(_prefix) + "<" + ', '.join([node.address]) + ">" + "<Leaf>: " +
                        " <Nil>" + " <" + ', '.join([node.next.address]) + "> "
                        + ', '.join(displayCont) + "\n")
            elif node.next is None:
                f.write(str(_prefix) + "<" + ', '.join([node.address]) + ">" + "<Leaf>: " +
                        " <" + ', '.join([node.prev.address]) + ">" + "<Nil> "
                        + ', '.join(displayCont) + "\n")
            else:
                f.write(str(_prefix) + "<" + ', '.join([node.address]) + ">" + "<Leaf>: " +
                        " <" + ', '.join([node.prev.address]) + ">" + " <" + ', '.join([node.next.address]) + "> "
                        + ', '.join(displayCont) + "\n")
        _prefix += "   " if _last else "|  "

        if type(node) is Node:
            # Recursively print the key of child nodes (if these exist).
            for i, child in enumerate(node.values):
                _last = (i == len(node.values) - 1)
                self.SaveTreeStructure(child, file, _prefix, _last, f)

    def saveTree(self, dir):
        with open("../treePic/" + dir +".txt", "w") as f:
            self.SaveTreeStructure(f = f)

    def readPagePool(self, ):
        with open("../index/pagePool.txt", "r") as f:  # 打开文件
            data = json.load(f)
            if data == []:
                return 0
            else:
                return data[0][2:5]

    def writePoolPage(self, ):
        with open("../index/pagePool.txt", "r") as f:  # 打开文件
            data = json.load(f)
            #data.append(self.pagePool)
            data = data + self.pagePool
            data = data[::-1]
        with  open("../index/pagePool.txt", "w") as f:
            json.dump(data, f)

    def getTableName(self, rel):
        """
        """
        with open(self.table_path, "r") as f:  # 打开文件
            data = json.load(f)
            for SingleTable in data:
                if SingleTable[0] not in self.TabeNames:
                    self.TabeNames.append(SingleTable[0])
            return(self.TabeNames)

    def addAttrFromFile(self, TableName):
        with open(self.table_path, "r") as f:
            data = json.load(f)
            for SingleTable in data:
                if SingleTable[0] == TableName:
                    self.attribute.append(SingleTable[1])
                    self.typeOfAtt.append(SingleTable[2])
        #print(self.attribute)

    def getIndexOfAttr(self, Attr):
        #print(self.attribute)
        #print(Attr)
        if Attr not in self.attribute:
            raise ValueError('Attribute not in the relation')
        for i, attr in enumerate(self.attribute):
            if attr == Attr:
                return i

    def output(self):
        return splits, parent_splits, fusions, parent_fusions, self.depth

    def getDepth(self):
        return self.depth

    def addValueFromFile(self, dataPath):
        '''
        copy all value from file, dataPath is the string of file path, and copy it
        to the self.valueTuple
        以文件名为index
        '''
        cur_dir = os.getcwd()
        os.chdir(dataPath)
        valueTuple = []
        # read all txt file under this directory
        for i, filename in enumerate(os.listdir('.')):
            #print(i, filename)
            with open(filename, "r") as f:
                data = json.load(f)
                if len(data) > 10:
                    continue;
                #for SingleValue in data:
                self.insert( filename, data )
        os.chdir('..')
        os.chdir(cur_dir)

    def addSpecValueFromFile(self, rel, att):
        '''
        rel is the name of the table
        att is the key value
        '''
        global valueIndex
        self.TabeNames = rel
        self.keyAttr = att
        self.addAttrFromFile(rel)
        index = self.getIndexOfAttr(att)
        dataPath = "../data/" + rel
        cur_dir = os.getcwd()
        os.chdir(dataPath)
        for i, filename in enumerate(os.listdir('.')):
            #print(self.pagePool)
            with open(filename, "r") as f:
                data = json.load(f)
                if len(data) > 10:
                    continue;
                for j, value in enumerate(data):
                    key = value[index]
                    inname = filename + "." + str(j)
                    #print(inname)
                    self.insert( key, inname )   # return a new node
        os.chdir('..')
        os.chdir(cur_dir)

        self.writePoolPage()
        self.add2directory()
        self.iteraAddPage()

    def deleteAll(self):
        self.removePage()
        del self.root
        self.root = Node()
        '''
        leaf = self.getSmallestKey()
        leafList = []
        while leaf.next is not None:
            leafList += leaf.keys
            leaf = leaf.next
        for key in leafList:
            self.delete(key)
        #print(leafList)
        '''

    def add2directory(self):
        this_data = [[self.TabeNames, self.keyAttr, self.root.address]]
        data = this_data
        with  open("../index/directory.txt", "r") as f:
            per_data = json.load(f)
        for k in per_data:
            if k[0] == self.TabeNames and k[1] == self.keyAttr:
                return
            data += [k]
        with  open("../index/directory.txt", "w") as f:
            json.dump(data, f)

    def delDirectory(self, rel, att):
        with  open("../index/directory.txt", "r") as f:
            data = json.load(f)
            for i, info in enumerate(data):
                if rel == info[0] and att == info[1]:
                    del data[i]
                    break
        with  open("../index/directory.txt", "w") as f:
            json.dump(data, f)

    def removePage(self, node=None):
        if node is None:
            node = self.root
        filepath = '../index/' + node.address
        print("remove:" + filepath)
        os.remove(filepath)
        if type(node) is Node:
            for i, child in enumerate(node.values):
                self.removePage(child)

    def iteraAddPage(self, node=None, file=None):
        """
        save each node in the form of .txt
        """
        if node is None:
            node = self.root
        filepath = '../index/' + node.address
        with open(filepath, "w") as f:
            if type(node) is Node:
                if node.parent is None:
                    displayCont = []
                    j = 0    #the index of node.keys.
                    for child in node.values:
                        if child.keys[-1] >= node.keys[j]:
                            displayCont += [node.keys[j]]
                            j += 1
                        displayCont += [child.address]
                    f.write("<" + ', '.join([node.address]) + ">" + "<Node>: <Nil> " +
                            ', '.join(displayCont) + "\n")
                else:
                    displayCont = []
                    j = 0  # the index of node.keys.
                    for child in node.values:
                        # displayCont += [child.address]
                        if child.keys[-1] >= node.keys[j]:
                            displayCont += [node.keys[j]]
                            j += 1
                        displayCont += [child.address]
                    f.write("<" + ', '.join([node.address]) + ">" + "<Node>: " +
                            " <" + ', '.join([node.parent.address]) + ">" + ', '.join(displayCont) + "\n")

            else:
                displayCont = []
                for i,data in enumerate(node.keys):
                    displayCont += [data, node.values[i]]
                if node.prev is None:
                    f.write("<" + ', '.join([node.address]) + ">" + "<Leaf>: " +
                            " <Nil>" + " <" + ', '.join([node.next.address]) + "> "
                            + ', '.join(displayCont) + "\n")
                elif node.next is None:
                    f.write("<" + ', '.join([node.address]) + ">" + "<Leaf>: " +
                            " <" + ', '.join([node.prev.address]) + ">" + "<Nil> "
                            + ', '.join(displayCont) + "\n")
                else:
                    f.write("<" + ', '.join([node.address]) + ">" + "<Leaf>: " +
                            " <" + ', '.join([node.prev.address]) + ">" + " <" + ', '.join([node.next.address]) + "> "
                            + ', '.join(displayCont) + "\n")

            if type(node) is Node:
                # Recursively print the key of child nodes (if these exist).
                for i, child in enumerate(node.values):
                    _last = (i == len(node.values) - 1)
                    self.iteraAddPage(child, file)




if __name__ == '__main__':

    bplustree1 = BPlusTree()
    bplustree1.addSpecValueFromFile("Suppliers", "sid")
    bplustree1.displayTree()
    bplustree1.saveTree("Suppliers_sid")
    #bplustree1.deleteAll()
    bplustree2 = BPlusTree()
    bplustree2.addSpecValueFromFile("Supply", "pid")
    #bplustree2.displayTree()
    bplustree2.saveTree("Supply_pid")



#    bplustree.saveTree("Supply_pid")


