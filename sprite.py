import pygame

#All animation sets
standFront = []
standLeft = []
standBack = []
walkFront = []
walkLeft = []
walkBack = []
animations = [standFront, standLeft, standBack, walkFront, walkLeft, walkBack]
#The amount of frames for each set of animations (ex. walking takes 4 frames)
frameSet = [2, 2, 2, 4, 4, 4]


class Sprite():
    #Get the image file and load it as the sprite sheet
    def __init__(self, filename):
        self.filename = filename
        self.spriteSheet = pygame.image.load(filename)

    #Base on the given file, take a portion of it to create a frame
    #Frame Number, x-coord, y-coord, width, height, scale image
    def getFrame(self, order, x, y, w, h, scale):
        #Keep the scale as an attribute
        self.scale = scale

        #Create empty image (rectangle) which will hold the sprite frame
        frame = pygame.Surface((w,h))

        #Maintain the transparency of the sprite
        frame.set_colorkey((0,0,0))

        #Get the spriteSheet, location of the surface, and the portion of the spriteSheet (row)
        frame.blit(self.spriteSheet, (0,0), ((order*w),y,w,h))

        #Increasing the scale of the picture (sprite image, [width, height])
        frame = pygame.transform.scale(frame, (w * scale, h * scale))
        return frame
    
    #Get the whole set of frames for each animations
    def getAnimations(self):
        count = 0
        for set in frameSet:
            for i in range(set):
                animations[count].append(self.getFrame(i, 0, count * 32, 32, 32, self.scale))
            # print("Animation: " + str(count) + ": " + str(animations[count]))
            count = count + 1
        return animations
    
    def getFrameSet(self):
        return frameSet

    # #~~~ Update frame animation ~~~
    # def frameTiming(self, currentFrame, setNumber):
    #     #Get the current ingame time
    #     currentTime = pygame.time.get_ticks()
        
    #     #Check the duration between frames. If the frame cooldown is over, get the next frame and reset the cooldown
    #     if currentTime - previousTime >= frameCoolDown:
    #         currentFrame += 1
    #         previousTime = currentTime
    #     #When all frames are played, reset to the starting frame
    #     if currentFrame >= frameSet[setNumber]:
    #         currentFrame = 0


