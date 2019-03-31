#!/usr/bin/python3
"""
March 26, 2019
Creates the required objects that the XML parser reads into.
"""


_author_ = "Yanjia Zhao"
_maintainer_ = "Prathikshaa Rangarajan"

import xml.etree.ElementTree as ET


"""
classes for Create_obj
"""

class Account:
    def __init__(self, acc_id, balance):
        self.acc_id = acc_id # should be string
        self.balance = balance
        self.type = 'account'
        self.created = True ##True means created succuss, FALSE means error; True as default
        self.err = ""

    """
    print function
    """
    def __repr__(self):
        print('Account ID: ', self.acc_id)
        print('Account Balance: ', self.balance)

        return ''

        
class Position:
    def __init__(self, symbol, acc_id, number):
        self.symbol = symbol
        self.account_id = acc_id #the array of Account objects, should be string
        self.number = number # no. of shares of the symbol to be added to the account
        self.type = 'position'
        self.created = True ##True means created succuss, FALSE means error; True as default
        self.err = ""
    """
    print function
    """
    def __repr__(self):
        print('Symbol: ', self.symbol)
        print('Account ID: ', self.account_id)
        print('Num. of shares of symbol: ', self.number)
            
        return ''

        
class Create_obj:
    def __init__(self):
        self.sequence=[]

    """
    print function
    """        
    def __repr__(self):
        print('Create:')
        for index in range (0, len(self.sequence)):
            print(self.sequence[index])
            pass    
        
       
        return ''


"""
classes for Transaction_obj
"""
        
class Order:
    def __init__(self, sym, amount, limit_price):
        self.sym = sym
        self.amount = amount
        self.limit_price = limit_price
        self.type = 'order'

    """
    print function
    """        
    def __repr__(self):

        print('Order:')
        print('Symbol: ', self.sym)
        print('Amount: ', self.amount)
        print('Limit: ', self.limit_price)

        return ''
        
class Query:
    def __init__(self, id):
        self.id = id
        self.type = 'query'

    """
    print function
    """        
    def __repr__(self):
        print('Query ID: ', self.id)
        return ''

        
class Cancel:
    def __init__(self, id):
        self.id = id
        self.type = 'cancel'

    """
    print function
    """        
    def __repr__(self):
        print('Cancel ID: ', self.id)
        return ''

        
class Transaction_obj:
    def __init__(self, id):
        self.id = id
        self.sequence = []

    """
    print function
    """        
    def __repr__(self):
        print('Transaction ID: ', self.id)

        for element in self.sequence:
            print(element)
            
        return ''

# todo: convert below to a function
# xml_parser("file.xml")

def parse_xml(recv_string):
    #tree = ET.parse(file_path)
    #root = tree.getroot()
    root=ET.fromstring(recv_string)
    #process create object here
    if root.tag=='create':
        create_obj=Create_obj()
        for child in root:
            if child.tag=='account':
                id1=child.attrib.get('id')
                balance=child.attrib.get('balance')
                account=Account(id1,balance)
                #create_obj.account.append(account)
                create_obj.sequence.append(account)
                pass

            elif child.tag=='symbol':
                sym=child.attrib.get('sym')

                for grandchild in child:
                    position_acc_id=grandchild.attrib.get('id')
                    num=grandchild.text
                    pass

                pos = Position(sym, position_acc_id, num)
                #create_obj.position.append(pos)
                create_obj.sequence.append(pos)
                pass
            pass
        print(create_obj)
                
        # for account in create_obj.account:
        #     print(account.id, account.balance)

        # for symbol in create_obj.symbol:
        #     print(symbol.sym)
        #     for account in symbol.account:
        #         print(account.id, account.balance)
        pass

    #process transaction object here
    if root.tag=='transactions':
        id1=root.attrib.get('id')
        transaction_obj=Transaction_obj(id1)
        for child in root:
            if child.tag=='order':
                symbol=child.attrib.get('sym')
                amount=child.attrib.get('amount')
                limit = child.attrib.get('limit')
                order=Order(symbol,amount,limit)
                transaction_obj.sequence.append(order)
                pass

            elif child.tag=='query':
                id2 = child.attrib.get('id')
                query=Query(id2)
                transaction_obj.sequence.append(query)
                pass

            elif child.tag=='cancel':
                id2 = child.attrib.get('id')
                cancel=Cancel(id2)
                transaction_obj.sequence.append(cancel)
                pass
            pass

        print(transaction_obj)

    #     print("Transaction_Obj ID: ", transaction_obj.id)
    #     for order in transaction_obj.order:
    #         print(order.sym,order.amount,order.limit)
    #     for query in transaction_obj.query:
    #         print(query.id)
    #     for cancel in transaction_obj.cancel:
    #         print(cancel.id)
    #         pass
    #     pass
    # pass


