import pandas as pd
import os
import re
import json
import sys
from buildTree import BPlusTree


class BpTreeRelAlg(BPlusTree):
    def __init__(self):
        super(BPlusTree, self).__init__()
        cost = 0

    def getCost(self):
        return self.cost

    def join(self, rel1, att1, rel2, att2):    # find rel1.att1 == rel2.att2
        '''
        未完成
        '''
        newTable = []
        temp = []
        bplustree1 = BPlusTree()
        bplustree2 = BPlusTree()
        bplustree1.addSpecValueFromFile(rel1, att1)
        bplustree2.addSpecValueFromFile(rel2, att2)
        index1 = bplustree1.getIndexOfAttr(att1)   #get the index of att1 in rel1
        index2 = bplustree1.getIndexOfAttr(att2)
        #att1 = bplustree1.addAttrFromFile(rel1)    #get the attributes of table1(rel)
        #att2 = bplustree2.addAttrFromFile(rel2)
        #tempAttr = att2
        #print(index1)
        #del(tempAttr[index2])       # delete the repeated attribute
        #newAttr = att1 + tempAttr    # design an new table that contains both the attributes of rel1 and rel2
        '''find the value of rel1.att1'''
        leaf1 = bplustree1.getSmallestKey()   #get the smallest node from rel1
        i = 0
        while leaf1.next is not None:       # iteratively get the leaf
            for key1 in leaf1.keys:
                leaf2 = bplustree2.find(key1)
                for key2 in leaf2.keys:
                    if key1 == key2:
                        temp = bplustree1.getQueryCont(key1)
                        del(temp[index1])
                        newTable += [bplustree2.getQueryCont(key1) + temp]
            leaf1 = leaf1.next
        #self.showTable(newTable)
        return newTable

    def select(self, relation, attribute, operand, value):    # With B+Tree
        newTable = []     # this newTable is to reserve the result
        temp = []
        cost = 0
        bplustree = BPlusTree()     # design a B+Tree
        bplustree.addSpecValueFromFile(relation, attribute)   # add the relation and attribute to the B+Tree
        index = bplustree.getIndexOfAttr(attribute)   # get the index of attribute in previous table
        cost = bplustree.getDepth() + 1
        self.cost = cost
        #print("Cost: " + str(cost))
        #bplustree.displayTree()


        if operand == '=' :
            # newTable = bplustree.getQueryCont(value)    # find the value that == value
            curLeaf = bplustree.find(value)
            for key in curLeaf.keys:  # iteratively get the value from each page
                if key == value:  # estimate whether the key is satisfy the condition
                    newTable = [bplustree.getQueryCont(key)]

        elif operand == '<' :
            curLeaf = bplustree.find(value)     # find the leaf that contain the value
            while curLeaf.prev is not None:     # judge whether curLeaf is the first leaf
                for key in curLeaf.keys:        # iteratively get the value from each page
                    if key < value:             # estimate whether the key is satisfy the condition
                        temp += [bplustree.getQueryCont(key)]
                temp.reverse()
                newTable += temp
                temp = []
                curLeaf = curLeaf.prev          # go to next leaf


        elif operand == '<=' :
            curLeaf = bplustree.find(value)     # find the leaf that contain the value
            while curLeaf.prev is not None:     # judge whether curLeaf is the first leaf
                for key in curLeaf.keys:        # iteratively get the value from each page
                    if key <= value:             # estimate whether the key is satisfy the condition
                        temp += [bplustree.getQueryCont(key)]
                temp.reverse()
                newTable += temp
                temp = []
                curLeaf = curLeaf.prev          # go to next leaf

        elif operand == '>' :
            curLeaf = bplustree.find(value)  # find the leaf that contain the value
            while curLeaf.next is not None:  # judge whether curLeaf is the last leaf
                for key in curLeaf.keys:  # iteratively get the value from each page
                    if key > value:  # estimate whether the key is satisfy the condition
                        temp += [bplustree.getQueryCont(key)]
                temp.reverse()
                newTable += temp
                temp = []
                curLeaf = curLeaf.next  # go to next leaf

        elif operand == '>=' :
            curLeaf = bplustree.find(value)  # find the leaf that contain the value
            while curLeaf.next is not None:  # judge whether curLeaf is the first leaf
                for key in curLeaf.keys:  # iteratively get the value from each page
                    if key >= value:  # estimate whether the key is satisfy the condition
                        temp += [bplustree.getQueryCont(key)]
                temp.reverse()
                newTable += temp
                temp = []
                curLeaf = curLeaf.next  # go to next leaf
        return newTable

    def saveTable(self):
        with open("../queryOutput/queryResult.txt", "w") as f:
            f.write('  '.join(self.attribute)+"\n")
            for data in self.valueTuple:
                f.write(str(data)+"\n")


