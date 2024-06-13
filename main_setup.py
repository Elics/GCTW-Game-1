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

#~~~ Global Variables ~~~
char_x = 350 #winWidth * 0.5
char_y = 350 #winHeight * 0.65
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

#~~~ Messages/Fonts ~~~
#Don't know what fonts you have? Run this line below
    #print(pygame.font.get_fonts())
# 1. First define the fonts, size, and boldness you want 
# 2. Then render the actual text, toggle anti-alias, and color
# 3. Finally, blit the rendered text in the redrawMethod
score_font = pygame.font.SysFont('Verdana', 30, True)

#~~~ Functions ~~~ 
#Create and add trash objects to trashPile. Additionally add their hitboxes to trashHitboxes
def spawnTrash(amount):
    for i in range(amount):
        trashPile.append(trash.Trash(char_w, char_h, char_s, widthBoundary, heightBoundary))

    for i in trashPile:
        trashHitboxes.append(i.hitbox)

#Checks the collision between trash objects and the player
#When they collide, replace with a new trash object, which will change shape and spawn location
def collectTrash(player_hitbox):
    #Get the index of the trash object that been hit by the player's hitbox base on the trashHitboxes list.
    #Returns -1 if nothing been hit yet
    collectTrash = player_hitbox.collidelist(trashHitboxes)
    if collectTrash != -1:
        #Create a new trash object 
        newTrash = trash.Trash(char_w, char_h, char_s, widthBoundary, heightBoundary)
        #Replace the current trash object with the new one
        trashPile[collectTrash] = newTrash
        
        #To track score, I currently have a list. 
        #Everytime a trash been collected, it will be tallied in this list
        #I need to find a way to replace this method, wastes resources
        collectPile.append(1)

        #Replace the old hitbox with the new hitbox
        trashHitboxes[collectTrash] = newTrash.hitbox


#Update the game window with new animations/movement
def redrawGameWindow():
    #Load/Update Background
    win.fill("white")

    #Load trash that exists in trashPile
    for trash in trashPile:
        pygame.draw.rect(win, "red", trash.hitbox)

    #Display the score
    score_txt = score_font.render("Collected: " + str(len(collectPile)), True, "black")
    win.blit(score_txt, (10, 450))

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
spawnTrash(2)
while run:
    #Loading time for game
    pygame.time.delay(100)

    #Checks for any player interaction while running (mouse clicks, keyboard, etc.)
    for event in pygame.event.get():
        #Handle scenario when the player closes the window (X)
        if event.type == pygame.QUIT:
            run = False
    
    #Get the user's input, specifically which keys they pressed
    #Then base on these keys, move the player around the map
    keys = pygame.key.get_pressed()
    char.movement(keys, widthBoundary, heightBoundary)
    
    #Update the window
    redrawGameWindow()

#When the game is off, close the pygame program as well.
pygame.quit()
