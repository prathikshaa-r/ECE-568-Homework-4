#!/usr/bin/python3
#socket_echo_server.py                                                                                           
import socket
import sys
import threading

from xml_parser_header import parse_xml
from database_connect import *
from database_setup import *


def recvall(sock,total_msg_len):
    msg = b''
    while(len(msg)) < total_msg_len:
        part = sock.recv(total_msg_len-len(msg))
        if part == b'':
            #raise RuntimeError("recv: socket connection closed")                                                            
            break
        msg = msg + part
        pass
    return msg
pass

order_id=1

def process_request(connection, client_address):
    try:
        print('connection from', client_address)
        # Receive the data in small chunks and retransmit it
        length=recvall(connection,28)
        recv_string=recvall(connection,int.from_bytes(length, byteorder='big'))
        obj=parse_xml(recv_string,order_id)
        # for sub in obj.sequence:
        #     if sub.type=='account':
        #         obj = create_account(connect(),sub)
        #         print(obj)
        #         print("Error:")
        #         print(obj.err)
        #     if sub.type=='position':
        #         obj = create_position(connect(),sub)
        #         print(obj)
        #         print("Error:")
        #         print(obj.err)
        for sub in obj.sequence:
            if sub.type=='account':
                new_obj = create_account(connect(),sub)
                print(new_obj)
                print("Error:")
                print(new_obj.err)
            if sub.type=='position':
                new_obj = create_position(connect(),sub)
                print(new_obj)
                print("Error:")
                print(new_obj.err)
            if sub.type=='order':
                new_obj= create_order(connect(),sub,obj.account_id)
                print(new_obj)
                print("Error:")
                print(new_obj.err)


    finally:
        # Clean up the connection
        connection.close()



# Create a TCP/IP socket                                                                                         
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port                                                                                    
server_address = (socket.gethostname(), 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections                                                                                
sock.listen(1)

while True:
    # Wait for a connection                                                                                      
    print('waiting for a connection')
    connection, client_address = sock.accept()
    t=threading.Thread(target=process_request(connection,client_address))
    t.start()
