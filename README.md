# sqlDBEngine

description of the directory structure 

1.Data file: simulating data record of relations
![image](https://user-images.githubusercontent.com/105361628/209983718-165a6b71-25df-4e69-aa9d-248672749f24.png)

2. index file
![image](https://user-images.githubusercontent.com/105361628/209983732-771966df-81e9-476f-88d9-bc1636f59c52.png)

directory.txt: B+ Tree directory, include ["relation name", "search key",   "root address"]
Pagepool.txt: save the memory address that were occupied by B+ Tree.
Pgxxx.txt: save the information of each node of B+Tree, for example 
Root node:  <pg050.txt><Node>: <Nil>[['pg049.txt', 'p15', 'pg022.txt']]
Internal node:  <pg029.txt><Node>:  <pg048.txt>[['pg028.txt', 'p03', 'pg042.txt', 'p04', 'pg017.txt']], 
Leaf node:  <pg017.txt><Leaf>:  <pg042.txt> <pg044.txt> ['p04', ['page20.txt.1'], 'p05', ['page08.txt.0']], 

3.program file: include the eight functions described in this project
![image](https://user-images.githubusercontent.com/105361628/209983840-1f3d89b8-7f47-4f44-b8b4-1d6691ab5be4.png)

4.QueryOutput file: contains a single file in which you print the resulting tables from the queries.
![image](https://user-images.githubusercontent.com/105361628/209983848-275fc15e-8e3b-4d71-872a-948f3afde508.png)

5. TreePic file: a list of files in which the B+ trees you create are displayed. 
![image](https://user-images.githubusercontent.com/105361628/209983858-64bef004-7734-4c48-a2b5-2e3cc0b2e519.png)




screenshots for the output that shows the IO costs from those queries 
Question8
a: with B+ tree 
the following figure demonstrates the architecture of B+Tree
![image](https://user-images.githubusercontent.com/105361628/209983981-e07e70c0-4055-4434-a2c9-d4cc1bda6e26.png)

The following graph illustrates the attribute of B+Tree.
![image](https://user-images.githubusercontent.com/105361628/209983969-24e26e36-1e86-4eda-942c-a07539af4a9d.png)


This picture represents current state of index file, each pgxxx.txt is a page of node of B+Tree.
![image](https://user-images.githubusercontent.com/105361628/209983991-5a467c27-aac1-4060-99b9-d6746a05a2ff.png)

The result of Qa is:
![image](https://user-images.githubusercontent.com/105361628/209984015-cf4db317-58e4-4438-a50f-c7dabdf5e0a8.png)


b: 
when removing the B+Tree, the structure of index file and directory.txt have changed. 
The structure of B+Tree was shown in the following photo.
![image](https://user-images.githubusercontent.com/105361628/209984027-fef7370d-bf14-461c-b201-8ef9e5194223.png)

And current directory.txt will be empty like that:
![image](https://user-images.githubusercontent.com/105361628/209984036-8c671989-27ec-462a-bc23-95f4a77c59aa.png)

And each page(pgxxx.txt) that in the index file are all removed:
![image](https://user-images.githubusercontent.com/105361628/209984040-90291061-aa01-455c-90f6-b615dbfb70af.png)

Txt files where the B+_trees are displayed 
![image](https://user-images.githubusercontent.com/105361628/209984103-6797723a-4d7c-4e55-b97a-411965d6e4bd.png)
![image](https://user-images.githubusercontent.com/105361628/209984109-489573d4-8d62-4527-9935-fad20e90be6c.png)
![image](https://user-images.githubusercontent.com/105361628/209984114-6836d2ae-f638-4508-b10f-8245884775ea.png)



