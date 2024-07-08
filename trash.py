import pygame
import random

#Defines a trash object. The dimensions are based on the player's dimensions
#The trash object should be smaller than the player
#widthBounds and heightBounds dictate where the trash can spawn

class Trash():
    def __init__(self, playerWidth, playerHeight, widthLowerBound, widthUpperBound, heightLowerBound, heightUpperBound):
        #Randomly generate width and height
        #NOTE: Since the trashsprites are likely drawn by hand, these random generation of the dimensions will be replaced
        self.width = random.randint(20, playerWidth - 20)
        self.height =  random.randint(20, playerHeight - 20)

        #Randomly generate the xy-coordinates
        self.x = random.randint(widthLowerBound, widthUpperBound)
        self.y = random.randint(heightLowerBound, heightUpperBound)

        #Initialize trash sprite hitbox
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

        #Chances of the trash being treasure (1/5 or 20%)
        self.treasure = random.randint(1, 5)

