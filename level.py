#This file manages the gameStatus, which is the cutscenes or levels to be played
#Each level or cutscene, which will be called states, is defined in its own class
import pygame
import window

#NOTE: Add a way to track already played scenes/levels

#~~ Background Images ~~
tempWin = window.Window("Our Earth")

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
    def __init__(self, gameStatus, fontSet):
        self.display = tempWin.currentWindow
        self.gameStatus = gameStatus
        self.fontSet = fontSet

    def run(self):
        self.display.blit(tempWin.backgroundList[1][0], (0,0))

        pygame.display.flip()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            pygame.time.delay(300)
            self.gameStatus.setState("playPrologue")

#Menu Screen
class menuScreen():
    def __init__(self, gameStatus, fontSet):
        self.display = tempWin.currentWindow
        self.gameStatus = gameStatus
        self.fontSet = fontSet
        self.select = None
        self.width = tempWin.winWidth
        self.height = tempWin.winHeight

    def run(self):
        self.display.blit(tempWin.backgroundList[0][0], (0,0))

        #Toggle screen size and updates the backgrounds accordingly
        #3 different sizes: Small, Default, Large
        if pygame.key.get_pressed()[pygame.K_h]:
            if tempWin.screenSizeIndex + 1 < len(tempWin.windowSizes):
                tempWin.screenSizeIndex += 1
                pygame.time.delay(200)
            else:
                tempWin.screenSizeIndex = 0
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
    def __init__(self, gameStatus, fontSet, speed, time, coins):
        self.display = tempWin.currentWindow
        self.gameStatus = gameStatus
        self.fontSet = fontSet
        self.speedBuff = speed
        self.timeBuff = time
        self.coins = coins
        self.selected = None

    def run(self):
        #Background Display
        #When an upgrade is selected, change the background to show it highlighted
        #Each upgrade button corresponds to an integer
        if (self.selected == 0):
            self.display.blit(tempWin.backgroundList[4][0], (0,0))
        elif (self.selected == 1):
            self.display.blit(tempWin.backgroundList[5][0], (0,0))
        elif (self.selected == 2):
            self.display.blit(tempWin.backgroundList[6][0], (0,0))

        #Display Coins
        #Coins Display Text
        coins_txt = self.fontSet[1].render(str(self.coins), False, "white")
        tempWin.addUI(coins_txt, (50, 530))

        pygame.display.flip()
        
#The ending scene
class gameEnd():
    def __init__(self, gameStatus, fontSet):
        self.display = tempWin.currentWindow
        self.gameStatus = gameStatus 
        self.fontSet = fontSet

    def run(self):
        self.display.blit(tempWin.backgroundList[2][0], (0,0))

        pygame.display.flip()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.gameStatus.setState("start")
      
#Runs the collection game mode. To run, I simply toggle the variable collectionMode
class runLevel():
    def __init__(self, gameStatus, levelNumber):
        self.gameStatus = gameStatus 
        self.levelNumber = levelNumber
    def run(self):
        if self.levelNumber == 1:
            tempWin.currentWindow.blit(tempWin.backgroundList[3][0], (0,0))

# ~~Cutscenes~~
class dialogueBox():
    def __init__(self, color, animationSet, fontSet):
        self.display = tempWin.currentWindow
        self.color = color
        self.animationSet = animationSet
        self.fontSet = fontSet

    #Character limit is 50
    #Create a dialogue block on the bottom of the screen and display the given set of text
    def setDialogue(self, textSet, counter):
        #Run the dialogue 
        if len(textSet) > counter:
            self.dialogueBox = pygame.Rect(0, 420, tempWin.winWidth, tempWin.winHeight)
            pygame.draw.rect(self.display, self.color, self.dialogueBox)
            tempWin.addUI(self.animationSet[0][0], (-80, 350))

            instructions_txt = self.fontSet[1].render("Press SPACE to continue", True, "white")
            tempWin.addUI(instructions_txt, (800, 550))

            #NOTE: Find a way to have multiple sentences rotate/show in a dialogue box
           
            dialogue_txt = self.fontSet[0].render(textSet[counter], True, "white")
            tempWin.addUI(dialogue_txt, (200, 500))
        
    
