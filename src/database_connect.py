#!/usr/bin/python3
"""
March 28, 2019
Connect to database and perform all required sql queries
"""
_author_ = "Prathikshaa Rangarajan"
_maintainer_= "Prahikshaa Rangarajan"

import psycopg2
import sys

from xml_parser_header import *

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
#test_account= Account()
#create_account(connect(), test_account)

def create_account(conn, account):
    try:
        account_id_int = int(account.account_id)
        balance_float = float(account.balance)
    except: # ValueError
        account.created = False
        account.err = "Invalid Account Format" + sys.exc_info()

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
        account.err = "Account creation failed due to unknown reasons." + sys.exc_info()
        # print ('Failed to create account', sys.exc_info())
        pass
    conn.commit()
    return account

def test_account_creation():
    try:
        db_conn = connect()
        create_account(db_conn, 10, 1234.45)
        db_conn.close()
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


#test_position = Position()
#create_position(connect(), test_position)

def create_position(conn, position):
    try:
        amount_float = float(position.amount)
        account_id_int = int(position.account_id)
    except: # ValueError
        position.created = False
        position.err = "Invalid position format"  + sys.exc_info()

    try:
        cur = conn.cursor()

    # read-modify write start
    # lock(symbol)
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
    # unlock(symbol)
    # read-modify-write end

    except psycopg2.IntegrityError:
        # raise
        position.created = False
        position.err = "Postion creation failed due to unknown reasons" + sys.exc_info()
    except:
        # print ('Failed to create position', sys.exc_info())
        # pass
        position.created = False
        position.err = "Postion creation failed due to unknown reasons" + sys.exc_info()
    conn.commit()
    return position

def test_position_creation():
    try:
        db_conn = connect()
        create_position(db_conn, "ac", 100, 12)
        db_conn.close()
    except ValueError:
        print("Invalid position format")
        pass
    except:
        print("Postion creation failed due to unknown reasons")
        pass
           
#-----------------------------------------Transactions-----------------------------------------#

def create_order(conn, order, account_id):
    # type checking inputs
    try:
        amount_float = float(order.amount)
        account_id_int = int(account_id)
        limit_price_float = float(order.limit_price)
    except: # ValueError
        raise

    buy = True
    if amount < 0 :
        buy = False
        pass

    # """
    # Buy Order
    # Reduce balance in Accounts
    # """
    if buy is True:
        create_buy_order(conn, order, account_id)
    # """
    # Sell Order
    # Reduce amount in positions
    # """

    else:
        create_sell_order(conn, order, account_id)
        pass
    pass
        
def create_buy_order(conn, order, account_id):
    try:
        cur = conn.cursor()
    # read-modify-write start
    # lock(Accounts)
        cur.execute('''SELECT balance FROM Accounts WHERE accoutn_id = %s''', (account_id,))
        row = cur.fetchone()
        balance = row[0]
        share_price = order.limit_price * order.amount
        if balance < share_price:
            # Insufficient funds error
            return
        cur.execute('''UPDATE Accounts SET balance = balance-%s WHERE accoutn_id = %s''', (share_price, account_id))
        cur.execute('''INSERT INTO Orders (trans_id, symbol, amount, limit_price, account_id) VALUES(%s, %s, %s, %s, %s)''', (order.trans_id, order.symbol, order.amount, order.limit_price, account_id))
    # unlock(Accounts)
    # read-modify-write end
        conn.commit()

    except psycopg2.IntegrityError:
        raise
    except:
        print ('Failed to create buy order', sys.exc_info())
        pass
    conn.commit()
    return conn

def create_sell_order(conn, order, account_id):
    try:
        cur = conn.curson()
    # read-modify-write start
    # lock(Positions)
        cur.execute('''SELECT COUNT(*) FROM Positons 
        WHERE symbol = %s AND account_id = %s AND amount > (-%s)''', (order.symbol, account_id, order.amount))
        row = cur.fetchone()
        position_count = row[0]
        if position_count != 1:
            # Insufficient Shares to sell error
            printf("Insufficient shares to sell")
            return
        cur.execute('''UPDATE Postions SET amount = amount + %s 
       WHERE account_id = %s AND symbol = %s''', (order.amount, account_id, order.symbol))
        cur.execute('''INSERT INTO Orders (trans_id, symbol, amount, limit_price, account_id) VALUES(%s, %s, %s, %s, %s)''', (order.trans_id, order.symbol, order.amount, order.limit_price, account_id))

    # unlock(Postions)
    # read-modify-write end
        conn.commit()

    except psycopg2.IntegrityError:
        raise
    except:
        print('Failed to create sell order', sys.exc_info())
        pass
    conn.commit()
    pass
    return conn

def test_order():
    order = Order("aa", )
    return
