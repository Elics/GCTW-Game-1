import pygame
import random

#Defines a trash object. The dimensions are based on the player's dimensions
#The trash object should be smaller than the player
#widthBounds and heightBounds dictate where the trash can spawn

levelOneTrash = ["images\\Trash\\07-Styrofoam.png",
                 "images\\Trash\\08-Plastic.png",
                 "images\\Trash\\11-Bottle.png",
                 "images\\Trash\\14-Twigs.png",
                 "images\\Trash\\25-FilterCigarette.png"
                 ]

class Trash():
    def __init__(self, playerWidth, playerHeight, widthLowerBound, widthUpperBound, heightLowerBound, heightUpperBound):
        #Select random trash and load it in
        self.image = pygame.image.load(levelOneTrash[random.randint(0, len(levelOneTrash) - 1)])
        
        #Scale the trash base on the player's width and height
        #NOTE: Since the trashsprites are likely drawn by hand, the random generation of the dimensions will be replaced
        self.width = int(playerWidth * 0.8)
        self.height =  int(playerHeight* 0.8)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
    
        #Randomly generate the xy-coordinates
        self.x = random.randint(widthLowerBound, widthUpperBound)
        self.y = random.randint(heightLowerBound, heightUpperBound)

        #Initialize trash sprite hitbox
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

        #Chances of the trash being treasure (1/10 or 10%)
        self.treasure = random.randint(1, 10)

