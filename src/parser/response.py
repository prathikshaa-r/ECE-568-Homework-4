#!/usr/bin/python3
from xml.etree.ElementTree import Element, SubElement
from ElementTree_pretty import prettify
from xml_parser_header import Create_obj,Account,Position
from Response_obj import Sub_Response, Response

##response of create
def create_response(create):#create=Create_obj()
    top=Element('results')
    for child in create.sequence:
        if child.type=='account':
            if child.create:
                attributes={"id":child.id}
                node=SubElement(top,'created',attributes)
            else:
                attributes={"id":child.id}
                node=SubElement(top,'error',attributes)
                node.text=child.msg
        
        elif child.type=='position':
            if child.create:
                attributes={"sym":child.symbol,"id":child.account_id}
                node=SubElement(top,'created',attributes)
            else:
                attributes={"sym":child.symbol,"id":child.account_id}
                node=SubElement(top,'error',attributes)
                node.text=child.msg
    print(prettify(top))




##response of transaction
#transaction=Transaction_obj(11)
def transaction_response(transaction):
    top=Element('results')
    for child in transaction.sequence:
        if child.type=='order':
            if (child.open):
                attributes={"sym":child.sym, "amount":child.amount, "limit":child.limit, "id":child.id}
                node=SubElement(top,'opened',attributes)
            else:
                attributes={"sym":child.sym, "amount":child.amount, "limit":child.limit}
                node=SubElement(top,'error',attributes)
                node.text=child.msg
        
        if child.type=='query':
            # I want to get one Response object here according to child.id
            response=Response() # assumen this is the response object that I get
            node=SubElement(top,'status')
            for sub_resp in response.response:
                if sub_resp.status=="open":
                    attributes = {"shares": sub_resp.shares}
                    subnode=SubElement(node,'open',attributes)
                if sub_resp.status=="canceled":
                    attributes= {"shares": sub_resp.shares,"time": sub_resp.time}
                    subnode = SubElement(node, 'canceled', attributes)
                if sub_resp.status=="executed":
                    attributes = {"shares": sub_resp.shares,"price":sub_resp.price, "time": sub_resp.time}
                    subnode = SubElement(node, 'executed', attributes)
        if child.type=='cancel':
            # I want to get one Response object here according to child.id
            # After all the open orders with this child.id is canceled
            response = Response()  # assumen this is the response object that I get
            node = SubElement(top, 'canceled')
            for sub_resp in response.response:
                if sub_resp.status == "canceled":
                    attributes = {"shares": sub_resp.shares, "time": sub_resp.time}
                    subnode = SubElement(node, 'canceled', attributes)
                if sub_resp.status == "executed":
                    attributes = {"shares": sub_resp.shares, "price": sub_resp.price, "time": sub_resp.time}
                    subnode = SubElement(node, 'executed', attributes)

"""
create_response() test
"""
"""
account1=Account('1',1000)
account2=Account('2',2000)
account2.create=False
position1=Position('STOCK1','1',200)
position2=Position('STOCK2','2',300)
position2.create=False
create=Create_obj()
create.sequence.append(account1)
create.sequence.append(account2)
create.sequence.append(position1)
create.sequence.append(position2)
create_response(create)
"""



