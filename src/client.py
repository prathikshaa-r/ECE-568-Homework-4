#socket_echo_client.py
import socket
import sys
import os

import random, string
from xml.etree.ElementTree import Element, SubElement
from ElementTree_pretty import prettify

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
    # attributes3={'id':str(random.randint(1,10001))}
    # SubElement(top,'query',attributes3)
    # attributes4={'id':str(random.randint(1,10001))}
    # SubElement(top,'cancel',attributes4)
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
sent=transaction_request()
length=len(sent)
sock.send(length.to_bytes(28,'big'))
sock.send(sent.encode())
print(sock.recv(2048))


# finally:
#     print('closing socket')
#     sock.close()
