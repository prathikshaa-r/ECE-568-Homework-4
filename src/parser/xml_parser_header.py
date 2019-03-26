#!/usr/bin/python3
"""
March 26, 2019
Creates the required objects that the XML parser reads into.
"""


_author_ = "Yanjia Zhao"
_maintainer_ = "Prathikshaa Rangarajan"


class Account:
    def __init__(self,id,balance):
        self.id=id
        self.balance=balance

        
class Symbol:
    def __init__(self,sym):
        self.sym=sym
        self.account=[] #the array of Account objects

        
class Create:
    def __init__(self):
        self.account=[] #the array of Account objects
        self.symbol=[] #the array of Symbol objects

        
class Order:
    def __init__(self,sym,amount,limit):
        self.sym=sym
        self.amount=amount
        self.limit=limit

        
class Query:
    def __init__(self,id):
        self.id=id

        
class Cancel:
    def __init__(self,id):
        self.id=id

        
class Transaction:
    def __init__(self,id):
        self.id=id
        self.order=[] #the array of Order objects
        self.query=[] #the array of Query objects
        self.cancel=[] #array of Cancel objects

# todo: convert below to a function
# xml_parser("file.xml")
import xml.etree.ElementTree as ET
tree = ET.parse('test.xml')
root = tree.getroot()
if root.tag=='create':
    create=Create()
    for child in root:
        if child.tag=='account':
            id1=child.attrib.get('id')
            balance=child.attrib.get('balance')
            account=Account(id1,balance)
            create.account.append(account)
        elif child.tag=='symbol':
            symbol=child.attrib.get('sym')
            sym=Symbol(symbol)
            for grandchild in child:
                id2=grandchild.attrib.get('id')
                num=grandchild.text
                account = Account(id2,num)
                sym.account.append(account)
            create.symbol.append(sym)
    #process create object here
    """
    for account in create.account:
        print(account.id, account.balance)
    for symbol in create.symbol:
        print(symbol.sym)
        for account in symbol.account:
            print(account.id, account.balance)
    """

if root.tag=='transactions':
    id1=root.attrib.get('id')
    transaction=Transaction(id1)
    for child in root:
        if child.tag=='order':
            symbol=child.attrib.get('sym')
            amount=child.attrib.get('amount')
            limit = child.attrib.get('limit')
            order=Order(symbol,amount,limit)
            transaction.order.append(order)
        elif child.tag=='query':
            id2 = child.attrib.get('id')
            query=Query(id2)
            transaction.query.append(query)
        elif child.tag=='cancel':
            id2 = child.attrib.get('id')
            cancel=Cancel(id2)
            transaction.cancel.append(cancel)
    #process transaction object here
    """
    print(transaction.id)
    for order in transaction.order:
        print(order.sym,order.amount,order.limit)
    for query in transaction.query:
        print(query.id)
    for cancel in transaction.cancel:
        print(cancel.id)
    """

