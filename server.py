import socket
import sys
import select
from _thread import *

#Sends a message to sockets other than the given argument or the server.
def broadcast_data (sock, message):
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock:
            try:
                #send message
                socket.send(str.encode(message))
            except:
                #If there is an error, assume broken socket connection, and close the socket and remove it from the lsit
                print("Connection to socket: " + str(socket) + " lost")
                socket.close()
                CONNECTION_LIST.remove(socket)


if __name__ == "__main__":
    numOfPlayers = 2        #The number of players allowed to connect in the game.
    CONNECTION_LIST = []    #The array where all the sockets connected are stored
    RECV_BUFFER = 2048
    HOST = ''               #Host of server socket
    PORT = 5555             #Port of server socket.

    #Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    #Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)

    print ("Game server stared on port " + str(PORT))

    while 1:
        #"All soccets in the readable list have incoming data buffered and avaliable to read" https://pymotw.com/2/select/
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST, [], [])

        for sock in read_sockets:
            #If there is a new connection
            if sock == server_socket:
                if numOfPlayers <= 0:
                    print("Third player attempted connect, disallowed")
                    sockfd, addr = server_socket.accept()
                    sockfd.close()
                else:
                    numOfPlayers = numOfPlayers - 1
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
                    #If statement is false if, data recieve is equal to 0 or is an empty string.
                    if data:
                        broadcast_data(sock, data.decode('utf-8'))
                except socket.error as e:
                    print(str(e))
                    broadcast_data(sock, "Client is offline")
                    print ("Client is offline")
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
    server_socket.close()
