#~~~ Imports ~~~
import pygame
import player
import trash

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
#(x, y, width, height, speed)
char = player.Player(50, 250, 100, 100, 40)

#Global Variables
char_x = char.x
char_y = char.y
char_w = char.width
char_h = char.height
char_s = char.speed

#Setup Window Boundaries
widthBoundary = winWidth - char_w - char_s
heightBoundary = winHeight - char_h - char_s

#Initialize trash sprites
trash = trash.Trash(char_w, char_h, char_s, widthBoundary, heightBoundary)

#~~~ Functions ~~~ 
def redrawGameWindow():
    #Load/Update Background
    win.fill("white")

    #Draw trash
    # trash.trashHitbox()
    # pygame.draw.rect(win, "red", trash.hitbox)

    #Draw the player
    char.playerHitbox()
    pygame.draw.rect(win, "black", char.hitbox)

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
