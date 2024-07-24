#This file manages the gameStatus, which is the cutscenes or levels to be played
#Each level or cutscene, which will be called states, is defined in its own class
import pygame
import window

#NOTE: Add a way to track already played scenes/levels

#~~ Initialize Game Window ~~
tempWin = window.Window("Our Earth")

# ~~Scene Tracker ~~
#Tracks all new and played scenes 
newScenes = ["playPrologue", "runLevel"]
#When a scene has been played, it will be popped from the newScenes and appended to playedScenes
playedScenes = []

#Sets the game status, return the current status, and set the status
class gameStatus():
    def __init__(self, currentState):
        self.currentState = currentState
        self.previousState = currentState

    def getState(self):
        return self.currentState
    def setState(self, changeState):
        self.currentState = changeState

    #Retrieve the previous state called for the menu
    def setPreviousState(self):
        self.previousState = self.currentState
    def getPreviousState(self):
        return self.previousState

#The starting screen
class startGame():
    def __init__(self, gameStatus):
        self.gameStatus = gameStatus

    def run(self):
        tempWin.currentWindow.blit(tempWin.backgroundList[1][0], (0,0))

        pygame.display.flip()


        if pygame.key.get_pressed()[pygame.K_SPACE]:
            pygame.time.delay(300)
            self.gameStatus.setState("selectLevel")

#Level Selection Screen: Replay any cutscene or level
class selectLevel():
    def __init__(self, gameStatus, fontSet):
        self.gameStatus = gameStatus
        self.fontSet = fontSet
        self.levelIndex = 0

    def run(self):
        tempWin.currentWindow.blit(tempWin.backgroundList[7][0], (0,0))
        prologue_rect = pygame.Rect(200,300, 200,100)
        sceneOne_rect = pygame.Rect(500,300, 200,100)
        pygame.draw.rect(tempWin.currentWindow, "red", prologue_rect)
        pygame.draw.rect(tempWin.currentWindow, "red", sceneOne_rect)
        prologue_txt = self.fontSet[0].render("Prologue", True, "white")
        levelOne_txt = self.fontSet[0].render("Level One", True, "white")

        if pygame.key.get_pressed()[pygame.K_a] and self.levelIndex > 0:
            self.levelIndex -= 1
        elif pygame.key.get_pressed()[pygame.K_d] and self.levelIndex < len(newScenes) - 1:
            self.levelIndex += 1
        elif pygame.key.get_pressed()[pygame.K_SPACE]:
            self.gameStatus.setState(newScenes[self.levelIndex])

        if self.levelIndex == 0:
            pygame.draw.rect(tempWin.currentWindow, "pink", prologue_rect)
        elif self.levelIndex == 1:
            pygame.draw.rect(tempWin.currentWindow, "pink", sceneOne_rect)

        tempWin.addUI(prologue_txt, (225,325))
        tempWin.addUI(levelOne_txt, (525,325))
        
        pygame.display.flip()
        

#Menu Screen
class menuScreen():
    def __init__(self, gameStatus , fontSet):
        self.gameStatus = gameStatus
        self.fontSet = fontSet
        self.select = None
        self.width = tempWin.winWidth
        self.height = tempWin.winHeight

    def run(self):
        tempWin.currentWindow.blit(tempWin.backgroundList[0][0], (0,0))

        currentSize = tempWin.windowSizes[tempWin.screenSizeIndex]

        #Display width and height
        windowSize_txt = self.fontSet[0].render(str(currentSize[0]) + "x" + str(currentSize[1]), True, "black")
        tempWin.addUI(windowSize_txt, (300,380))

        #Toggle screen size and updates the backgrounds accordingly
        #3 different sizes: Small, Default, Large
        if pygame.key.get_pressed()[pygame.K_d] and tempWin.screenSizeIndex < len(tempWin.windowSizes) - 1:
            tempWin.screenSizeIndex += 1
            pygame.time.delay(200)
        elif pygame.key.get_pressed()[pygame.K_a] and tempWin.screenSizeIndex > 0:
            tempWin.screenSizeIndex -= 1
            pygame.time.delay(200)
        elif pygame.key.get_pressed()[pygame.K_SPACE]:
            tempWin.setWindow()
            tempWin.updateBackground()
            
        #After the sizes are adjusted, update the width and height variables 
        #These variables will be accessed and updated in main.py
        self.width = tempWin.winWidth
        self.height = tempWin.winHeight

        #NOTE: Render buttons when pressed

        pygame.display.flip()

