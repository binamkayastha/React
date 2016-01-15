import sys, pygame, socket, select, string, sys
from math import sqrt
pygame.init()

#Generates a Rectangular GUI Class for Button
class Button:
    def __init__(self, x, y, width, height): #Constructor
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.draw()

    #Draws the button
    def draw(self):
        pygame.draw.rect(screen, (200, 200, 200), [self.x, self.y, self.width, self.height], 0)

    #Draws button with specified color
    def drawcolor(self, color):
        pygame.draw.rect(screen, color, [self.x, self.y, self.width, self.height], 0)

    #Checks whether the given mousex and mousey are inside the button
    def mouseInside(self, mousex, mousey): 
        if (self.x < mousex and mousex < (self.x + self.width) and self.y < mousey and mousey < (self.y + self.height)):
            return True;
        else:
            return False;

    def isClicked(self, mousex, mousey, ispressed, s):
        if self.mouseInside(mousex, mousey) and ispressed:
            print("You acted")
            s.send(str.encode("Enemy acted"))

#Generates a Circular GUI Class for Button
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
    #host = '130.215.225.166' #WPI Ip
    host = ''
    port = 5555

    #Created socket variable with default values.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #A 2 second timeout for blocking socket operations.
    s.settimeout(2)

    try:
        s.connect((host, port)) #Connect to host
    except:
        print("Unable to connect")
        sys.exit()

    print("Connected to game.")
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
            #Add closing connectin here.

        socket_list = [sys.stdin, s]
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
        for sock in read_sockets:
            #If data was sent.
            if sock == s:
                data = sock.recv(2048)
                #If no data was send ("Empty string")
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

                #Makes ispressed equal to true once every click.
                if pressed1: 
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
