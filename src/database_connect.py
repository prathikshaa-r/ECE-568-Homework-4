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
from response_obj import *

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
        position.err = "Account corresponding to database may not exist." # + sys.exc_info()
    except:
        # print ('Failed to create position', sys.exc_info())
        # pass
        position.created = False
        position.err = "Postion creation failed due to unknown reasons." # + sys.exc_info()
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
    if order.amount < 0 :
        buy = False
        pass

    # """
    # Buy Order
    # Reduce balance in Accounts
    # """
    if buy is True:
        print('is a buy order')
        order = create_buy_order(conn, order, account_id)
    # """
    # Sell Order
    # Reduce amount in positions
    # """

    else:
        print('is a sell order')
        order = create_sell_order(conn, order, account_id)
        pass

    # match_order(order)
    return order
        
def create_buy_order(conn, order, account_id):
    try:
        cur = conn.cursor()
    # read-modify-write start
    # lock(Accounts)
        cur.execute('''SELECT balance FROM Accounts WHERE account_id = %s''', (account_id,))
        row = cur.fetchone()
        balance = row[0]
        share_price = order.limit_price * order.amount
        if balance < share_price:
            # Insufficient funds error
            order.success = False
            order.err = 'Insufficient Funds'
            return
        
        cur.execute('''UPDATE Accounts SET balance = balance-%s WHERE account_id = %s''', (share_price, account_id))
        cur.execute('''INSERT INTO Orders (trans_id, symbol, amount, limit_price, account_id) VALUES(%s, %s, %s, %s, %s)''', (order.trans_id, order.symbol, order.amount, order.limit_price, account_id))
    # unlock(Accounts)
    # read-modify-write end
        conn.commit()

    except psycopg2.IntegrityError:
        # raise
        order.success = False
        order.err = 'Failed to create order ' + sys.exc_info()
        pass
    except:
        # print ('Failed to create buy order', sys.exc_info())
        order.success = False
        order.err = 'Failed to create order ' 
        pass
    conn.commit()
    return order

def create_sell_order(conn, order, account_id):
    try:
        cur = conn.cursor()
    # read-modify-write start
    # lock(Positions)
        cur.execute('''SELECT COUNT(*) FROM Positions 
        WHERE symbol = %s AND account_id = %s AND amount > (-%s)''', (order.symbol, account_id, order.amount))
        row = cur.fetchone()
        position_count = row[0]
        if position_count != 1:
            # Insufficient Shares to sell error
            order.success = False
            order.err = 'Insufficient shares to sell'
            return
        cur.execute('''UPDATE Positions SET amount = amount + %s 
       WHERE account_id = %s AND symbol = %s''', (order.amount, account_id, order.symbol))
        cur.execute('''INSERT INTO Orders (trans_id, symbol, amount, limit_price, account_id) VALUES(%s, %s, %s, %s, %s)''', (order.trans_id, order.symbol, order.amount, order.limit_price, account_id))

    # unlock(Postions)
    # read-modify-write end
        conn.commit()

    except psycopg2.IntegrityError:
        # raise
        order.success = False
        order.err = "Database Error: Invalid account or symbol or combination thereof " + sys.exc_info()
        pass
    
    except:
        # print('Failed to create sell order', sys.exc_info())
        order.success = False
        order.err = "Failed to create order " + sys.exc_info()
        pass

    conn.commit()
    pass
    return order

def test_order():
    account_id = 1

    sym = "abc"
    amount = -1000
    limit_price = 125
    
    trans_id = 2
    order = Order(sym, amount, limit_price)
    create_order(connect(), order, account_id, trans_id)

    print(order.success)
    print('Error:')
    print(order.err)
    return

# test_order()

def query_order(conn, query_obj):
    query_resp = TransactionResponse(query_obj.trans_id, 'query')

    try:
        trans_id = int(query_obj.trans_id)
    except:
        query_resp.success = False
        query_resp.err = 'Invalid format of transaction id'
        return query_resp

    try:
        cur = conn.cursor()
        cur.execute('''SELECT status, amount, limit_price FROM Orders WHERE trans_id = %s;''', (trans_id,))
        rows = cur.fetchall()
        if not rows:
            query_resp.success = False
            query_resp.err = 'No orders found with given transaction id'
            return query_resp
        
        for row in rows:
            resp = TransactionSubResponse(row[0], row[1], row[2], 'random_time')
            query_resp.trans_resp.append(resp)
    except psycopg2.IntegrityError:
        # raise
        query_resp.success = False
        query_resp.err = "Database Error" + sys.exc_info()
        pass
    
    except:
        query_resp.success = False
        query_resp.err = "Failed to query transaction ID " + sys.exc_info()
        pass

    conn.commit()
    pass
    return query_resp

def test_query():
    query_obj = Query('asd')
    resp = query_order(connect(), query_obj)
    # for row in resp.trans_resp:
    #     print(row)
    #     pass

    # if not resp.success:
    #     print(resp.err)
    #     pass
    print(resp)

test_query()

def cancel_order(trans_id):
    trans_id = int(query_obj.trans_id)
    return
