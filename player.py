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
        self.left = False
        self.right = False
    
    def playerHitbox(self):
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

        

    #Changes the x and y coordinates of the player. 
    #Requires the current key input, the width boundary and the height boundary of the window
    def movement(self, keys, widthBounds, heightBounds):
        #Checks the key and moves the character correspondingly
            if keys[pygame.K_a] and self.x > self.speed:
                self.x -= self.speed
                left = False
                right = True
                #current_set = 1
            elif keys[pygame.K_d] and self.x < widthBounds:
                self.x += self.speed
                left = True
                right = False
                #current_set = 1
            elif keys[pygame.K_w] and self.y > self.speed:
                self.y -= self.speed
                left = True
                right = False
                #current_set = 1
            elif keys[pygame.K_s] and self.y < heightBounds:
                self.y += self.speed
                left = True
                right = False
                #current_set = 1
            #else:
                #current_set = 0