#Displays Upgrade Shop after every level
class upgradeShop():
    def __init__(self, gameStatus, speed, time, coins, fontSet):
        self.gameStatus = gameStatus
        self.speedBuff = speed
        self.timeBuff = time
        self.coins = coins
        self.fontSet = fontSet
        self.selected = None
        self.price = 10

    def run(self):
        #Create a text to display the price
        price_txt = self.fontSet[0].render(str(self.price), True, "white")

        #Background Display
        #When an upgrade is selected, change the background to show it highlighted
        #Each upgrade button corresponds to an integer
        #Only display the price if an upgrade is selected
        if (self.selected == 0):
            tempWin.currentWindow.blit(tempWin.backgroundList[4][0], (0,0))
            tempWin.addUI(price_txt, (50, 50))
        elif (self.selected == 1):
            tempWin.currentWindow.blit(tempWin.backgroundList[5][0], (0,0))
            tempWin.addUI(price_txt, (50, 50))
        elif (self.selected == 2):
            tempWin.currentWindow.blit(tempWin.backgroundList[6][0], (0,0))

        #Display Coins
        #Coins Display Text
        coins_txt = self.fontSet[0].render(str(self.coins), True, "white")
        tempWin.addUI(coins_txt, (50, 530))

        pygame.display.flip()
        
#The ending scene
class gameEnd():
    def __init__(self, gameStatus):
        tempWin.currentWindow = tempWin.currentWindow
        self.gameStatus = gameStatus 

    def run(self):
        tempWin.currentWindow.blit(tempWin.backgroundList[2][0], (0,0))

        pygame.display.flip()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.gameStatus.setState("start")
      
#Runs the collection game mode. To run, I simply toggle the variable collectionMode
class runLevel():
    def __init__(self, gameStatus, playerClass):
        self.gameStatus = gameStatus 
        self.levelNumber = None
        self.playerClass = playerClass
        self.setPlayerPosition = True

    def run(self):
        #NOTE: Use a python equivalent of a switch-case or dictionary?
        if self.levelNumber == 1:
            tempWin.currentWindow.blit(tempWin.backgroundList[3][0], (0,0))
            if self.setPlayerPosition == True:
                self.playerClass.x = 600
                self.playerClass.y = 400
                self.setPlayerPosition = False
        elif self.levelNumber == 2:
            tempWin.currentWindow.fill("white")



# ~~Cutscenes~~
class dialogueBox():
    def __init__(self, color, animationSet, fontSet):
        tempWin.currentWindow = tempWin.currentWindow
        self.color = color
        self.animationSet = animationSet
        self.fontSet = fontSet

    #Character limit is 50
    #Create a dialogue block on the bottom of the screen and display the given set of text
    def setDialogue(self, textSet, nextLine):
        #Run the dialogue 
        if len(textSet) > nextLine:
            self.dialogueBox = pygame.Rect(0, 420, tempWin.winWidth, tempWin.winHeight)
            pygame.draw.rect(tempWin.currentWindow, self.color, self.dialogueBox)
            tempWin.addUI(self.animationSet[0][0], (-80, 350))

            instructions_txt = self.fontSet[1].render("Press SPACE to continue", True, "white")
            tempWin.addUI(instructions_txt, (800, 550))

            #NOTE: Find a way to have multiple sentences rotate/show in a dialogue box
           
            dialogue_txt = self.fontSet[0].render(textSet[nextLine], True, "white")
            tempWin.addUI(dialogue_txt, (200, 500))
        
