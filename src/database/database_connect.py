#!/usr/bin/python3
import psycopg2

database='exchange_matching'
conn = psycopg2.connect(database='exchange_matching', user='postgres', password='passw0rd', host='0.0.0.0', port='5432')

print("Opened database %s successfully" % database)
cur = conn.cursor()
cur.execute('''CREATE TABLE COMPANY
      (ID INT PRIMARY KEY     NOT NULL,
      NAME           TEXT    NOT NULL,
      AGE            INT     NOT NULL,
      ADDRESS        CHAR(50),
      SALARY         REAL);''')
print "Table created successfully"

conn.commit()
conn.close()
