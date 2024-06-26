#~~~ Imports ~~~
import pygame
import player
import trash
import sprite
import level

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
char_s = 10 #Character Speed
scale = 6 #Scale of character
#Stores all the surfaces/trash sprites
trashPile = []
#Contains the rectangles of all the generated trash
trashHitboxes = []
#Holds all collected trash
collectPile = []
#Tracks score on each level
scoresList = []

#~~ Stage Timer ~~
#Initialize clock object to track time
clock = pygame.time.Clock()
#Choose the time limit for the stage
#Separate varible created for shop upgrade
baseTime = 10
stageCounter = baseTime
#Initialize the timer
stage_event = pygame.USEREVENT +1
#Updates the stage_event every 1000 miliseconds/1 second
pygame.time.set_timer(stage_event, 1000)
# In the main loop, update the counter 
# and print out the time until the timer ends at 0

#~~ Player Initialization ~~
#(x, y, width, height, speed)
#Add a sprite sheet to create the player
char_sheet = sprite.Sprite("NPC.png")
#Frame Number, X, Y, Width, Height, Scale
#Take a single frame from the sprite sheet to obtain dimensions
char_frame = char_sheet.getFrame(0, 0, 0, 32, 32, scale)
char_w = char_frame.get_width()
char_h = char_frame.get_height()
#Initialize the player
char = player.Player(char_x, char_y, char_w, char_h, char_s)
#Create player hitbox
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
# print(pygame.font.get_fonts())
# 1. First define the fonts, size, and boldness you want 
# 2. Then render the actual text, toggle anti-alias, and color
# 3. Finally, blit the rendered text in the redrawMethod
score_font = pygame.font.SysFont('Verdana', 30, True)
title_font = pygame.font.SysFont('Arial', 80, True)
subtitle_font = pygame.font.SysFont('Arial', 40, False, True)

#~~ Shop Features ~~
#Since all the variables are initialized above, the shop will be created below
upgradeIndex = 0
#A List of all Upgrades
 #Upgrades
    # char.speed += 10
    # baseTime += 10
upgradeList = [char.speed, baseTime]


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
    score = len(collectPile)
    score_txt = score_font.render("Collected: " + str(score), True, "black")
    stageCounter_txt = score_font.render(str(stageCounter), True, "black")
    win.blit(score_txt, (10, winHeight-50))
    win.blit(stageCounter_txt, (0,0))

    #Load the player/Update player's movement
    char.playerHitbox(scale)

    #Player Hitbox testing
    # pygame.draw.rect(win, "red", char.hitbox)
    # win.blit(char_frame, (char.x, char.y))

     #Show frame
    win.blit(animations[currentSet][currentFrame], (char.x, char.y))

    #Check collision and update trash lists accordingly
    collectTrash(char.hitbox)
   

    #Update/Finalize all changes made
    pygame.display.flip()
    
    return score

#~~~ Main Loop ~~~
#Toggles the Running status of the game (on/off)
run = True

#Spawn the initial set of trash in the map
spawnTrash(5)

#~~ Game Statuses ~~
#Initialize the game status and play the starting screen first
gameStatus = level.gameStatus("start")
#Initialize all the states
start = level.startGame(win, gameStatus, title_font, subtitle_font)
menu = level.menuScreen(win, gameStatus, title_font, subtitle_font)
end = level.gameEnd(win, gameStatus, title_font, subtitle_font)
shop = level.upgradeShop(win, gameStatus, title_font, subtitle_font, char.speed, baseTime)
level = level.runLevel(gameStatus)

#Add the states to the gameStates dictionary
gameStates = {"start":start, "menu":menu, "end":end, "shop":shop, "level":level}

while run:
    #Loading time for game
    pygame.time.delay(100)

    #Checks for any player interaction while running (mouse clicks, keyboard, etc.)
    for event in pygame.event.get():
        #Handle scenario when the player closes the window (X)
        if event.type == pygame.QUIT:
            run = False 
        #Check when the collection game mode has started, then toggle on the counter
        elif event.type == stage_event and gameStatus.getState() == "level":
            stageCounter -= 1
        #When the level ends, several changes will be made:
        # 1. Change to cutscene
        # 2. Add the player's score to the scoresList, and wipe out the current score (managed by the collecitonPile)
        # 3. Reset the counter (currently default to 10 seconds)
        if stageCounter == 0:
            stageCounter = baseTime
            gameStatus.setState("shop")
            scoresList.append(score)
            while len(collectPile) != 0:
                collectPile.pop()

    #Checks the current state. If it's a cutscene, then the variable
    #collecitonMode will be set to false, allowing the cutscene to play instead
    if gameStatus.getState() != "runLevel":
        level.collectionMode = False
    #Get the current gameStatus and check through the gameStates dictionary
    #When there is a match, run the given state
    gameStates[gameStatus.getState()].run()

    #Menu Screen Toggle
    if pygame.key.get_pressed()[pygame.K_m]:
        if gameStatus.getState() != "menu":
            gameStatus.setPreviousState()
            gameStatus.setState("menu")
        else:
            gameStatus.setState(gameStatus.getPreviousState())
        
    #Shop interface/Interaction
    #Get the index to the upgrade from the upgradeList
    if gameStatus.getState() == "shop":
        if pygame.key.get_pressed()[pygame.K_d]:
            upgradeIndex = 1
        elif pygame.key.get_pressed()[pygame.K_a]:
            upgradeIndex = 0
        #Highlights the corresponding selection made
        shop.selected = upgradeIndex

        #After confirming the index with SPACE, check if the current status is below 60
        #Then add the upgrade to the selected index
        #Update all stats and reset the timer base on the update made. Play level when choice is made
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if(upgradeList[upgradeIndex] < 60):
                upgradeList[upgradeIndex] = upgradeList[upgradeIndex] + 10
                char.speed = upgradeList[0]
                baseTime = upgradeList[1] 
                #Update the stageCounter and the speedBuff display
                stageCounter = baseTime
                shop.speedBuff = char.speed
                shop.timeBuff = baseTime
                pygame.time.delay(300)
                gameStatus.setState("level")

        #If Q is pressed, return the End Screen
        elif pygame.key.get_pressed()[pygame.K_q]:
            gameStatus.setState("end")
        
    #Runs Collection Mode: Collecting trash
    if level.collectionMode == True:
        #Get the user's input, specifically which keys they pressed
        #Then base on these keys, move the player around the map
        keys = pygame.key.get_pressed()
        char.movement(keys, widthBoundary, heightBoundary)
        currentSet = char.currentSet

        #~~ Running Animations in Main Loop ~~
        # Get the current ingame time
        currentTime = pygame.time.get_ticks()
        
        #Check the duration between frames. If the frame cooldown is over, get the next frame and reset the cooldown
        #Returns the currentFrame to run
        currentFrame = char_sheet.frameTiming(currentTime, previousTime, frameCoolDown, currentFrame, currentSet)[0]
        #Returns the time of the previous frame
        previousTime = char_sheet.frameTiming(currentTime, previousTime, frameCoolDown, currentFrame, currentSet)[1]

        #Update the window
        score = redrawGameWindow()

#When the game is off, close the pygame program as well.
pygame.quit()
