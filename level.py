#This file manages the gameStatus, which is the cutscenes or levels to be played
#Each level or cutscene, which will be called states, is defined in its own class
import pygame
import window

#NOTE: Add a way to track already played scenes/levels

#~~ Background Images ~~
tempWin = window.Window("Our Earth")
tempWin.addBackground("images\\backgrounds\\Menu.png", None)
tempWin.addBackground("images\\backgrounds\\Start.png", None)
tempWin.addBackground("images\\backgrounds\\Quit.png", None)


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
    def __init__(self, display, gameStatus, fontSet):
        self.display = display
        self.gameStatus = gameStatus
        self.fontSet = fontSet

    def run(self):
        self.display.blit(tempWin.backgroundList[1][0], (0,0))

        pygame.display.flip()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            pygame.time.delay(300)
            self.gameStatus.setState("sceneOne")

#Menu Screen
class menuScreen():
    def __init__(self, display, gameStatus, fontSet):
        self.display = display
        self.gameStatus = gameStatus
        self.fontSet = fontSet
        self.select = None

    def run(self):
        self.display.blit(tempWin.backgroundList[0][0], (0,0))

        #NOTE: Render buttons when pressed

        pygame.display.flip()

#Displays Upgrade Shop after every level
class upgradeShop():
    def __init__(self, display, gameStatus, fontSet, speed, time, coins):
        self.display = display
        self.gameStatus = gameStatus
        self.fontSet = fontSet
        self.speedBuff = speed
        self.timeBuff = time
        self.coins = coins
        self.selected = None

    def run(self):
        self.display.fill("#E5FFB8")
        #Create top of screen text
        title_txt = self.fontSet[0].render("Shop", True, "black")
        instructions_txt = self.fontSet[1].render("Press SPACE to select/Press M to access MENU", True, "black")
        cost_txt = self.fontSet[2].render("Each upgrade starts at 10 coins and increased by 10 coins over time", True, "black")

        #Create button and captions text
        speedRect = pygame.Rect(100, 300, 325, 50)
        timeRect = pygame.Rect(600, 300, 325, 50)
        skipRect = pygame.Rect(350, 400, 325, 50)
        speed_txt = self.fontSet[1].render("Current Speed: " + str(self.speedBuff), False, "black")
        time_txt = self.fontSet[1].render("Current Timelimit: " + str(self.timeBuff), False, "black")
        coins_txt = self.fontSet[1].render("Coins: " + str(self.coins), False, "black")
        speedUpgrade_txt = self.fontSet[1].render("Speed +10", False, "black")
        timeUpgrade_txt = self.fontSet[1].render("Time +10", False, "black")
        skip_txt = self.fontSet[1].render("Next Level", False, "Red")

        #Render the Shop Text & Instructions
        self.display.blit(title_txt, (400, 0))
        self.display.blit(coins_txt, (800, 20))
        self.display.blit(cost_txt, (250, 150))
        self.display.blit(instructions_txt, (50, 550))

        #When a button is selected, highlight its corresponding rectangle
        #Each upgrade button corresponds to an integer
        if (self.selected == 0):
            pygame.draw.rect(self.display, "pink", speedRect)
        else:
            pygame.draw.rect(self.display, "white", speedRect)
        self.display.blit(speed_txt, (100, 100))
        self.display.blit(speedUpgrade_txt, (150, 300))

        if (self.selected == 1):
            pygame.draw.rect(self.display, "pink", timeRect)
        else:
            pygame.draw.rect(self.display, "white", timeRect)
        self.display.blit(time_txt, (600, 100))
        self.display.blit(timeUpgrade_txt, (650, 300))

        if (self.selected == 2):
            pygame.draw.rect(self.display, "pink", skipRect)
        else:
            pygame.draw.rect(self.display, "white", skipRect)
        self.display.blit(skip_txt, (380, 400))

        pygame.display.flip()
        
