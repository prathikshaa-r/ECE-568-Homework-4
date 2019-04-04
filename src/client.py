#socket_echo_client.py
import socket
import sys
import os

import random, string, time
from xml.etree.ElementTree import Element, SubElement
from ElementTree_pretty import prettify

test=[]

def test1():
    top = Element('create')
    attributes1 = {"id":'1', "balance":'2000'}
    SubElement(top, 'account', attributes1)
    attributes2 = {"id": '2', "balance": '3000'}
    SubElement(top, 'account', attributes2)
    attributes3 = {"id": '3', "balance": '3000'}
    SubElement(top, 'account', attributes3)

    attributes4 = {"sym":"A"}
    node = SubElement(top, 'symbol', attributes4)
    attributes5 = {"id": '1'}
    node1 = SubElement(node, 'account', attributes5)
    node1.text = '1000'

    attributes6 = {"sym": "B"}
    node = SubElement(top, 'symbol', attributes6)
    attributes7 = {"id": '2'}
    node1 = SubElement(node, 'account', attributes7)
    node1.text = '1000'

    attributes8 = {"sym": "C"}
    node = SubElement(top, 'symbol', attributes8)
    attributes9 = {"id": '3'}
    node1 = SubElement(node, 'account', attributes9)
    node1.text = '1000'
    return prettify(top)



def test2():
    top = Element('transactions')
    attributes1 = {'id': '1'}
    top.attrib = attributes1
    attributes2 = {'sym': 'A', 'amount': '-30','limit': '100'}
    SubElement(top, 'order', attributes2)
    return prettify(top)

def test3():
    top = Element('transactions')
    attributes1 = {'id': '2'}
    top.attrib = attributes1
    attributes2 = {'sym': 'B', 'amount': '40','limit': '100'}
    SubElement(top, 'order', attributes2)
    return prettify(top)

def test4():
    top = Element('transactions')
    attributes1 = {'id': '3'}
    top.attrib = attributes1
    attributes2 = {'sym': 'C', 'amount': '30','limit': '100'}
    SubElement(top, 'order', attributes2)
    return prettify(top)

def test5():
    top = Element('transactions')
    attributes1 = {'id': '1'}
    top.attrib = attributes1
    attributes2 = {'id': '1'}
    SubElement(top, 'query', attributes2)
    return prettify(top)

def test6():
    top = Element('transactions')
    attributes1 = {'id': '2'}
    top.attrib = attributes1
    attributes2 = {'id': '2'}
    SubElement(top, 'query', attributes2)
    return prettify(top)

def test7():
    top = Element('transactions')
    attributes1 = {'id': '3'}
    top.attrib = attributes1
    attributes2 = {'id': '3'}
    SubElement(top, 'query', attributes2)
    return prettify(top)




def randomword(length):
   letters = string.ascii_uppercase
   return ''.join(random.choice(letters) for i in range(length))

def create_request():
    top=Element('create')
    attributes1={"id":str(random.randint(1,10001)),"balance":str(random.randint(1,10001))}
    SubElement(top, 'account', attributes1)
    attributes2={"sym":randomword(3)}
    node=SubElement(top,'symbol',attributes2)
    attributes3={"id":str(random.randint(1,10001))}
    node1=SubElement(node,'account',attributes3)
    node1.text=str(random.randint(1,10001))
    return prettify(top)

def transaction_request():
    top=Element('transactions')
    attributes1={'id':str(random.randint(1,10001))}
    top.attrib=attributes1
    attributes2={'sym':randomword(3),'amount':str(random.randint(-10000,10001)),'limit':str(random.randint(1,10001))}
    SubElement(top,'order',attributes2)
    attributes3={'id':str(random.randint(1,10001))}
    SubElement(top,'query',attributes3)
    attributes4={'id':str(random.randint(1,10001))}
    SubElement(top,'cancel',attributes4)
    return prettify(top)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('vcm-8454.vm.duke.edu', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

# try:

    # Send data
    #message = b'This is the message.  It will be repeated.'
    #print('sending {!r}'.format(message))

# filename = 'create.xml'
# length=os.path.getsize(filename)
# sock.send(length.to_bytes(28,'big'))
# f = open(filename, 'rb')
# l = f.read(1024)
# while(l):
#     sock.send(l)
#     l = f.read(1024)
# f.close()
# sent=transaction_request()
# #sent=create_request()
# test=[]
# test.append(test1())
# test.append(test2())
# test.append(test3())
# test.append(test4())
# test.append(test5())
# test.append(test6())
# test.append(test7())

sent=test1()
length=len(sent)
sock.send(length.to_bytes(28,'big'))
sock.send(sent.encode())
time.sleep(1)



print(sock.recv(2048))


# finally:
#     print('closing socket')
#     sock.close()
