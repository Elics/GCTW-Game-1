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
            self.gameStatus.setState("level")

#Runs the collection game mode. To run, I simply toggle the variable collectionMode
class runLevel():
    def __init__(self, gameStatus):
        self.gameStatus = gameStatus 
    def run(self):
        self.collectionMode = True
        
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
        press_space = self.sub.render("Want to try again? Press SPACE", True, "white")
        self.display.blit(end, (300, 300))
        self.display.blit(press_space, (320, 400))
        pygame.display.flip()
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.gameStatus.setState("level")