#Summary: The player lands on earth at a beach. They are excited to explore and witness seagulls for the first time.
#However, they are stopped by the massive amount of trash filling the beach. To remedy the situation, they start to clean up
#for the first time.
class sceneOne():
    def __init__(self, gameStatus, fontSet, animationSet, profileSet, playerClass, playerSheet, scale, windowDimensions):
        tempWin.currentWindow = tempWin.currentWindow
        self.gameStatus = gameStatus 
        self.fontSet = fontSet
        self.animationSet = animationSet
        self.profileSet = profileSet
        self.playerClass = playerClass
        self.playerSheet = playerSheet
        self.scale = scale
        
        self.width = windowDimensions[0]
        self.height = windowDimensions[1]

        #Tracks scene progression/dialogue
        self.sceneMove = False
        self.dialoguePart = 0
        self.nextLine = 0

        #Animations for the scene
        self.currentFrame = 0
        self.previousTime = pygame.time.get_ticks()

        #A temporary variable to help set the player's position in the scene
        self.setPlayerPosition = True
        self.nextSceneToggle = False
        
    #Allow the character to move around the map when sceneMove is True
    def movementScene(self):
        #Allow players to move when True
        if self.sceneMove == True:
            keys = pygame.key.get_pressed()
            self.playerClass.movement(keys, self.playerClass.speed, self.width, 200, self.height)

        #Idle Animation
        currentSet = self.playerClass.currentSet
        currentTime = pygame.time.get_ticks()
        self.currentFrame = self.playerSheet.frameTiming(currentTime, self.previousTime, 200, self.currentFrame, currentSet)[0]
        self.previousTime = self.playerSheet.frameTiming(currentTime, self.previousTime, 200, self.currentFrame, currentSet)[1]
        self.playerClass.playerHitbox(self.scale)
        tempWin.currentWindow.blit(self.animationSet[currentSet][self.currentFrame], (self.playerClass.x, self.playerClass.y))

    #Loops through the given dialogue list with the given dialogue box. After the dialogue is finished, set the next scene
    def loopDialogue(self, gameState, dialogueList, dialogueBox):
        #First check if all the dialogue has been spoken, else run the next set of dialogue (dialoguePart) from the list (dialogueList)
        if len(dialogueList) > self.dialoguePart:
            #Get the list of lines for the scene
            currentDialogueLines = dialogueList[self.dialoguePart]

            #When the player presses space, run the next line
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                pygame.time.delay(300)
                self.nextLine += 1 

            #If the part is finished, run the next part in the list.
            #In order to run the next part, check if the nextScene can be run and the player is no longer moving
            if (len(currentDialogueLines) <= self.nextLine):
                if self.nextSceneToggle == True and self.sceneMove == False:
                    self.dialoguePart += 1
                    self.nextLine = 0
                #Turn off the nextSceneToggle for the next part
                self.nextSceneToggle = False                

            #When all conditions are checked, display the lines of dialogue onto the dialogueBox
            dialogueBox.setDialogue(currentDialogueLines, self.nextLine)

        #If there is a gameState and the dialogueList (aka all the dialogue parts) are finished, set the next state to run the next scene
        if gameState != None and len(dialogueList) <= self.dialoguePart:
            self.gameStatus.setState(gameState)

    def run(self):
        #Player Location when scene starts
        if self.setPlayerPosition == True:
            self.playerClass.x = 300
            self.playerClass.y = 250
            self.setPlayerPosition = False

        #Display background
        tempWin.currentWindow.blit(tempWin.backgroundList[3][0], (0 ,0))
        #Spawn a trigger block to signal the next dialoguePart
        NPC = pygame.Rect(600, 500, 100, 50)
        pygame.draw.rect(tempWin.currentWindow, "red", NPC)

        #Set up Dialogue
        testBox = dialogueBox("black", self.profileSet, self.fontSet)
        scene1_1 = ["WOAH! Earth is bigger than I thought", 
                   "Base on the travel guide, there should be squawkers here",
                   "Let's find a good spot to lay down"]
        scene1_2 = ["Huh, what are all these hard \"rocks\"?", 
                   "OUCH! It got on my feet!", 
                   "Do humans really live in these conditions??",
                   "Hmm, if I want to watch the squakers...",
                   "...then I have to clear the area", 
                   "Let's clean up a bit. It shouldn't take too long, right?"]
        dialogueList = [scene1_1, scene1_2] 
        
        #First play scene1_1. After it finish, allow player to move
        if self.dialoguePart < 1:
            self.sceneMove = True
            #Wait until the player touches the NPC rectangle to play scene1_2
            if pygame.Rect.colliderect(self.playerClass.hitbox, NPC) == True:
                self.sceneMove = False
                self.nextSceneToggle = True
        #After both dialogue parts are finished, run the level
        if self.dialoguePart == 1:
            self.sceneMove = False
            self.nextSceneToggle = True

        self.movementScene()
        #NOTE: Switch to tutorial when it is complete
        self.loopDialogue("runLevel", dialogueList, testBox)

        pygame.display.flip()

