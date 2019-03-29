#socket_echo_server.py                                                                                           
import socket
import sys
sys.path.append('../parser')
from xml_parser_header import parse_xml

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
    try:
        print('connection from', client_address)
        # Receive the data in small chunks and retransmit it
        recv_string=""
        while True:
            data = connection.recv(1024)
            if data:
                """                                                                                          
                print('sending data back to the client')                                                     
                connection.sendall(data)                                                                     
                """
            else:
                break
            recv_string+=data.decode("utf-8")
        parse_xml(recv_string)
    finally:
        # Clean up the connection
        connection.close()