#This file manages the gameStatus, which is the cutscenes or levels to be played
#Each level or cutscene, which will be called states, is defined in its own class
import pygame

#Sets the game status, return the current status, and set the status
class gameStatus():
    def __init__(self, currentState):
        self.currentState = currentState
        self.previousState = currentState
    def getState(self):
        return self.currentState
    def setState(self, changeState):
        self.currentState = changeState
    #Question methods to retrieve previous state
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
        self.display.fill("white")
        title_txt = self.fontSet[0].render("Environmental", True, "black")
        press_space_txt = self.fontSet[1].render("Press SPACE to start/Press M for the menu", True, "Black")

        self.display.blit(title_txt, (200, 150))
        self.display.blit(press_space_txt, (200, 250))

        pygame.display.flip()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            pygame.time.delay(300)
            self.gameStatus.setState("runLevel")

#Menu Screen
class menuScreen():
    def __init__(self, display, gameStatus, fontSet):
        self.display = display
        self.gameStatus = gameStatus
        self.fontSet = fontSet

    def run(self):
        self.display.fill("gray")
        title_txt = self.fontSet[0].render("MENU", True, "white")
        notice_txt = self.fontSet[1].render("Under Construction: Press Q to enter exit scene", True, "red")

        self.display.blit(title_txt, (600, 300))
        self.display.blit(notice_txt, (200, 400))

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
        skip_txt = self.fontSet[1].render("Skip Upgrades", False, "Red")

        #Render the Shop Text & Instructions
        self.display.blit(title_txt, (400, 0))
        self.display.blit(coins_txt, (800, 20))
        self.display.blit(cost_txt, (250, 150))
        self.display.blit(instructions_txt, (50, 550))

        #When a button is selected, highlight its corresponding rectangle
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
        self.display.fill("black")
        end_txt = self.fontSet[0].render("Game Over", True, "white")
        press_space_txt = self.fontSet[1].render("Press SPACE to go back to Start Screen", True, "white")
        note_txt = self.fontSet[1].render("All upgrades are kept until you press X!", True, "white")

        self.display.blit(end_txt, (300, 300))
        self.display.blit(press_space_txt, (320, 400))
        self.display.blit(note_txt, (320, 450))

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

    #Text limit is 50
    def setDialogue(self, textSet, counter):
        self.dialogueBox = pygame.Rect(0, 420, 1000, 200)
        pygame.draw.rect(self.display, self.color, self.dialogueBox)
        self.display.blit(self.animationSet[0][0], (-80, 350))

        instructions_txt = self.fontSet[1].render("Press SPACE to continue", True, "white")
        self.display.blit(instructions_txt, (800, 550))
        dialogue_txt = self.fontSet[0].render(textSet[counter], True, "white")
        self.display.blit(dialogue_txt, (200, 500))
        

class sceneOne():
    def __init__(self, display, gameStatus, fontSet, animationSet, dialogueSet):
        self.display = display
        self.gameStatus = gameStatus 
        self.fontSet = fontSet
        self.animationSet = animationSet
        self.dialogueSet = dialogueSet
        self.subcounter = 0

    def run(self):
        self.display.fill("white")
        testBox = dialogueBox(self.display, "black", self.dialogueSet, self.fontSet)
        textSet = ["Hello there!", "Let's go to the beach!"]
        textTwo = ["Hmm, it is pretty hard to find a spot"]
        # testBox.setDialogue()

        if pygame.key.get_pressed()[pygame.K_SPACE] and len(textSet) - 1 > self.subcounter:
            self.subcounter += 1
        elif pygame.key.get_pressed()[pygame.K_SPACE] and len(textSet) - 1 == self.subcounter:
            self.gameStatus.setStatus("sceneOnept2")


        pygame.display.flip()
