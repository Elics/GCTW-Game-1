#~~~ Imports ~~~
import pygame
import player
import trash
import sprite
import level
import window

#Initialize pygame program
pygame.init()

#Initialize window using windowDetails variable, which is a window class from window.py
win = level.tempWin

#~~ Player Initialization Variables ~~
#Player's Initial X & Y Coordinates
char_x = 0 
char_y = 0 
#Player's Initial Speed
char_s = 15
#Character Model Scale
scale = 6

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
#Add a sprite sheet to create the player
#File Name, Scale, Number of frames per animation, Total number of animations
char_sheet = sprite.Sprite("images\\characters\\tempPlayer.png", scale, [2, 2, 2, 4, 4, 4], 7)
#Take a single frame from the sprite sheet to obtain dimensions
#Frame Number, X, Y, Width, Height
char_frame = char_sheet.getFrame(0, 0, 0, 32, 32)
char_w = char_frame.get_width()
char_h = char_frame.get_height()
#Initialize the player using the single frame
#(x-coord, y-coord, width, height, speed)
char = player.Player(char_x, char_y, char_w, char_h, char_s)
#Initialize player's hitbox
char.playerHitbox(scale)

#~~ Animations Variables ~~
#Get a whole list of animations (walking, idle, etc.)
animations = char_sheet.getAnimations()
#For inverted animations (walking left)
#Number of frames, Index of the animation to copy, Index of the empty set to transfer the animation
animations = char_sheet.getInvertedAnimations(4, 4, 6)

#Scaled up character for dialogue
char_dialogue_sheet = sprite.Sprite("images\\characters\\tempPlayer.png", 10, [2, 2, 2, 4, 4, 4], 6)
dialogue_animations = char_dialogue_sheet.getAnimations()

#Track the time of the previous frame played
previousTime = pygame.time.get_ticks()
#Time between frames, FPS
frameCoolDown = 200
#Tracks the current animation being played
currentSet = 0
#Tracks the current frame of an animation being played
currentFrame = 0

#~~ Player Boundaries ~~
#Setup upper boundaries based on player's hitbox
widthBoundary =  win.winWidth - char.hitbox[2] - char_s
heightBoundary = win.winHeight - char.hitbox[3]- char_s

#~~~ Messages/Fonts ~~~
#Don't know what fonts you have? Run this line below
# print(pygame.font.get_fonts())
# 1. First define the fonts, size, and boldness you want 
# 2. Then render the actual text, toggle anti-alias, and color
# 3. Finally, blit the rendered text in the redrawMethod
score_font = pygame.font.SysFont('Verdana', 30, True)
title_font = pygame.font.SysFont('Arial', 80, True)
subtitle_font = pygame.font.SysFont('Arial', 40, False)
instruction_font = pygame.font.SysFont('Arial', 20, False)
name_font = pygame.font.SysFont('Nunito', 40, True)
menu_font = pygame.font.SysFont('Verdana', 80, False)

#~~ Shop Features ~~
#Index to loop through available upgrades
upgradeIndex = 0
#Tracks the player's coins
coinPouch = 0
#A List of all Upgrades
 #Upgrades
    # char.speed += 10
    # baseTime += 10
upgradeList = [char.speed, baseTime]

#~~ Level Features ~~
#A list of levels and the minimum collection goal
levelsList = {
    0:2,
    1:[5]
    }
#Indicate the current level
currentLevel = 1
#Stores all the surfaces/trash sprites
trashPile = []
#Contains the rectangles of all the generated trash
trashHitboxes = []
#Holds all collected trash
collectPile = 0
#Tracks score on each level
scoresList = []
scoreIndex = 0
#Allow trash to spawn on the map
spawnTrashToggle = True
trashSpawnRate = 5

#~~~ Functions ~~~ 
#Create and add trash objects to trashPile. Additionally add their hitboxes to trashHitboxes
#After trash is spawn, it will stop spawning new boxes until the level timer reaches 0
def spawnTrash(amount, widthLowerBoundary, widthUpperBoundary, heightLowerBoundary, heightUpperBoundary):
    global spawnTrashToggle
    #Check if the trash can spawn
    if spawnTrashToggle == True:
        #Initialize Trash objects and add to trashPile list
        for i in range(amount):
            trashPile.append(trash.Trash(char.hitbox[2], char.hitbox[3], widthLowerBoundary, widthUpperBoundary, heightLowerBoundary, heightUpperBoundary))

        #Add Trash hitboxes to the trashHitboxes list. This is essential for player/trash collision
        #A separate list is needed as the collidelist() method only takes a list of rectangles.
        for i in trashPile:
            trashHitboxes.append(i.hitbox)
    #Finishes spawning a set number of boxes
    spawnTrashToggle = False

