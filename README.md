# sqlDBEngine

description of the directory structure 

1.Data file: simulating data record of relations

2. index file

directory.txt: B+ Tree directory, include ["relation name", "search key",   "root address"]
Pagepool.txt: save the memory address that were occupied by B+ Tree.
Pgxxx.txt: save the information of each node of B+Tree, for example 
Root node:  <pg050.txt><Node>: <Nil>[['pg049.txt', 'p15', 'pg022.txt']]
Internal node:  <pg029.txt><Node>:  <pg048.txt>[['pg028.txt', 'p03', 'pg042.txt', 'p04', 'pg017.txt']], 
Leaf node:  <pg017.txt><Leaf>:  <pg042.txt> <pg044.txt> ['p04', ['page20.txt.1'], 'p05', ['page08.txt.0']], 

3.program file: include the eight functions described in this project

4.QueryOutput file: contains a single file in which you print the resulting tables from the queries.

5. TreePic file: a list of files in which the B+ trees you create are displayed. 




screenshots for the output that shows the IO costs from those queries 
Question8
a: with B+ tree 
the following figure demonstrates the architecture of B+Tree

The following graph illustrates the attribute of B+Tree.


This picture represents current state of index file, each pgxxx.txt is a page of node of B+Tree.

The result of Qa is:


b: 
when removing the B+Tree, the structure of index file and directory.txt have changed. 
The structure of B+Tree was shown in the following photo.

And current directory.txt will be empty like that:

And each page(pgxxx.txt) that in the index file are all removed:

The result of Qb is: 

The answers of Qc Qd Qe are:







Txt files where the B+_trees are displayed 