class relationalAlgebraOperations():
    def __init__(self):
        self.relation = 1

    def tableSort(self, index, Class ):
        if not isinstance(Class, table):
            raise ValueError('Relation must a type of Table')
        result = sorted(Class.valueTuple, key=lambda x: x[index])
        return result

    def getIndexOfAttr(self, Attr, Class):
        '''
        return the index of the attribute of the table
        :param Attr:  attribute, class of relation
        :return:  index number
        '''
        if not isinstance(Class, table):
            raise ValueError('Relation must a type of Table')
        for i, attr in enumerate(Class.attribute):
            if attr == Attr:
                return i

    def join(self, rel1, att1, rel2, att2):
        '''

        :param rel1:
        :param att1:
        :return:
        '''
        if not isinstance(rel1, table):
            raise ValueError('Relation1 must a type of Table')
        if not isinstance(rel2, table):
            raise ValueError('Relation2 must a type of Table')
        if att1 not in rel1.attribute:
            raise ValueError('There is no attribute1 in this relation1')
            return
        if att2 not in rel2.attribute:
            raise ValueError('There is no attribute2 in this relation2')
            return
        newTable = []
        index1 = self.getIndexOfAttr(att1, rel1)
        index2 = self.getIndexOfAttr(att2, rel2)
        tempAttr = rel2.attribute
        del(tempAttr[index2])
        newAttr = rel1.attribute + tempAttr
        i = 0
        for data1 in rel1.valueTuple:
            for data2 in rel2.valueTuple:
                if data1[index1] == data2[index2]:
                    newTable.append([])
                    del(data2[index2])
                    newTable[i] = data1+data2
                    i = i + 1
        #self.showTable(newTable)
        return self.NewTable('NewTable', newAttr, newTable)

    def project(self, relation, attList):
        '''
        :param rel:
        :param attList:
        :return:
        '''
        if not isinstance(relation, table):
            raise ValueError('Relation must a type of Table')
        for attribute in attList:
            if attribute not in relation.attribute:
                raise ValueError('There is no attribute in this relation')
                return
        sizeOfAttList = len(attList)
        newTable = []
        index = []
        for i in range(0, sizeOfAttList):    #get the location of attributes
            index.append(self.getIndexOfAttr(attList[i], relation))
        print(index)
        for i,data in enumerate(relation.valueTuple):
            newTable.append([])
            for j in range(sizeOfAttList):
                newTable[i].append(data[index[j]])
        #self.showTable(newTable)
        return self.NewTable('NewTable', attList, newTable)

    def select(self, relation, attribute, operand, value):
        if attribute not in relation.attribute:
            raise ValueError('There is no attribute in this relation')
            return
        newTable = []
        index = self.getIndexOfAttr(attribute, relation)
        newValueTuple = self.tableSort(index, relation)
        '''
        for data in newValueTuple:
            print(data)
        '''
        if operand == '=' :
            j = 0
            for i, data in enumerate(newValueTuple) :
                if data[index] == value:
                    newTable.append([])
                    newTable[j] = data
                    j+=1
        elif operand == '<' :
            j = 0
            for i, data in enumerate(newValueTuple) :
                if data[index] < value:
                    newTable.append([])
                    newTable[j] = data
                    j+=1

        elif operand == '<=' :
            j = 0
            for i, data in enumerate(newValueTuple) :
                if data[index] <= value:
                    newTable.append([])
                    newTable[j] = data
                    j+=1
        elif operand == '>' :
            j = 0
            for i, data in enumerate(newValueTuple) :
                if data[index] > value:
                    newTable.append([])
                    newTable[j] = data
                    j+=1
        elif operand == '>=' :
            j = 0
            for i, data in enumerate(newValueTuple) :
                if data[index] >= value:
                    newTable.append([])
                    newTable[j] = data
                    j+=1
        return self.NewTable('NewTable', relation.attribute, newTable)

    def showTable(self, table):
        for data in table:
            print(data)

    def NewTable(self, tableName, attr, tableValue):
        NewTable = table(tableName)
        NewTable.addAttr(attr)
        NewTable.addValue(tableValue)
        return NewTable


