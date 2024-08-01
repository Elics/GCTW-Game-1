import pygame
import random

#Defines a trash object. The dimensions are based on the player's dimensions
#The trash object should be smaller than the player
#widthBounds and heightBounds dictate where the trash can spawn

levelOneTrash = ["images\\Trash\\07-Styrofoam.png",
                 "images\\Trash\\08-Plastic.png",
                 "images\\Trash\\11-Bottle.png",
                 "images\\Trash\\14-Twigs.png",
                 "images\\Trash\\25-FilterCigarette.png",
                 "images\\Trash\\Treasure.png"
                 ]

class Trash():
    def __init__(self, playerWidth, playerHeight, widthLowerBound, widthUpperBound, heightLowerBound, heightUpperBound):
        #Chances of the trash being treasure (1/10 or 10%)
        self.treasure = random.randint(1, 10)

        #Randomly select trash image. If treasure, use the Treasure.png
        if self.treasure == 1:
            self.image = pygame.image.load(levelOneTrash[5])
        else:
            self.image = pygame.image.load(levelOneTrash[random.randint(0, len(levelOneTrash) - 2)])

        #Scale the trash base on the player's width and height
        self.width = int(playerWidth * 1.5)
        self.height =  int(playerHeight * 0.8)
        #Scale the image as well
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
    
        #Randomly generate the xy-coordinates
        self.x = random.randint(widthLowerBound, widthUpperBound)
        self.y = random.randint(heightLowerBound, heightUpperBound)

        #Initialize trash sprite hitbox
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
