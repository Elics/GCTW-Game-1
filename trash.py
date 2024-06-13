import pygame
import random

class Trash():
    def __init__(self, playerWidth, playerHeight, playerSpeed, widthBound, heightBound):
        self.width = random.randint(20, playerWidth - 20)
        self.height =  random.randint(20, playerHeight - 20)
        self.x = random.randint(playerSpeed, widthBound)
        self.y = random.randint(playerSpeed, heightBound)
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def collected(self, collectPile):
        return len(collectPile)