class DataBaseFactory:
    def __init__(self,):
        self.file_path = "../data/"
        self.table_path = self.file_path + "schemas.txt"
        self.TabeNames = []

    '''
    getTableName():
        get the title of table, and return it
        "schemas.txt"
    '''
    def getTableName(self,):
        with open(self.table_path, "r") as f:  # 打开文件
            data = json.load(f)
            for SingleTable in data:
                if SingleTable[0] not in self.TabeNames:
                    self.TabeNames.append(SingleTable[0])
            return(self.TabeNames)

    '''
    createTable():
        generate table, include attribute, value, types,
        and return a class of table
    '''
    def createTable(self, TableName):
        if(TableName == ''):
            print("Error, the name of table is NULL")
        newTable = table(TableName)
        newTable.addAttrFromFile(self.table_path, TableName)
        newDataPath = self.file_path + TableName + "/"
        #print(newDataPath)
        newTable.addValueFromFile(newDataPath)
        return newTable

    '''
    dumpTable(self, TableClass):
        TableClass is the Class a the table, json file
    '''
    def dumpTable(self, TableClass):
        name = TableClass.getName()
        filename = "../queryOutput/" + name + '.json'
        with open(filename, 'w') as file_obj:
            json.dump(TableClass.getAttr(), file_obj)
            json.dump(TableClass.getTable(), file_obj)


class table:
    '''
    Each table is a class of table
    '''
    def __init__(self, name = None):
        self.name = name   #the name of table
        self.row = 0
        self.attribute = []
        self.typeOfAtt = []
        self.valueTuple = []
        self.NumOfCol = 0
        self.numOfRow = 0

    def getName(self):
        return self.name

    def getAttr(self):
        return self.attribute

    def getSize(self):
        return len(self.valueTuple)

    def getTable(self):
        return self.valueTuple

    def addAttr(self, attr):
        self.attribute = attr

    def addAttrFromFile(self, AttrPath, TableName):
        with open(AttrPath, "r") as f:
            data = json.load(f)
            for SingleTable in data:
                if SingleTable[0] == TableName:
                    self.attribute.append(SingleTable[1])
                    self.typeOfAtt.append(SingleTable[2])

    def addValue(self, ValueTuple):
        '''
        copy ValueTuple to Table.valueTuple
        :param ValueTuple:
        :return:
        '''
        self.valueTuple = ValueTuple

    def addValueFromFile(self, dataPath):
        '''
        copy all value from file, dataPath is the string of file path, and copy it
        to the self.valueTuple
        :param dataPath:
        :return:
        '''
        cur_dir = os.getcwd()
        os.chdir(dataPath)
        # read all txt file under this directory
        j = 0;
        for i, filename in enumerate(os.listdir('.')):
            #print(i, filename)
            with open(filename, "r") as f:
                data = json.load(f)
                if len(data) > 10:
                    continue;
                for SingleValue in data:
                    self.valueTuple.append([])
                    self.valueTuple[j] = SingleValue
                    j=j+1
        self.numOfRow = j
        os.chdir('..')
        os.chdir(cur_dir)

    def printTable(self):
        print()
        print(self.attribute)
        for data in self.valueTuple:
            print(data)

    def saveTable(self):
        with open("../queryOutput/queryResult.txt", "w") as f:
            f.write('  '.join(self.attribute)+"\n")
            for data in self.valueTuple:
                f.write(str(data)+"\n")


def test1():
    '''
    获取价格在20-24之间的grey颜色的memory的雇主产品名，颜色，价格，名称，以及雇主地址
    '''
    dataBase = DataBaseFactory()
    tableName = dataBase.getTableName()  # get all names of tables of this database
    operand = relationalAlgebraOperations()

    Suppliers = dataBase.createTable(tableName[0])  # Suppliers
    Products = dataBase.createTable(tableName[1])  # Products
    Catalogs = dataBase.createTable(tableName[2])  # Catalogs

    ##第一步：选取范围在35-45之间的value
    newtable = operand.select(operand.select(Catalogs, 'cost', '<=', 45), 'cost', '>', 35)
    ##第二步：联合newTable和Products表
    newtable = operand.join(operand.join(Products, 'pid', newtable, 'pid'), 'sid', Suppliers, 'sid')
    ##第三步：选取灰色的memory
    newtable = operand.select(newtable, 'color', '=', 'grey')
    newtable = operand.select(newtable, 'pname', '=', 'memory')
    ##第四步：选取属性：pname，color，address
    att = ['pname', 'color', 'cost', 'address']
    newtable = operand.project(newtable, att)
    newtable.printTable()
    newtable.saveTable()