def clearTrash():
    for i in range(len(trashPile)):
        trashPile.pop()

    for j in range(len(trashHitboxes)):
        trashHitboxes.pop()

#Checks the collision between trash objects and the player
#When they collide, replace with a new trash object, which will change shape and spawn location
def collectTrash(player_hitbox, widthLowerBoundary, widthUpperBoundary, heightLowerBoundary, heightUpperBoundary):
    #Get the index of the trash object that been hit by the player's hitbox base on the trashHitboxes list.
    #Returns -1 if nothing been hit yet
    collectTrash = player_hitbox.collidelist(trashHitboxes)
    if collectTrash != -1:
        #Create a new trash object with proportions based on player's hitbox
        # playerWidth, playerHeight, playerSpeed, window width, window height
        newTrash = trash.Trash(char.hitbox[2], char.hitbox[3], widthLowerBoundary, widthUpperBoundary, heightLowerBoundary, heightUpperBoundary)
        
        #NOTE: To track score, I currently have a list. 
        #Everytime a trash been collected, it will be tallied in this list
        #I need to find a way to replace this method, wastes resources
        global coinPouch
        global collectPile
        if trashPile[collectTrash].treasure == 1:
        #If trash has treasure attribute: 10+ Coins, 5+ Points
            coinPouch = coinPouch + 10
            collectPile = collectPile + 5
        else:
        #Normal Trash: 2+ Coints, 1+ Points
            coinPouch = coinPouch + 2
            collectPile = collectPile + 1


        #Replace the current trash object with the new one
        trashPile[collectTrash] = newTrash

        #Replace the old hitbox with the new hitbox
        trashHitboxes[collectTrash] = newTrash.hitbox

#Update the game window with new animations/movement
#Parameters: Current Level and 4 Boundaries adjustments to define the trash spawn areas 
#Returns the number of coins earned by the end of the level
def redrawGameWindow(widthLowerBoundary, widthUpperBoundary, heightLowerBoundary, heightUpperBoundary):
    #Draw the trash that exists in trashPile
    for trash in trashPile:
        if trash.treasure == 1:
            pygame.draw.rect(win.currentWindow, "blue", trash.hitbox)
        else:    
            win.currentWindow.blit(trash.image, (trash.x, trash.y))

    #Display score
    score_txt = score_font.render("Collected: " + str(collectPile), True, "black")
    win.addUI(score_txt, (750, 0))

    #Display timer
    stageCounter_txt = score_font.render(str(stageCounter), True, "black")
    win.addUI(stageCounter_txt, (0,0))

    #Display coins
    coin_txt = score_font.render("Coins: " + str(coinPouch), True, "black")
    win.addUI(coin_txt, (400, 0))

    #Load the player/Update player's movement
    char.playerHitbox(scale)

    #Player Hitbox testing
    # pygame.draw.rect(win.currentWindow, "red", char.hitbox)
    # win.currentWindow.blit(char_frame, (char.x, char.y))

    #Show frame
    win.currentWindow.blit(animations[currentSet][currentFrame], (char.x, char.y))

    #Check collision and update trash lists accordingly
    collectTrash(char.hitbox, widthLowerBoundary, widthUpperBoundary, heightLowerBoundary, heightUpperBoundary) 

    #Update/Finalize all changes made
    pygame.display.flip()

#~~~ Main Loop ~~~
#Toggles the Running status of the game (on/off)
run = True

# #Spawn the initial set of trash in the map
# #Spawn Location Dimensions (estimated): X:15-950; Y:200-550
# spawnTrash(5, char.speed, widthBoundary, win.backgroundList[3][1], heightBoundary)
 
#~~ Game Statuses ~~
#Initialize the game status class and play the starting screen first
#I place this here to access the windowDetails variable, which is used to display backgrounds in level.py
gameStatus = level.gameStatus("runLevel")

#Initialize all the states
#NOTE: Fonts are placed in a list
start = level.startGame(gameStatus)
menu = level.menuScreen(gameStatus, [menu_font])
end = level.gameEnd(gameStatus)
shop = level.upgradeShop(gameStatus, char.speed, baseTime, 0, [score_font])
runLevel = level.runLevel(gameStatus, char)
selectLevel = level.selectLevel(gameStatus, [subtitle_font])
levelComplete = level.levelComplete(gameStatus, char)

