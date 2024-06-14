import pygame

class Sprite():
    #Get the image file and load it as the sprite sheet
    def __init__(self, filename):
        self.filename = filename
        self.spriteSheet = pygame.image.load(filename)

    #Base on the given file, take a portion of it to create a frame
    #Frame Number, x-coord, y-coord, width, height, scale image
    def getFrame(self, order, x, y, w, h, scale):
        #Create empty image (rectangle) which will hold the sprite frame
        frame = pygame.Surface((w,h))

        #Maintain the transparency of the sprite
        frame.set_colorkey((0,0,0))

        #Get the spriteSheet, location of the surface, and the portion of the spriteSheet (row)
        frame.blit(self.spriteSheet, (0,0), ((order*w),y,w,h))

        #Increasing the scale of the picture (sprite image, [width, height])
        frame = pygame.transform.scale(frame, (w * scale, h * scale))
        return frame

