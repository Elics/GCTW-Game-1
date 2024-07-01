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
char_sheet = sprite.Sprite("NPC.png", scale)
#Frame Number, X, Y, Width, Height, Scale
#Take a single frame from the sprite sheet to obtain dimensions
char_frame = char_sheet.getFrame(0, 0, 0, 32, 32)
char_w = char_frame.get_width()
char_h = char_frame.get_height()
#Initialize the player
char = player.Player(char_x, char_y, char_w, char_h, char_s)
#Create player hitbox
char.playerHitbox(scale)

#Scaled up character for dialogue
char_dialogue_sheet = sprite.Sprite("NPC.png", 10)
dialogue_char = char_dialogue_sheet.getFrame(0, 0, 0, 32, 32)
dialogue_animations = char_dialogue_sheet.getAnimations()

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
name_font = pygame.font.SysFont('Nunito', 40, True)
# dialogue_font = pygame.font.SysFont('')

#~~ Shop Features ~~
#Since all the required variables are initialized above, the shop will be created below
#Index to loop through available upgrades
upgradeIndex = 0
#A list to store all coin values collected
coinsList = []
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
        
        #To track score, I currently have a list. 
        #Everytime a trash been collected, it will be tallied in this list
        #I need to find a way to replace this method, wastes resources
        #If a trash has the treasure attribute, it will provide coins and 5 points
        if trashPile[collectTrash].treasure == 1:
            coinsList.append(10)
            collectPile.append(5)
        else:
            collectPile.append(1)

        #Replace the current trash object with the new one
        trashPile[collectTrash] = newTrash

        #Replace the old hitbox with the new hitbox
        trashHitboxes[collectTrash] = newTrash.hitbox

#Update the game window with new animations/movement
def redrawGameWindow():
    #Load/Update Background
    win.fill("white")

    #Load trash that exists in trashPile
    for trash in trashPile:
        if trash.treasure == 1:
            pygame.draw.rect(win, "blue", trash.hitbox)
        else:    
            pygame.draw.rect(win, "red", trash.hitbox)

    #Display the score
    score = len(collectPile)
    score_txt = score_font.render("Collected: " + str(score), True, "black")
    stageCounter_txt = score_font.render(str(stageCounter), True, "black")
    win.blit(score_txt, (10, winHeight-50))
    win.blit(stageCounter_txt, (0,0))

    #Display coins
    totalCoins = sum(coinsList)
    coin_txt = score_font.render("Coins: " + str(totalCoins), True, "black")
    win.blit(coin_txt, (800, winHeight-50))


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
    
    return [score, totalCoins]

#~~~ Main Loop ~~~
#Toggles the Running status of the game (on/off)
run = True

#Spawn the initial set of trash in the map
spawnTrash(5)

#~~ Game Statuses ~~
#Initialize the game status and play the starting screen first
gameStatus = level.gameStatus("sceneOne")
#Initialize all the states
start = level.startGame(win, gameStatus, title_font, subtitle_font)
menu = level.menuScreen(win, gameStatus, title_font, subtitle_font)
end = level.gameEnd(win, gameStatus, title_font, subtitle_font)
shop = level.upgradeShop(win, gameStatus, title_font, subtitle_font, char.speed, baseTime, 0)
sceneOne = level.sceneOne(win, gameStatus, name_font, subtitle_font, animations, dialogue_animations)
level = level.runLevel(gameStatus)

#Add the states to the gameStates dictionary
gameStates = {"start":start, "menu":menu, "end":end, "shop":shop, "level":level, "sceneOne":sceneOne} 

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
            scoresList.append(scoreCoinList[0])
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
        #If Q is pressed, return the End Screen
    if pygame.key.get_pressed()[pygame.K_q] and gameStatus.getState() == "menu":
        gameStatus.setState("end")
        
    #Shop interface/Interaction
    #Get the index to the upgrade from the upgradeList
    if gameStatus.getState() == "shop":
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
        #Update all stats and reset the timer base on the update made. Play level when choice is made
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            #Plays the level after buying/skipping upgrade
            if upgradeIndex == 2:
                pygame.time.delay(300)
                gameStatus.setState("level")
            #Player buys an upgrade and has money to do so
            elif upgradeList[upgradeIndex] < 60 and len(coinsList) > 0:
                #Collect the coins
                if int(upgradeList[upgradeIndex] / 10) <= len(coinsList):
                    for i in range(int(upgradeList[upgradeIndex] / 10)):
                        coinsList.pop()
                    shop.coins = sum(coinsList)
                    #Increase corresponding upgrade by 10 on the upgradeList
                    upgradeList[upgradeIndex] = upgradeList[upgradeIndex] + 10
                    #Update the corresponding variables base on the values in the upgradeList
                    char.speed = upgradeList[0]
                    baseTime = upgradeList[1] 
                    #Update the stageCounter, the buff displays, and coin display for the gameStatus.upgradeShop
                    stageCounter = baseTime
                    shop.speedBuff = char.speed
                    shop.timeBuff = baseTime  
                #If the player does not have enough coins
                else:
                    lessCoins_txt = subtitle_font.render("Not enough coins for next upgrade level!", True, "blue")
                    win.blit(lessCoins_txt, (250, 250))
                    pygame.display.flip()
                    pygame.time.delay(500)
            #If the player reached max upgrade on any item
            elif upgradeList[upgradeIndex] == 60:
                maxUpgradeReach_txt = subtitle_font.render("Max Upgrade Reached!", True, "blue")
                win.blit(maxUpgradeReach_txt, (350, 250))
                pygame.display.flip()
                pygame.time.delay(500)
            #If the player has no coins
            else:
                noCoins_txt = subtitle_font.render("You have no coins!", True, "blue")
                win.blit(noCoins_txt, (350, 250))
                pygame.display.flip()
                pygame.time.delay(500)
        
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
        scoreCoinList = redrawGameWindow()

        #Update Shop Coin Display
        shop.coins = scoreCoinList[1]

#When the game is off, close the pygame program as well.
pygame.quit()
