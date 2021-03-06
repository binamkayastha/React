import socket
import sys
import select
from _thread import *

def broadcast_data (sock, message):
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock:
            try:
                socket.send(str.encode(message))
            except:
                #broken socket connection
                print("Connection to socket: " + str(socket) + " lost")
                socket.close()
                CONNECTION_LIST.remove(socket)


if __name__ == "__main__":
    CONNECTION_LIST = []
    RECV_BUFFER = 2048
    HOST = ''
    PORT = 5555

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    #Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)

    print ("Chat server stared on port " + str(PORT))

    while 1:
        #Get the list of sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST, [], [])

        for sock in read_sockets:
            #New connection
            if sock == server_socket:
                #Handle the case in which there is a new connectionn recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd) #add to list
                print("Client connected")
                
                broadcast_data(sockfd, "Client entered room \n")

            #Some incoming message from a client
            else:
                #Data recieved from client, process it
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data.decode('utf-8'))
#                        sock.sendall(str(
                except socket.error as e:
                    print(str(e))
                    broadcast_data(sock, "Client is offline")
                    print ("Client is offline")
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
    server_socket.close()
