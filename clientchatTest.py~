import socket, select, string, sys

def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()

if __name__ == "__main__":
    if(len(sys.argv) < 3):
        print ("Usage: python telnet.py hostname port")
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    try:
        s.connect((host, port))
    except:
        print ("unable to connect")
        sys.exit()

    print ("connected to remote host. Start sending messages")
    prompt()

    while 1:
        socket_list = [sys.stdin, s]

        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

        for sock in read_sockets:
            if sock == s:
                data = sock.recv(2048)
                if not data:
                    print ("\nDisconnected from chat server")
                    sys.exit()
                else:
                    print(data.decode('utf-8'))
                    prompt()
            #User entered a message
            else:
                msg = input()
                s.send(str.encode(msg + '\n'))
                prompt()