class sceneOne():
    def __init__(self, gameStatus, fontSet, animationSet, profileSet, playerClass, playerSheet, scale, windowDimensions):
        self.display = tempWin.currentWindow
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
        self.sceneText = 0
        self.counter = 0

        #Animations for the scene
        self.currentFrame = 0
        self.previousTime = pygame.time.get_ticks()

        #A temporary variable to help set the player's position in the scene
        self.setPlayerPosition = True
        

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
        self.display.blit(self.animationSet[currentSet][self.currentFrame], (self.playerClass.x, self.playerClass.y))

    #loops through the given dialogue list with the given dialogue box. After the dialogue is finished, set the next scene
    def loopDialogue(self, gameState, dialogueList, dialogueBox, movementTrue):
        #Loop through dialogue
        #First check if the player is moving and the current scene exist in the dialogue list
        if self.sceneMove == False and len(dialogueList) > self.sceneText:
            #Get the list of lines for the scene
            currentTextSet = dialogueList[self.sceneText]
            #When the player presses space, run the next line
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                pygame.time.delay(300)
                self.counter += 1 
            #If the list is finished, run the next list. If player is required to move for the next scene
            #check movementTrue and set the sceneMove to true
            elif (len(currentTextSet) <= self.counter):
                if movementTrue == True:
                    self.sceneMove = True
                self.sceneText += 1
            #When all conditions are checked, set the dialogue to from the current scene and counter
            dialogueBox.setDialogue(currentTextSet, self.counter)
        #If there is a gameState and the dialogueList (aka all the scenes) are finished, set the next state
        if gameState != None and len(dialogueList) <= self.sceneText:
            self.gameStatus.setState(gameState)

    def run(self):
        #Set where the player will appear on the scene when this class runs
        if self.setPlayerPosition == True:
            self.playerClass.x = 300
            self.playerClass.y = 250
            self.setPlayerPosition = False

        #Spawn a trigger block to que the next sceneText
        NPC = pygame.Rect(600, 500, 100, 50)

        #Set up Dialogue
        testBox = dialogueBox("black", self.profileSet, self.fontSet)
        textOne = ["WOAH! Earth is bigger than I thought", "Base on the travel guide, there should be squawkers here", "Let's find a good spot to lay down"]
        textTwo = ["Huh, what are all these hard \"rocks\"?", "OUCH! It got on my feet!", "Do humans really live in these conditions??", "Hmm, if I want to watch the squakers...", "...then I have to clear the area", "Let's clean up a bit. It shouldn't take too long, right?"]
        dialogueList = [textOne, textTwo]
        
        self.display.blit(tempWin.backgroundList[3][0], (0 ,0))
        pygame.draw.rect(self.display, "red", NPC)

        sceneOne.movementScene(self)
       
        if pygame.Rect.colliderect(self.playerClass.hitbox, NPC) == True and self.sceneMove == True:
            self.sceneMove = False
            self.counter = 0
    
        self.loopDialogue("runLevel", dialogueList, testBox, True)

        pygame.display.flip()

#Inherits the sceneOne class methods
class prologue(sceneOne):
    def __init__(self, gameStatus, fontSet, animationSet, profileSet, playerClass, playerSheet, scale, windowDimensions):
        self.display = tempWin.currentWindow
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
        self.sceneText = 0
        self.counter = 0

        #Animations for the scene
        self.currentFrame = 0
        self.previousTime = pygame.time.get_ticks()

        #A temporary variable to help set the player's position in the scene
        self.setPlayerPosition = True


    def run(self):
        #Set player location on scene when this class runs
        if self.setPlayerPosition == True:
            self.playerClass.x = 0
            self.playerClass.y = 0
            self.setPlayerPosition = False

        self.display.fill("black")
        prologueBox = dialogueBox("black", self.profileSet, self.fontSet)
        prologue1 = ["For years, humans have always thought for themselves", "They never knew that beyond the Earth...", 'there were ALIENS!!']
        self.loopDialogue(None, prologue1, prologueBox, False)

        pygame.display.flip()


        