def testBPTree():

    with open("../queryOutput/queryResult.txt", "w") as f:
        print("Qa: ")
        f.write("Qa: " + "\n")
        BpTreeOpare = BpTreeRelAlg()
        newTable = BpTreeOpare.select("Suppliers", "sid", "=", "s23")
        print("When B+Tree used, the cost of searching Suppliers is: " + str(BpTreeOpare.getCost()))
        f.write("When B+Tree used, the cost of searching Suppliers is: " + str(BpTreeOpare.getCost()) + "\n")
        print(newTable)
        for data in newTable:
            f.write(str(data) + "\n")


        print("Qb: ")
        f.write("Qb: " + "\n")
        dataBase = DataBaseFactory()
        tableName = dataBase.getTableName()  # get all names of tables of this database
        operand = relationalAlgebraOperations()
        Suppliers = dataBase.createTable(tableName[0])  # Suppliers
        Products = dataBase.createTable(tableName[1])  # Products
        Supply = dataBase.createTable(tableName[2])  # Catalogs
        cost = Suppliers.getSize()
        print("When B+Tree not used, the cost of searching Suppliers is: " + str(cost))
        f.write("When B+Tree not used, the cost of searching Suppliers is: " + str(cost) + "\n")
        newTable = operand.select(Suppliers, "sid", "=", "s23")
        newTable.printTable()
        f.write('  '.join(newTable.attribute) + "\n")
        for data in newTable.valueTuple:
            f.write(str(data) + "\n")

        print("Qc: ")
        f.write("Qc: " + "\n")
        newTable = operand.join(Products, 'pid', Supply, 'pid')
        newTable = operand.select(newTable, "pid", "=", "p15")
        newTable = operand.join(newTable, "sid", Suppliers, 'sid')
        att = ['pid', 'address']
        newTable = operand.project(newTable, att)
        newTable.printTable()
        f.write('  '.join(newTable.attribute) + "\n")
        for data in newTable.valueTuple:
            f.write(str(data) + "\n")

        print("Qd: ")
        f.write("Qd: " + "\n")
        dataBase = DataBaseFactory()
        tableName = dataBase.getTableName()  # get all names of tables of this database
        operand = relationalAlgebraOperations()
        Suppliers = dataBase.createTable(tableName[0])  # Suppliers
        Products = dataBase.createTable(tableName[1])  # Products
        Supply = dataBase.createTable(tableName[2])  # Supply

        newTable = operand.select(Suppliers, "sname", "=", "Kiddie")
        newTable = operand.join(newTable, "sid", Supply, 'sid')
        newTable = operand.select(newTable, "pid", "=", "p20")
        att = ['pid', 'sname', 'cost']
        newTable = operand.project(newTable, att)
        newTable.printTable()
        f.write('  '.join(newTable.attribute) + "\n")
        for data in newTable.valueTuple:
            f.write(str(data) + "\n")

        print("Qe: ")
        f.write("Qe: " + "\n")
        dataBase = DataBaseFactory()
        tableName = dataBase.getTableName()  # get all names of tables of this database
        operand = relationalAlgebraOperations()
        Suppliers = dataBase.createTable(tableName[0])  # Suppliers
        Products = dataBase.createTable(tableName[1])  # Products
        Supply = dataBase.createTable(tableName[2])  # Supply
        newTable = operand.select(Supply, "cost", ">=", 47)
        newTable = operand.join(newTable, "sid", Suppliers, 'sid')
        newTable = operand.join(newTable, "pid", Products, 'pid')
        att = ['sname', 'pname', 'cost']
        newTable = operand.project(newTable, att)
        newTable.printTable()
        f.write('  '.join(newTable.attribute) + "\n")
        for data in newTable.valueTuple:
            f.write(str(data) + "\n")


if __name__ == '__main__':
    '''
    测试：获取价格在20-24之间的grey颜色的memory的雇主地址，颜色，cost，名称
    '''
    testBPTree()

    

