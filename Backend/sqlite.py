import sqlite3

connection=sqlite3.connect("student.db")



cursor=connection.cursor()


table_info ="""
 create table STUDENT(
 NAME VARCHAR(25),
 CLASS varchar(25),
 SECTION VARCHAR(25),
 MARKS INT

 )
"""

cursor.execute(table_info)



cursor.execute("insert into STUDENT values('Rahul','10','A',90)")
cursor.execute("insert into STUDENT values('sh','2','b',50)")
cursor.execute("insert into STUDENT values('shri','2','b',50)")
cursor.execute("insert into STUDENT values('varsha','2','b',50)")
 


print("The inserted data is")


data=cursor.execute("select * from STUDENT")


for row in data:
    print(row)

connection.commit()
connection.close()