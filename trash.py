import pygame
import random

#Defines a trash object. The dimensions are based on the player's dimensions
#The trash object should be smaller than the player
#widthBound and heightBound are the window boundaries. These dictate where the trash can spawn
class Trash():
    def __init__(self, playerWidth, playerHeight, playerSpeed, widthBound, heightBound):
        self.width = random.randint(20, playerWidth - 20)
        self.height =  random.randint(20, playerHeight - 20)
        self.x = random.randint(playerSpeed, widthBound)
        self.y = random.randint(playerSpeed, heightBound)
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

