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
    def __init__(self, display, gameStatus, font, subfont):
        self.display = display
        self.gameStatus = gameStatus
        self.font = font
        self.subfont = subfont

    def run(self):
        self.display.fill("white")
        title_txt = self.font.render("Environmental", True, "black")
        press_space_txt = self.subfont.render("Press SPACE to start/Press M for the menu", True, "Black")

        self.display.blit(title_txt, (200, 150))
        self.display.blit(press_space_txt, (200, 250))

        pygame.display.flip()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            pygame.time.delay(300)
            self.gameStatus.setState("level")

class menuScreen():
    def __init__(self, display, gameStatus, font, subfont):
        self.display = display
        self.gameStatus = gameStatus
        self.font = font
        self.subfont = subfont

    def run(self):
        self.display.fill("gray")
        title_txt = self.font.render("MENU", True, "white")
        notice_txt = self.subfont.render("The MENU screen is currently under construction", True, "red")

        self.display.blit(title_txt, (600, 300))
        self.display.blit(notice_txt, (200, 400))

        pygame.display.flip()


#Displays Upgrade Shop after every level
class upgradeShop():
    def __init__(self, display, gameStatus, font, subfont, speed, time):
        self.display = display
        self.gameStatus = gameStatus
        self.font = font
        self.subfont = subfont
        self.speedBuff = speed
        self.timeBuff = time
        self.selected = None

    def run(self):
        self.display.fill("#E5FFB8")
        title_txt = self.font.render("Shop", True, "black")
        instructions_txt = self.subfont.render("Press SPACE to continue/Press Q to Quit", True, "black")

        speedRect = pygame.Rect(100, 300, 325, 50)
        timeRect = pygame.Rect(600, 300, 325, 50)
        speed_txt = self.subfont.render("Current Speed: " + str(self.speedBuff), False, "black")
        time_txt = self.subfont.render("Current Timelimit: " + str(self.timeBuff), False, "black")
        speedUpgrade_txt = self.subfont.render("Speed +10", False, "black")
        timeUpgrade_txt = self.subfont.render("Time +10", False, "black")

        self.display.blit(title_txt, (400, 0))
        self.display.blit(instructions_txt, (50, 550))

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

        pygame.display.flip()
        
#The ending scene
class gameEnd():
    def __init__(self, display, gameStatus, font, subfont):
        self.display = display
        self.gameStatus = gameStatus 
        self.font = font
        self.subfont = subfont

    def run(self):
        self.display.fill("black")
        end_txt = self.font.render("Game Over", True, "white")
        press_space_txt = self.subfont.render("Press SPACE to go back to Main Menu", True, "white")
        note_txt = self.subfont.render("All upgrades are kept until you press X!", True, "white")

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
        self.collectionMode = True
