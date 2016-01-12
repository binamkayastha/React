import sys, pygame
pygame.init()

size = width, height = 1000, 1000
speed = [1, 1]
black = 0, 0, 0
white = 255, 255, 255

screen = pygame.display.set_mode(size)
screen.fill(black)


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

#Create the button variables
buttonact = Button(0, 0, 200, 100)
buttonreact = Button (width-200, 0, 200, 100)

#Draw the buttons
buttonact.draw()
buttonreact.draw()

#Set variables
lastpressed = False
ispressed = False    #Booleans to stop pressed1 being true all the time

#Endless loop for which game goes on
while 1:
    #Not exactly sure what this is supposed to do, apparenlty healthy for application
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
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
    if buttonreact.mouseInside(mousex, mousey) and ispressed:
        print("You reacted")
    
    #Display the current status to the game
    pygame.display.update()
