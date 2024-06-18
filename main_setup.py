#~~~ Imports ~~~
import pygame
import player
import trash
import sprite

#Initialize pygame program
pygame.init()

#~~~ Create Game Window ~~~
#Window Dimension variables
winWidth = 1000
winHeight = 600

#Initialize window 
win = pygame.display.set_mode((winWidth, winHeight))

#Create name of the window
pygame.display.set_caption("Our Game")

#~~~ Global Variables ~~~
char_x = 0 #winWidth * 0.5
char_y = 0 #winHeight * 0.65
char_s = 20
scale = 6
trashPile = []
trashHitboxes = []
collectPile = []

#Initialize the player
#(x, y, width, height, speed)
char_sheet = sprite.Sprite("NPC.png")
#Frame Number, X, Y, Width, Height, Scale
char_frame = char_sheet.getFrame(0, 0, 0, 32, 32, scale)
char_w = char_frame.get_width()
char_h = char_frame.get_height()
char = player.Player(char_x, char_y, char_w, char_h, char_s)
char.playerHitbox(scale)

#~~ Animations Variables ~~ 
animations = char_sheet.getAnimations()
previousTime = pygame.time.get_ticks()
frameSet = char_sheet.getFrameSet()
frameCoolDown = 250
currentSet = 0
currentFrame = 0

#Setup Window Boundaries based on player's hitbox
widthBoundary =  winWidth - char.hitbox[2] - char_s
heightBoundary = winHeight - char.hitbox[3]- char_s

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
        trashPile.append(trash.Trash(char.hitbox[2], char.hitbox[3], char_s, widthBoundary, heightBoundary))

    for i in trashPile:
        trashHitboxes.append(i.hitbox)

#Checks the collision between trash objects and the player
#When they collide, replace with a new trash object, which will change shape and spawn location
def collectTrash(player_hitbox):
    #Get the index of the trash object that been hit by the player's hitbox base on the trashHitboxes list.
    #Returns -1 if nothing been hit yet
    collectTrash = player_hitbox.collidelist(trashHitboxes)
    if collectTrash != -1:
        #Create a new trash object with proportions based on player's hitbox
        # playerWidth, playerHeight, playerSpeed, window width, window height
        newTrash = trash.Trash(char.hitbox[2], char.hitbox[3], char_s, widthBoundary, heightBoundary)
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
    win.blit(score_txt, (10, winHeight-50))

    #Load the player/Update player's movement
    char.playerHitbox(scale)
    # pygame.draw.rect(win, "red", char.hitbox)
    # win.blit(char_frame, (char.x, char.y))
     #Show frame
    win.blit(animations[currentSet][currentFrame], (char.x, char.y))

    #Check collision and update trash lists accordingly
    collectTrash(char.hitbox)

    #Update/Finalize all changes made
    pygame.display.flip()


#~~~ Main Loop ~~~
#Toggles the Running status of the game (on/off)
run = True
spawnTrash(5)
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
    currentSet = char.currentSet
    #Implement a way to add a walk right mode

    # oooooooooooooooooooooooooooooooooooooooooooooooooooooo
    # char_sheet.frameTiming(0, 0)
    # Get the current ingame time
    currentTime = pygame.time.get_ticks()
    
    #Check the duration between frames. If the frame cooldown is over, get the next frame and reset the cooldown
    if currentTime - previousTime >= frameCoolDown:
        currentFrame += 1
        previousTime = currentTime
    #When all frames are played, reset to the starting frame
    if currentFrame >= frameSet[currentSet]:
        currentFrame = 0
    
    #Update the window
    redrawGameWindow()

#When the game is off, close the pygame program as well.
pygame.quit()
