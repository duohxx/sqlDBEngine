from relAlg import BpTreeRelAlg, relationalAlgebraOperations, DataBaseFactory, table

def test():

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
        #BpTreeOpare.display()

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



'''
includes the three relational algebra functions
'''

if __name__ == '__main__':

    test()