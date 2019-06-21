import sqlite3

conn = sqlite3.connect('auditoria.db')

print ("Opened database successfully")

conn.execute('''CREATE TABLE AUDITOR
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         EMAIL           TEXT    NOT NULL,
         AGE            INT     NOT NULL,
         ADDRESS        CHAR(50));''')

conn.execute('''CREATE TABLE UTILIZADOR
         (ID INT PRIMARY KEY     NOT NULL,
         USER           TEXT    NOT NULL,
         PASSWORD           TEXT    NOT NULL,
         TYPE            TEXT     NOT NULL);''')

conn.execute('''CREATE TABLE AUDITORIA
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         STDATE           CHAR(20)    NOT NULL,
         ENDATE            CHAR(20)     NOT NULL,
         DESCRIPTION           TEXT    NOT NULL,
         AUDITOR             INT       NOT NULL);''')



cursor = conn.execute("SELECT ID, USER, PASSWORD, TYPE from UTILIZADOR")
for row in cursor:
   print ("ID = ", row[0])
   print ("USER = ", row[1])
   print ("PASSWORD = ", row[2])
   print ("TYPE = ", row[3], "\n")

conn.commit()

print ("Operation done successfully")

print ("Tables created successfully")

conn.close()
