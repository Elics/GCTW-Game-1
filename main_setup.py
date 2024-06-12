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

#Global Variables
char_x = 250 #winWidth * 0.5
char_y = 250 #winHeight * 0.65
char_w = 100
char_h = 100
char_s = 40
trashPile = []
trashHitboxes = []
collectPile = []

#Initialize the player
#(x, y, width, height, speed)
char = player.Player(char_x, char_y ,char_w, char_h, char_s)

#Setup Window Boundaries
widthBoundary = winWidth - char_w - char_s
heightBoundary = winHeight - char_h - char_s

#Create a list of trash objects and add their hitboxes in trashHitboxes
for i in range(5):
    trashPile.append(trash.Trash(char_w, char_h, char_s, widthBoundary, heightBoundary))

for i in trashPile:
    trashHitboxes.append(i.hitbox)

#~~~ Functions ~~~ 
#Checks the collision between trash object and the player
#When they collide, add the trash object to the collectPile, update the spawn location, and hide it
def collectTrash(player_hitbox):
    #Check if the hitboxes collide base on the trashHitboxes list/Return index of collided rectangle
    if pygame.Rect.collidelist(player_hitbox, trashHitboxes) != -1:
        #Get the index of the trash that has been hit
        collectTrash = player_hitbox.collidelist(trashHitboxes)

        #Remove the trash from the trashPile and add it to the collectPile
        collectPile.append(trashPile.pop(collectTrash))
        
        #Remove the old trash hitbox from the trashHitboxes
        trashHitboxes.pop(collectTrash)

#Update the game window with new animations/movement
def redrawGameWindow():
    #Load/Update Background
    win.fill("white")

    #Load trash that exists in trashPile
    for trash in trashPile:
        pygame.draw.rect(win, "red", trash.hitbox)

    #Load the player/Update player's movement
    char.playerHitbox()
    pygame.draw.rect(win, "black", char.hitbox)

    #Check collision and update trash lists accordingly
    collectTrash(char.hitbox)

    #Update/Finalize all changes made
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
