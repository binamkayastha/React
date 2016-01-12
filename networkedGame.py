import sys, pygame, socket, select, string, sys
pygame.init()

#Crerating GUI Class for Button
class Button:
    def __init__(self, x, y, width, height): #Constructor
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self): #Draws the button
        pygame.draw.rect(screen, (200, 200, 200), [self.x, self.y, self.width, self.height], 0)

    def drawcolor(self, color): #Draws button with specified color
        pygame.draw.rect(screen, color, [self.x, self.y, self.width, self.height], 0)

    def mouseInside(self, mousex, mousey): #Checks whether the given mousex and mousey are inside the button
        if (self.x < mousex and mousex < (self.x + self.width) and self.y < mousey and mousey < (self.y + self.height)):
            return True;
        else:
            return False;

if __name__ == "__main__":
    
    #Currently hardcoded to Binam's ip address, where server.py is run)
    host = '130.215.225.166'
    port = 5555

    #Created socket variable
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    
    try:
        s.connect((host, port)) #Connect to host (really should to try/except, but too lazy)
    except:
        print("Unable to connect")
        sys.exit()

    print("Connected to game. Waiting for server's okay")
    #Now that connection is up, run the screensetup


    #Set basic parts of pygame screen up
    size = width, height = 1000, 1000
    black = 0, 0, 0
    white = 255, 255, 255

    screen = pygame.display.set_mode(size)
    screen.fill(black)


    #Create the button variables
    buttonact = Button(0, 0, 200, 100)
    buttonreact = Button (width-200, 0, 200, 100)

    #Draw the buttons
    buttonact.draw()
    buttonreact.draw()
    pygame.display.update()

    #Set variables
    lastpressed = False
    ispressed = False    #Booleans to stop pressed1 being true all the time

    #Endless loop for which game goes on
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        socket_list = [sys.stdin, s]
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
        for sock in read_sockets:
            if sock == s:
                data = sock.recv(2048)
                if not data:
                    print("\nDisconnected from game")
                    sys.exit()
                else:
                    print(data.decode('utf-8'))
                    print("How do you respond")
            #Something else happens
            else:
                #Set the current variables of the mouse
                mousex, mousey = pygame.mouse.get_pos()
                pressed1= pygame.mouse.get_pressed()[0]
                if pressed1: #Makes ispressed an ONMOUSEDOWN/ONMOUSEUP event
                    if lastpressed:
                        ispressed = False
                    else:
                        ispressed = True
                    lastpressed = True
                else:
                    ispressed = False
                    lastpressed = False

                #Checks whether the buttons are being pressed
                if buttonact.mouseInside(mousex, mousey) and ispressed:
                    print("You acted")
                    s.send(str.encode("Enemy acted"))
                if buttonreact.mouseInside(mousex, mousey) and ispressed:
                    print("You reacted")
                    s.send(str.encode("Enemy reacted"))
                
                #Display the current status to the game
                pygame.display.update()
