#!/usr/bin/python3
import psycopg2

database='exchange_matching'
conn = psycopg2.connect(database='exchange_matching', user='postgres', password='passw0rd', host='0.0.0.0', port='5432')

print("Opened database %s successfully" % database)
