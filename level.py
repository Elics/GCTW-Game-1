#This file manages the gameStatus, which is the cutscenes or levels to be played
#Each level or cutscene, which will be called states, is defined in its own class
import pygame

#Sets the game status, return the current status, and set the status
class gameStatus():
    def __init__(self, currentState):
        self.currentState = currentState
    def getState(self):
        return self.currentState
    def setState(self, changeState):
        self.currentState = changeState

#The starting screen
class startGame():
    def __init__(self, display, gameStatus, title, subtitle):
        self.display = display
        self.gameStatus = gameStatus
        self.font = title
        self.sub = subtitle
    def run(self):
        self.display.fill("white")
        title = self.font.render("Environmental", True, "black")
        press_space = self.sub.render("Press SPACE to start", True, "Black")
        self.display.blit(title, (200, 150))
        self.display.blit(press_space, (400, 250))
        pygame.display.flip()
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            pygame.time.delay(300)
            self.gameStatus.setState("level")

#Displays Upgrade Shop after every level
class upgradeShop():
    def __init__(self, display, gameStatus, font, subfont, speed, time):
        self.display = display
        self.gameStatus = gameStatus
        self.font = font
        self.subfont = subfont
        self.speedBuff = speed
        self.timeBuff = time
    def run(self):
        self.display.fill("#E5FFB8")
        title = self.font.render("Shop", True, "black")
        instructions = self.subfont.render("Press SPACE to continue/Press Q to Quit", True, "black")

        speedRect = pygame.Rect(100, 300, 325, 50)
        timeRect = pygame.Rect(600, 300, 325, 50)
        speed = self.subfont.render("Current Speed: " + str(self.speedBuff), False, "black")
        time = self.subfont.render("Current Timelimit: " + str(self.timeBuff), False, "black")


        self.display.blit(title, (400, 0))
        self.display.blit(instructions, (10, 600))

        pygame.draw.rect(self.display, "white", speedRect)
        self.display.blit(speed, (100, 300))

        pygame.draw.rect(self.display, "white", timeRect)
        self.display.blit(time, (600, 300))
    

        pygame.display.flip()

        if pygame.key.get_pressed()[pygame.K_q]:
            self.gameStatus.setState("end")
        
#The ending scene
class gameEnd():
    def __init__(self, display, gameStatus, title, subtitle):
        self.display = display
        self.gameStatus = gameStatus 
        self.font = title
        self.sub = subtitle
    def run(self):
        self.display.fill("black")
        end = self.font.render("Game Over", True, "white")
        press_space = self.sub.render("Press SPACE to go back to Main Menu", True, "white")
        self.display.blit(end, (300, 300))
        self.display.blit(press_space, (320, 400))
        pygame.display.flip()
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            pygame.time.delay(300)
            self.gameStatus.setState("start")

            
#Runs the collection game mode. To run, I simply toggle the variable collectionMode
class runLevel():
    def __init__(self, gameStatus):
        self.gameStatus = gameStatus 
    def run(self):
        self.collectionMode = True
