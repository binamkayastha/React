import sys, pygame, socket, select, string, sys
from math import sqrt
pygame.init()

#Crerating GUI Class for Button
class Button:
    def __init__(self, x, y, width, height): #Constructor
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.draw()

    def draw(self): #Draws the button
        pygame.draw.rect(screen, (200, 200, 200), [self.x, self.y, self.width, self.height], 0)

    def drawcolor(self, color): #Draws button with specified color
        pygame.draw.rect(screen, color, [self.x, self.y, self.width, self.height], 0)

    def mouseInside(self, mousex, mousey): #Checks whether the given mousex and mousey are inside the button
        if (self.x < mousex and mousex < (self.x + self.width) and self.y < mousey and mousey < (self.y + self.height)):
            return True;
        else:
            return False;
    
    def isClicked(self, mousex, mousey, ispressed, s):
        if self.mouseInside(mousex, mousey) and ispressed:
            print("You acted")
            s.send(str.encode("Enemy acted"))


class ButtonC:
    def __init__(self, name, x, y, r): #Constructor
        self.name = name
        self.x = x
        self.y = y
        self.r = r
        self.draw()
    
    def draw(self):
        pygame.draw.circle(screen, (175, 175, 175), (self.x, self.y), self.r, 0)
    
    def mouseInside(self, mousex, mousey):
        #distance between mousex mousey and self.x and self.y is less than radius
        if(sqrt((mousex - self.x)**2 + (mousey - self.y)**2) < self.r):
            return True
        else:
            return False

    def isClicked(self, mousex, mousey, ispressed, s):
        if self.mouseInside(mousex, mousey) and ispressed:
            print("You " + self.name)
            s.send(str.encode(self.name))



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
    '''
    btnPunch = Button(40, 625, 200, 150)
    btnGrab = Button(40, 750, 200, 150) 
    btnDash = Button(280, 625, 200, 150)
    btnCharge = Button(280, 750, 200, 150)
    '''
    btnPunch = ButtonC("punch", 115, 625, 55)
    btnGrab = ButtonC("grab", 115, 750, 55) 
    btnDash = ButtonC("dash", 355, 625, 55)
    btnCharge = ButtonC("charge", 355, 750, 55)
    btnBlock = ButtonC("block", 480, 625, 55)
    btnDodge = ButtonC("dodge", 480, 750, 55)


    #Draw the buttons
    #buttonact.draw()
    #buttonreact.draw()
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
                buttonact.isClicked(mousex, mousey, ispressed, s)
                buttonreact.isClicked(mousex, mousey, ispressed, s)
                btnPunch.isClicked(mousex, mousey, ispressed, s)
                btnGrab.isClicked(mousex, mousey, ispressed, s)
                btnDash.isClicked(mousex, mousey, ispressed, s)
                btnCharge.isClicked(mousex, mousey, ispressed, s)
                btnBlock.isClicked(mousex, mousey, ispressed, s)
                btnDodge.isClicked(mousex, mousey, ispressed, s)

                #Display the current status to the game
                pygame.display.update()