#The ending scene
class gameEnd():
    def __init__(self, display, gameStatus, fontSet):
        self.display = display
        self.gameStatus = gameStatus 
        self.fontSet = fontSet

    def run(self):
        self.display.blit(tempWin.backgroundList[2][0], (0,0))

        pygame.display.flip()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.gameStatus.setState("start")
      
#Runs the collection game mode. To run, I simply toggle the variable collectionMode
class runLevel():
    def __init__(self, gameStatus):
        self.gameStatus = gameStatus 
    def run(self):
        pass

# ~~Cutscenes~~
class dialogueBox():
    def __init__(self, display, color, animationSet, fontSet):
        self.display = display
        self.color = color
        self.animationSet = animationSet
        self.fontSet = fontSet

    #Character limit is 50
    def setDialogue(self, textSet, counter):
        #Run the dialogue 
        if len(textSet) > counter:
            self.dialogueBox = pygame.Rect(0, 420, 1000, 200)
            pygame.draw.rect(self.display, self.color, self.dialogueBox)
            self.display.blit(self.animationSet[0][0], (-80, 350))

            instructions_txt = self.fontSet[1].render("Press SPACE to continue", True, "white")
            self.display.blit(instructions_txt, (800, 550))
            dialogue_txt = self.fontSet[0].render(textSet[counter], True, "white")
            self.display.blit(dialogue_txt, (200, 500))
        else:
            self.display.fill("white")
        

class sceneOne():
    def __init__(self, display, gameStatus, fontSet, animationSet, dialogueSet, playerClass, playerSheet, scale, windowDimensions, background):
        self.display = display
        self.gameStatus = gameStatus 
        self.fontSet = fontSet
        self.animationSet = animationSet
        self.dialogueSet = dialogueSet
        self.playerClass = playerClass
        self.playerSheet = playerSheet
        self.scale = scale
        self.sceneMove = False
        self.sceneText = 0
        self.width = windowDimensions[0]
        self.height = windowDimensions[1]
        self.background = background

        #Animations for the scene
        self.currentFrame = 0
        self.counter = 0
        self.previousTime = pygame.time.get_ticks()
        self.playerClass.x = 300
        self.playerClass.y = 250

    def run(self):
        self.display.blit(self.background, (0 ,0))
        NPCs = [pygame.Rect(600, 500, 100, 50)]

        #Set up Dialogue
        testBox = dialogueBox(self.display, "black", self.dialogueSet, self.fontSet)
        textOne = ["Finally, after a long day I can relax on the beach.", "Let's find a good spot to lay down."]
        textTwo = ["Hmm, it is pretty hard to find a spot", "Let's clean up a bit."]
        dialogueList = [textOne, textTwo]
        
        for NPC in NPCs:
            pygame.draw.rect(self.display, "red", NPC)
            
        #Allow players to move when True
        if self.sceneMove == True:
            keys = pygame.key.get_pressed()
            self.playerClass.movement(keys, self.width, self.height, 200)

        #Idle Animation
        currentSet = self.playerClass.currentSet
        currentTime = pygame.time.get_ticks()
        self.currentFrame = self.playerSheet.frameTiming(currentTime, self.previousTime, 200, self.currentFrame, currentSet)[0]
        self.previousTime = self.playerSheet.frameTiming(currentTime, self.previousTime, 200, self.currentFrame, currentSet)[1]
        self.playerClass.playerHitbox(self.scale)
        self.display.blit(self.animationSet[currentSet][self.currentFrame], (self.playerClass.x, self.playerClass.y))

        if pygame.Rect.collidelist(self.playerClass.hitbox, NPCs) != -1 and self.sceneMove == True:
            self.sceneMove = False
            self.counter = 0
    
        #Loop through dialogue
        if self.sceneMove == False and len(dialogueList) > self.sceneText:
            currentTextSet = dialogueList[self.sceneText]
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                pygame.time.delay(300)
                self.counter += 1 
            elif len(currentTextSet) <= self.counter:
                self.sceneMove = True
                self.sceneText += 1
            testBox.setDialogue(currentTextSet, self.counter)
        elif len(dialogueList) <= self.sceneText:
            self.gameStatus.setState("runLevel")

        pygame.display.flip()
