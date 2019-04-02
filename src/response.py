#!/usr/bin/python3
from xml.etree.ElementTree import Element, SubElement
from ElementTree_pretty import prettify
from xml_parser_header import Create_obj,Account,Position, Order
from response_obj import Order_resp,TransactionResponse,TransactionSubResponse

##response of create
def create_response(create):#create=Create_obj()
    top=Element('results')
    for child in create.sequence:
        if child.type=='account':
            if child.created:
                attributes={"id":child.account_id}
                node=SubElement(top,'created',attributes)
            else:
                attributes={"id":child.account_id}
                node=SubElement(top,'error',attributes)
                node.text=child.msg
        
        elif child.type=='position':
            if child.created:
                attributes={"sym":child.symbol,"id":child.account_id}
                node=SubElement(top,'created',attributes)
            else:
                attributes={"sym":child.symbol,"id":child.account_id}
                node=SubElement(top,'error',attributes)
                node.text=child.msg
    print(prettify(top))




##response of transaction
#response
def transaction_response(response):
    top=Element('results')
    for child in response:
        if child.type=='order':
            if (child.open):
                attributes={"sym":child.sym, "amount":child.amount, "limit":child.limit, "id":child.id}
                node=SubElement(top,'opened',attributes)
            else:
                attributes={"sym":child.sym, "amount":child.amount, "limit":child.limit}
                node=SubElement(top,'error',attributes)
                node.text=child.msg
        if child.type=='transac':
            attributes={"id":child.trans_id}
            node
            if child.request=='query':
                node=SubElement(top,'status',attributes)
            if child.request=='cancel':
                node=SubElement(top,'canceled',attributes)
            for grand_child in child.trans_resp:
                if(grand_child.status=='open'):
                    sub_attributes = {"shares": grand_child.shares}
                    subnode = SubElement(node, 'open', sub_attributes)
                if(grand_child.status=='canceled'):
                    sub_attributes = {"shares": grand_child.shares, "time": grand_child.time}
                    subnode = SubElement(node, 'canceled', sub_attributes)
                if(grand_child.status=='executed'):
                    sub_attributes = {"shares": grand_child.shares, "price": grand_child.price, "time": grand_child.time}
                    subnode = SubElement(node, 'executed', sub_attributes)
    print(prettify(top))

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


"""
transaction_response() test
"""

"""
order1=Order('DUKE','3000','4000')
Order1=Order_resp(order1,True,'open','1')
order2=Order('UNC','300','400')
Order2=Order_resp(order2,False,'err','2')
trs1=TransactionSubResponse('open','300','300','300')
trs2=TransactionSubResponse('canceled','20','20','20')
trs3=TransactionSubResponse('executed','66','66','66')
tr1=TransactionResponse('1','query')
tr1.trans_resp.append(trs1)
tr1.trans_resp.append(trs2)
tr1.trans_resp.append(trs3)
tr2=TransactionResponse('2','cancel')
tr2.trans_resp.append(trs2)
tr2.trans_resp.append(trs3)
response=[]
response.append(Order1)
response.append(Order2)
response.append(tr1)
response.append(tr2)
transaction_response(response)
"""





