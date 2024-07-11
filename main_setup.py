#~~~ Imports ~~~
import pygame
import player
import trash
import sprite
import level
import window

#Initialize pygame program
pygame.init()

#Initialize window and set name of the window
win = window.Window("Our Earth")
#Add backgrounds for the LEVELS
win.addBackground("images\\backgrounds\\Beach.png", 200)

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
# dialogue_font = pygame.font.SysFont('')

#~~ Shop Features ~~
#Index to loop through available upgrades
upgradeIndex = 0
#A list to store all coin values collected
coinsList = [10]
#A List of all Upgrades
 #Upgrades
    # char.speed += 10
    # baseTime += 10
upgradeList = [char.speed, baseTime]

#~~ Level Features ~~
#Stores all the surfaces/trash sprites
trashPile = []
#Contains the rectangles of all the generated trash
trashHitboxes = []
#Holds all collected trash
collectPile = []
#Tracks score on each level
scoresList = []

#~~~ Functions ~~~ 
#Create and add trash objects to trashPile. Additionally add their hitboxes to trashHitboxes
def spawnTrash(amount, widthLowerBoundary, widthUpperBoundary, heightLowerBoundary, heightUpperBoundary):
    #Initialize Trash objects and add to trashPile list
    for i in range(amount):
        trashPile.append(trash.Trash(char.hitbox[2], char.hitbox[3], widthLowerBoundary, widthUpperBoundary, heightLowerBoundary, heightUpperBoundary))

    #Add Trash hitboxes to the trashHitboxes list. This is essential for player/trash collision
    #A separate list is needed as the collidelist() method only takes a list of rectangles.
    for i in trashPile:
        trashHitboxes.append(i.hitbox)

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
        if trashPile[collectTrash].treasure == 1:
        #If trash has treasure attribute: 10+ Coins, 5+ Points
            coinsList[0] = coinsList[0] + 10
            collectPile.append(5)
        else:
        #Normal Trash: 2+ Coints, 1+ Points
            coinsList[0] = coinsList[0] + 2
            collectPile.append(1)

        #Replace the current trash object with the new one
        trashPile[collectTrash] = newTrash

        #Replace the old hitbox with the new hitbox
        trashHitboxes[collectTrash] = newTrash.hitbox

#Update the game window with new animations/movement
#Parameters: Current Level and 4 Boundaries adjustments to define the trash spawn areas 
#Returns the number of coins earned by the end of the level
def redrawGameWindow(levelNumber, widthLowerBoundary, widthUpperBoundary, heightLowerBoundary, heightUpperBoundary):
    #Load/Update Background
    #NOTE: When there are multiple levels, create a list/if-else to load proper backgrounds per level
    if levelNumber == 1:
        win.currentWindow.blit(win.backgroundList[0][0], (0,0))

    #Draw the trash that exists in trashPile
    for trash in trashPile:
        if trash.treasure == 1:
            pygame.draw.rect(win.currentWindow, "blue", trash.hitbox)
        else:    
            pygame.draw.rect(win.currentWindow, "red", trash.hitbox)

    #Display the score
    score = len(collectPile)
    score_txt = score_font.render("Collected: " + str(score), True, "black")
    stageCounter_txt = score_font.render(str(stageCounter), True, "black")
    win.currentWindow.blit(score_txt, (10, win.winHeight-50))
    win.currentWindow.blit(stageCounter_txt, (0,0))

    #Display coins
    coin_txt = score_font.render("Coins: " + str(coinsList[0]), True, "black")
    win.currentWindow.blit(coin_txt, (800, win.winHeight-50))


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
    
    return [score, coinsList[0]]

#~~~ Main Loop ~~~
#Toggles the Running status of the game (on/off)
run = True

#Spawn the initial set of trash in the map
#Spawn Location Dimensions (estimated): X:15-950; Y:200-550
spawnTrash(5, char.speed, widthBoundary, win.backgroundList[0][1], heightBoundary)
 
#~~ Game Statuses ~~
#Initialize the game status and play the starting screen first
gameStatus = level.gameStatus("shop")

#Initialize all the states
#NOTE: Fonts are placed in a list
start = level.startGame(win.currentWindow, gameStatus, [title_font, instruction_font])
menu = level.menuScreen(win.currentWindow, gameStatus, [title_font, subtitle_font])
end = level.gameEnd(win.currentWindow, gameStatus, [title_font, subtitle_font])
shop = level.upgradeShop(win.currentWindow, gameStatus, [title_font, subtitle_font, instruction_font], char.speed, baseTime, 0)
runLevel = level.runLevel(gameStatus)