#All Cutscenes
playPrologue = level.prologue(gameStatus, [name_font, instruction_font], animations, dialogue_animations, char, char_sheet, scale, (widthBoundary, heightBoundary))
sceneOne = level.sceneOne(gameStatus, [name_font, instruction_font], animations, dialogue_animations, char, char_sheet, scale, (widthBoundary, heightBoundary))
tutorial = level.tutorial(gameStatus, [name_font, instruction_font], animations, dialogue_animations, char, char_sheet, scale, (widthBoundary, heightBoundary))


#Add the states to the gameStates dictionary
#This allows the gameStatus class to know which state to call
gameStates = {"start":start, "menu":menu, "end":end, "shop":shop, "runLevel":runLevel, "selectLevel":selectLevel,"levelComplete":levelComplete, "sceneOne":sceneOne, "playPrologue":playPrologue, "tutorial":tutorial} 

while run:
    #Loading time for game
    pygame.time.delay(100)

    #Checks for any player interaction while running (mouse clicks, keyboard, etc.)
    for event in pygame.event.get():
        #Handle scenario when the player closes the window (X)
        if event.type == pygame.QUIT:
            run = False 
        #Check when the collection game mode has started, then toggle on the counter
        elif event.type == stage_event and gameStatus.getState() == "runLevel" and currentLevel != 0:
            stageCounter -= 1
        #When the level ends, several changes will be made:
            # 1. Change to Shop state
            # 2. Add the player's score to the scoresList, and wipe out the current score (managed by the collecitonPile)
            # 3. Reset the counter (currently default to 10 seconds)
        if stageCounter == 0:
            currentLevel = 1 
            clearTrash()
            stageCounter = baseTime
            gameStatus.setState("shop")
            scoresList.append(collectPile)
            collectPile = 0
            spawnTrashToggle = True

            #Modify the trashSpawnRate base on player performance
            if scoresList[len(scoresList) - 1] >= levelsList.get(1)[scoreIndex]:
                trashSpawnRate = 2
            elif scoresList[len(scoresList) - 1] < levelsList.get(1)[scoreIndex]:
                trashSpawnRate = 10
            else:
                trashSpawnRate = 5

    #Get the current gameStatus and check through the gameStates dictionary
    #When there is a match, run the given state
    gameStates[gameStatus.getState()].run()
    
    #Menu Screen Toggle
    if pygame.key.get_pressed()[pygame.K_m]:
        pygame.time.delay(200)
        #When opening the menu, track the previous state and then change to menu state
        if gameStatus.getState() != "menu":
            gameStatus.setPreviousState()
            gameStatus.setState("menu")
        else:
            #When closing the Menu, updates the game boundaries according to the screen size
            widthBoundary =  menu.width - char.hitbox[2] - char_s
            heightBoundary = menu.height - char.hitbox[3]- char_s

            #Clear the current set of trash
            clearTrash()
            #Respawn trash base on the window size
            spawnTrashToggle = True
            spawnTrash(5, char.speed, widthBoundary, win.backgroundList[3][1], heightBoundary)

            #Return to the previous state
            gameStatus.setState(gameStatus.getPreviousState())
    #If Q is pressed, return the End Screen
    if gameStatus.getState() == "menu":
        if pygame.key.get_pressed()[pygame.K_q]: 
            gameStatus.setState("end")
        
        
    #~~ Shop Interface ~~
    #Get the index to the upgrade from the upgradeList
    if gameStatus.getState() == "shop":
        #Update the coin display
        shop.coins = coinPouch

        #Check which selection the player has made
        if pygame.key.get_pressed()[pygame.K_d] and upgradeIndex < 2:
            pygame.time.delay(100)
            upgradeIndex += 1
        elif pygame.key.get_pressed()[pygame.K_a] and upgradeIndex > 0:
            pygame.time.delay(100)
            upgradeIndex -= 1
        
        #Highlights the corresponding selection made
        shop.selected = upgradeIndex
        #Updates the price depending which index is 
        if upgradeIndex < 2:
            shop.price = 10*int(upgradeList[upgradeIndex] / 10)

        #After confirming the index with SPACE, check if the current status is below 60
        #Then add the upgrade to the selected index
        #Update all stats and reset the timer base on the update made.
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            #Plays the level after buying/skipping upgrade
            if upgradeIndex == 2:
                pygame.time.delay(300)
                gameStatus.setState("runLevel")

            #Player buys an upgrade and checks if they have enough coins to do so
            elif upgradeList[upgradeIndex] < 60 and coinPouch > 0:
                #Collect the coins
                if int(upgradeList[upgradeIndex] / 10)*10 <= coinPouch:
                    coinPouch = coinPouch - 10*int(upgradeList[upgradeIndex] / 10)
                    #Update coinPouch/display
                    shop.coins = coinPouch
                    #Increase corresponding upgrade by 10 on the upgradeList
                    upgradeList[upgradeIndex] = upgradeList[upgradeIndex] + 10
                    #Update the corresponding variables base on the values in the upgradeList
                    char.speed = upgradeList[0]
                    baseTime = upgradeList[1] 
                    #Update the stageCounter and the buff displays
                    stageCounter = baseTime
                    shop.speedBuff = char.speed
                    shop.timeBuff = baseTime  
                    

                #If the player does not have enough coins for the upgrade
                else:
                    lessCoins_txt = subtitle_font.render("Not enough coins for next upgrade level!", True, "blue")
                    win.addUI(lessCoins_txt, (240, 450)), (0, 0)
                    pygame.display.flip()
                    pygame.time.delay(500)

            #If the player reached max upgrade on any item
            elif upgradeList[upgradeIndex] >= 60:
                maxUpgradeReach_txt = subtitle_font.render("Max Upgrade Reached!", True, "blue")
                win.addUI(maxUpgradeReach_txt, (330, 450)), (0,0)
                pygame.display.flip()
                pygame.time.delay(500)

            #If the player has 0 coins 
            else:
                #Testing Scale with dummy surface
                noCoins_txt = subtitle_font.render("You have no coins!", True, "blue")
                win.addUI(noCoins_txt, (350, 450)), (0, 0)

                # win.currentWindow.blit(noCoins_txt, (int(win.winWidth*0.35), int(win.winHeight*0.75)))
                pygame.display.flip()
                pygame.time.delay(500)
        
    #~~ Collection Mode: Collect Trash ~~
    if gameStatus.getState() == "runLevel":
        #Get the proper background from level.py by updating the current level
        runLevel.levelNumber = currentLevel
        #Set up background bounds based on the current level
        if currentLevel == 0: 
            #Tutorial
            w_lowBounds = char.speed
            h_lowbounds = char.speed
            spawnTrash(1, char.speed, widthBoundary, char.speed, heightBoundary)

            #When the player collects 2 trash, end the level and reset everything
            if(levelsList.get(0) <= collectPile):
                collectPile = 0
                coinPouch = 0
                stageCounter = 0

        elif currentLevel == 1: 
            #Level One
            w_lowBounds = char.speed
            h_lowbounds = win.backgroundList[3][1]
            #After the round ends, check the player's score and change the spawn rate base on that score
            spawnTrash(trashSpawnRate, char.speed, widthBoundary, win.backgroundList[3][1], heightBoundary)

        else: 
            #Default bounds if the level does not have specific bounds
            w_lowBounds = char.speed
            h_lowbounds = char.speed
            spawnTrash(5, char.speed, widthBoundary, char.speed, heightBoundary)

        #Get the user's input, specifically which keys they pressed
        #Then base on these keys, move the player around the map
        keys = pygame.key.get_pressed()
        char.movement(keys, w_lowBounds, widthBoundary, h_lowbounds, heightBoundary)
        #Return the current animation set that the player toggled based on the movement method
        currentSet = char.currentSet

        #~~ Running Animations in Main Loop ~~
        # Get the current ingame time
        currentTime = pygame.time.get_ticks()
        
        #Check the duration between frames. If the frame cooldown is over, get the next frame and reset the cooldown
        #Returns the currentFrame to run
        currentFrame = char_sheet.frameTiming(currentTime, previousTime, frameCoolDown, currentFrame, currentSet)[0]
        #Returns the time of the previous frame
        previousTime = char_sheet.frameTiming(currentTime, previousTime, frameCoolDown, currentFrame, currentSet)[1]

        #Update the window and return the score and coin list
        redrawGameWindow(w_lowBounds, widthBoundary, h_lowbounds, heightBoundary)

        #Update Shop Coin Display
        shop.coins = coinPouch

#When the game is off, close the pygame program as well.
pygame.quit()

#NOTE: Next Goal, work on tutorial and first cutscene 
