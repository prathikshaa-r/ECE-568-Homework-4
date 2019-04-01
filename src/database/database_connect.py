#!/usr/bin/python3
"""
March 28, 2019
Connect to database and perform all required sql queries
"""
_author_ = "Prathikshaa Rangarajan"
_maintainer_= "Prahikshaa Rangarajan"

import psycopg2
import sys

from ..parser.xml_parser_header import *

# sys.path.append('..')
# import parser.xml_parser_header

# if __name__ == "__main__" and __package__ is None:
#         from sys import path
#         from os.path import dirname as dir

#         path.append(dir(path[0]))
#         from src.parser.xml_parser_header import Accounts

# from parser.xml_parser_header import Accounts

# Connects to the database and returns database connection object
def connect():
    try:
        database='exchange_matching'
        conn = psycopg2.connect(database='exchange_matching',\
                                user='postgres', password='passw0rd',\
                                host='0.0.0.0', port='5432')

        print("Opened database %s successfully." % database)
    except:
        print("Failed to connect to database %s.", database)
        pass
    return conn

#-------------------------------Creations--------------------------------#

'''
 Takes a connection object and account creation fields
 creates account, if successful, returns connection object
 else raises
 -- psycopg2.IntegrityError
 -- ValueError
'''
test_account= Account()
create_account(connect(), test_account)

def create_account(conn, account):
    try:
        account_id_int = int(account.account_id)
        balance_float = float(account.balance)
    except: # ValueError
        account.created = False
        account.err = "Invalid Account Format"

    try:    
        cur = conn.cursor()
        cur.execute('''INSERT INTO Accounts
        (account_id, balance)
        VALUES (%s, %s);'''
                    , (account.account_id, account.balance))

        conn.commit()

    except psycopg2.IntegrityError:
        account.created = False
        account.err = "Account already exists."
    except:
        account.creasted = False
        account.err = "Account creation failed due to unknown reasons."
        # print ('Failed to create account', sys.exc_info())
        pass
    conn.commit()
    return conn

def test_account_creation():
    try:
        create_account(connect(), 10, 1234.45)
    except psycopg2.IntegrityError:
        print("Account already exists")
        pass
    except ValueError:
        print("Invalid Account Format")
        pass
    except:
        print("Account creation failed due to unknown reasons.")
        pass
    pass


test_position = Position()
create_position(connect(), test_position)

def create_position(conn, position):
    try:
        amount_float = float(position.amount)
        account_id_int = int(position.account_id)
    except: # ValueError
        position.created = False
        position.err = "Invalid position format"

    try:
        cur = conn.cursor()
        cur.execute('''SELECT COUNT(*) FROM Positions
        WHERE symbol = %s AND account_id = %s''', (position.symbol, position.account_id))
        row = cur.fetchone()

        # update if position already exists
        if row[0] == 1:
            cur.execute('''UPDATE Positions SET amount = amount + %s 
            WHERE symbol = %s AND account_id = %s''', (position.amount, position.symbol, position.account_id))
            pass
        # create new, if no such position exists
        else:
            cur.execute('''INSERT INTO Positions (symbol, amount, account_id) 
            VALUES(%s, %s, %s)''', (position.symbol, position.amount, position.account_id))
            pass

        conn.commit()

    except psycopg2.IntegrityError:
        # raise
        position.created = False
        position.err = "Postion creation failed due to unknown reasons"
    except:
        # print ('Failed to create position', sys.exc_info())
        # pass
        position.created = False
        position.err = "Postion creation failed due to unknown reasons"
    conn.commit()
    return conn

def test_position_creation():
    try:
        create_position(connect(), "ac", 100, 12)
    except ValueError:
        print("Invalid position format")
        pass
    except:
        print("Postion creation failed due to unknown reasons")
        pass
           
#-----------------------------------------Transactions-----------------------------------------#

#def create_order(conn, trans_id, symbol, amount, limit_price, account_id):
    