#All Cutscenes
sceneOne = level.sceneOne(win.currentWindow, gameStatus, [name_font, instruction_font], animations, dialogue_animations, char, char_sheet, scale, (widthBoundary, heightBoundary), win.backgroundList[0][0])

#Add the states to the gameStates dictionary
#This allows the gameStatus class to know which state to call
gameStates = {"start":start, "menu":menu, "end":end, "shop":shop, "runLevel":runLevel, "sceneOne":sceneOne} 

while run:
    #Loading time for game
    pygame.time.delay(100)

    #Checks for any player interaction while running (mouse clicks, keyboard, etc.)
    for event in pygame.event.get():
        #Handle scenario when the player closes the window (X)
        if event.type == pygame.QUIT:
            run = False 
        #Check when the collection game mode has started, then toggle on the counter
        elif event.type == stage_event and gameStatus.getState() == "runLevel":
            stageCounter -= 1
        #When the level ends, several changes will be made:
            # 1. Change to Shop state
            # 2. Add the player's score to the scoresList, and wipe out the current score (managed by the collecitonPile)
            # 3. Reset the counter (currently default to 10 seconds)
        if stageCounter == 0:
            stageCounter = baseTime
            gameStatus.setState("shop")
            scoresList.append(scoreCoinList[0])
            while len(collectPile) != 0:
                collectPile.pop()

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
    #If Q is pressed, return the End Screen
    if gameStatus.getState() == "menu":
        if pygame.key.get_pressed()[pygame.K_q]: 
            gameStatus.setState("end")

        #TESTING WINDOW SIZING OPTION TOGGLE
        elif pygame.key.get_pressed()[pygame.K_h]:
            if win.screenSizeIndex + 1< len(win.windowSizes):
                win.screenSizeIndex += 1
            else:
                win.screenSizeIndex = 0
            win.setWindow()
            win.updateBackground()
        
    #~~ Shop Interface ~~
    #Get the index to the upgrade from the upgradeList
    if gameStatus.getState() == "shop":
        #Update the coin display
        shop.coins = coinsList[0]

        #Check which selection the player has made
        if pygame.key.get_pressed()[pygame.K_d] and upgradeIndex < 2:
            pygame.time.delay(100)
            upgradeIndex += 1
        elif pygame.key.get_pressed()[pygame.K_a] and upgradeIndex > 0:
            pygame.time.delay(100)
            upgradeIndex -= 1
        
        #Highlights the corresponding selection made
        shop.selected = upgradeIndex

        #After confirming the index with SPACE, check if the current status is below 60
        #Then add the upgrade to the selected index
        #Update all stats and reset the timer base on the update made.
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            #Plays the level after buying/skipping upgrade
            if upgradeIndex == 2:
                pygame.time.delay(300)
                gameStatus.setState("runLevel")

            #Player buys an upgrade and checks if they have enough coins to do so
            elif upgradeList[upgradeIndex] < 60 and coinsList[0] > 0:
                #Collect the coins
                if int(upgradeList[upgradeIndex] / 10)*10 <= coinsList[0]:
                    coinsList[0] = coinsList[0] - 10*int(upgradeList[upgradeIndex] / 10)
                    #Update coinsList/display
                    shop.coins = coinsList[0]
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
                    win.currentWindow.blit(lessCoins_txt, (250, 250))
                    pygame.display.flip()
                    pygame.time.delay(500)

            #If the player reached max upgrade on any item
            elif upgradeList[upgradeIndex] >= 60:
                maxUpgradeReach_txt = subtitle_font.render("Max Upgrade Reached!", True, "blue")
                win.currentWindow.blit(maxUpgradeReach_txt, (350, 250))
                pygame.display.flip()
                pygame.time.delay(500)

            #If the player has 0 coins 
            else:
                noCoins_txt = subtitle_font.render("You have no coins!", True, "blue")
                win.currentWindow.blit(noCoins_txt, (350, 250))
                pygame.display.flip()
                pygame.time.delay(500)
        
    #Runs Collection Mode: Collecting trash
    if gameStatus.getState() == "runLevel":
        #Get the user's input, specifically which keys they pressed
        #Then base on these keys, move the player around the map
        keys = pygame.key.get_pressed()
        char.movement(keys, widthBoundary, heightBoundary, win.backgroundList[0][1])
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
        scoreCoinList = redrawGameWindow(1, char.speed, widthBoundary, win.backgroundList[0][1], heightBoundary)

        #Update Shop Coin Display
        shop.coins = scoreCoinList[1]

#When the game is off, close the pygame program as well.
pygame.quit()
