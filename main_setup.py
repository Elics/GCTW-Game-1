#~~~ Imports ~~~
import pygame
import player

#Initialize pygame program
pygame.init()

#~~~ Create Game Window ~~~
#Window Dimension variables
winWidth = 500
winHeight = 500

#Initialize window 
win = pygame.display.set_mode((winWidth, winHeight))

#Create name of the window
pygame.display.set_caption("Our Game")

#Initialize the player
char = player.Player(50, 250, 24, 24, 10)


#Setup Window Boundaries
widthBoundary = winWidth - char.width - char.speed
heightBoundary = winHeight - char.height - char.speed

#~~~ Functions ~~~ 
def redrawGameWindow():
    #Load/Update Background
    win.fill("white")

    #Draw the player
    hitbox = pygame.Rect(char.x, char.y, char.width, char.height)
    pygame.draw.rect(win, "black", hitbox)

    #Update any changes
    pygame.display.flip()


#~~~ Main Loop ~~~
#Toggles the Running status of the game (on/off)
run = True
while run:
    #Loading time for game
    pygame.time.delay(100)

    #Checks for any player interaction while running (mouse clicks, keyboard, etc.)
    for event in pygame.event.get():
        #Handle scenario when the player closes the window (X)
        if event.type == pygame.QUIT:
            run = False
        
    keys = pygame.key.get_pressed()
    char.movement(keys, widthBoundary, heightBoundary)
    
    #Update the window
    redrawGameWindow()

#When the game is off, close the pygame program as well.
pygame.quit()
