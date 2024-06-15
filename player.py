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
    
    #Defines the player's hitbox
    #I created this as a separate method as the hitbox is constantly changing when the character moves
    def playerHitbox(self, scale):
        self.hitbox = pygame.Rect(self.x + scale*11, self.y + scale*9, self.width*0.3, self.height*0.45)   

    #Changes the x and y coordinates of the player. 
    #Requires the current key input, the width boundary and the height boundary of the window
    def movement(self, keys, widthBounds, heightBounds):
        #Checks the key and moves the character correspondingly
            if keys[pygame.K_a] and self.hitbox[0] > self.speed :
                self.x -= self.speed
                left = False
                right = True
                self.currentSet = 1
            elif keys[pygame.K_d] and self.hitbox[0] < widthBounds:
                self.x += self.speed
                left = True
                right = False
                self.currentSet = 2
            elif keys[pygame.K_w] and self.hitbox[1] > self.speed:
                self.y -= self.speed
                left = True
                right = False
                self.currentSet = 3
            elif keys[pygame.K_s] and self.hitbox[1] < heightBounds:
                self.y += self.speed
                left = True
                right = False
                self.currentSet = 4
            else:
                self.currentSet = 0