#Creating the Player class
import pygame

class Player():

    # ~~ Character Location + Dimensions ~~
        #Character (x-coor, y-coord, width, height)
        #NOTE: Left-Right starts from 0 to 500
        #NOTE: Up-Down starts from 0 to 500 as well

    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        #This will be for the animations
        self.currentSet = 0
        self.left = False 
        self.right = False
        self.up = False
        self.down = False
    
    #Defines the player's hitbox
    #I created this as a separate method as the hitbox is constantly changing when the character moves
    def playerHitbox(self, scale):
        self.hitbox = pygame.Rect(self.x + scale*11, self.y + scale*9, self.width*0.3, self.height*0.45)   

    #Changes the x and y coordinates of the player. 
    #Requires the current key input, the width boundary and the height boundary of the window
    #Sets the animation to run as well depending on what key is pressed
    def movement(self, keys, widthLowerBounds, widthUpperBounds, heightLowerBounds, heightUpperBounds):
        #Checks the key and moves the character correspondingly
        #Left
        if keys[pygame.K_a] and self.hitbox[0] > widthLowerBounds :
            self.x -= self.speed
            self.left = False
            self.right = True
            self.down = False
            self.up = False
            self.currentSet = 6

        #Right
        elif keys[pygame.K_d] and self.hitbox[0] < widthUpperBounds:
            self.x += self.speed
            self.left = True
            self.right = False
            self.down = False
            self.up = False
            self.currentSet = 4
        
        #Down
        elif keys[pygame.K_w] and self.hitbox[1] > heightLowerBounds:
            self.y -= self.speed
            self.left = False
            self.right = False
            self.down = True
            self.up = False
            self.currentSet = 5

        #Up
        elif keys[pygame.K_s] and self.hitbox[1] < heightUpperBounds:
            self.y += self.speed
            self.left = False
            self.right = False
            self.down = False
            self.up = True
            self.currentSet = 3

        #Idle Animation
        else:
            self.currentSet = 0