#Summary: The player is introducted to their avatar. They are an alien who works as a taxi driver.
#Due to the character's strong work ethic, they were able to get a free vacation and decided to visit Earth.
#Inherits the sceneOne class methods
class prologue(sceneOne):
    def __init__(self, gameStatus, fontSet, animationSet, profileSet, playerClass, playerSheet, scale, windowDimensions):
        tempWin.currentWindow = tempWin.currentWindow
        self.gameStatus = gameStatus 
        self.fontSet = fontSet
        self.animationSet = animationSet
        self.profileSet = profileSet
        self.playerClass = playerClass
        self.playerSheet = playerSheet
        self.scale = scale
        self.width = windowDimensions[0]
        self.height = windowDimensions[1]

        #Tracks scene progression/dialogue
        self.sceneMove = False
        self.dialoguePart = 0
        self.nextLine = 0

        #Animations for the scene
        self.currentFrame = 0
        self.previousTime = pygame.time.get_ticks()

        #A temporary variable to help set the player's position in the scene
        self.setPlayerPosition = True
        self.nextSceneToggle = None

    def run(self):
        #Set player location for the scene
        #The player is currently offscreen
        if self.setPlayerPosition == True:
            self.playerClass.x = -200
            self.playerClass.y = 250
            self.setPlayerPosition = False

        #Set up background
        tempWin.currentWindow.fill("black")

        #Create the UFO to board
        UFO = pygame.Rect(740, 150, 200, 100)
        #Draw the UFO. When the player is on it, the next scene will play
        pygame.draw.rect(tempWin.currentWindow, "grey", UFO)

        #Set up dialogue
        prologueBox = dialogueBox("black", self.profileSet, self.fontSet)
        prologue0 = ["Humans are selfish creatures", 
                     "They never knew that beyond the Earth...", 
                     "there were ALIENS!!"]
        prologue1 = ["Oh sorry. I forgot to introduce myself",
                     "Hi there! I'm Meep, commander of the Shuttle buggy",
                     "Shuttle buggy is the best space ship accross the galaxy!",
                     "I've been an excellence driver...",
                     "for Intergalatica's Space Taxi Service",
                     "So much so that my boss decided to give me...",
                     "a paid vacation! WOOHOOO!!",
                     "I have dreamt of coming to Earth since I was a blob",
                     "Join me on my vacation why don't you?",
                     "Let's get on the Shuttle Buggy!",
                     "Use the WASD keys to move toward the ship"]
        prologue2 = ["ALL ABOARD THE SHUTTLE BUGGY!",
                     "your safety is not guaranteed",
                     "the taxi service is not responsible for lost items,",
                     "limbs, or children.",
                     "Sit tight and relax!"]
        dialogueList = [prologue0, prologue1, prologue2]


        #Play the first three prologue sets
        if self.dialoguePart < 1:
            # #Run the dialogue without an ending scene
            # self.loopDialogue(None, dialogueList, prologueBox)

            #Waits for prologue0 to finish, then makes the character appear across the screen
            if self.nextSceneToggle == False and self.playerClass.x < 300:
                self.playerClass.x += 15
            #When the player finish moving, run prologue1 and prologue2
            elif self.playerClass.x >= 300:
                self.nextSceneToggle = True

        #After prologue 0,1,2, run a movementScene and prologue 3
        else:
            #Allow the player to move after prologue 2
            self.sceneMove = True
            
            #Wait for the player to reach the ship, then play prologue3
            if pygame.Rect.colliderect(self.playerClass.hitbox, UFO) == True:
                self.sceneMove = False
                self.nextSceneToggle = True
                
        self.movementScene()
        self.loopDialogue("sceneOne", dialogueList, prologueBox)

        pygame.display.flip()

class tutorial(sceneOne):
    def __init__(self, gameStatus, fontSet, animationSet, profileSet, playerClass, playerSheet, scale, windowDimensions):
        self.gameStatus = gameStatus 
        self.fontSet = fontSet
        self.animationSet = animationSet
        self.profileSet = profileSet
        self.playerClass = playerClass
        self.playerSheet = playerSheet
        self.scale = scale
        self.width = windowDimensions[0]
        self.height = windowDimensions[1]

        #Tracks scene progression/dialogue
        self.sceneMove = True
        self.dialoguePart = 0
        self.nextLine = 0

        #Animations for the scene
        self.currentFrame = 0
        self.previousTime = pygame.time.get_ticks()

        #A temporary variable to help set the player's position in the scene
        self.setPlayerPosition = True
        self.nextSceneToggle = None
        

    #NOTE: For an easy tutorial, simply show a cutscene of instructions rather than live for now
    def run(self):
        if self.setPlayerPosition == True:
            self.playerClass.x = 600
            self.playerClass.y = 400
            self.setPlayerPosition = False
        tempWin.currentWindow.blit(tempWin.backgroundList[3][0], (0,0))
        self.movementScene()
        



        pygame.display.flip()