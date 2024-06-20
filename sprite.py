import pygame

#~~ Animation Set Lists ~~
standFront = [] 
standRight = []
standBack = []
walkFront = []
walkRight = []
walkBack = []
#All inverted animations will be appended at the end
walkLeft = []

#Final Animations in single list
animations = [standFront, standRight, standBack, walkFront, walkRight, walkBack, walkLeft]

#The amount of frames for each set of animations (ex. walking takes 4 frames)
frameSet = [2, 2, 2, 4, 4, 4]

#Creates sprite animations. Takes any image file and cut up the files to get single images/frames.
#getAnimations() = Takes a whole set of frames and insert them into the corresponding lists. 
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
    
    #Get the whole set of frames for each animations and insert to corresponding animation set list
    def getAnimations(self):
        #Index of the current animation set
        count = 0

        #Goes through frame set to collect the proper amount of frames per row
        #Ex. Walk Animation = 4 frames, Splice the image in a row 4 times
        for set in frameSet:
            for i in range(set):
                animations[count].append(self.getFrame(i, 0, count * 32, 32, 32, self.scale))
            count += 1

        #For inverted animations, such as walkLeft
        #Add the number of frames to frameSets to be tracked
        frameSet.append(4) 
        #Then loop through each walkRight frames and invert them horizontally for a walkRight
        for frame in walkRight:
            walkLeft.append(pygame.transform.flip(frame, True, False))

        #Update all animation sets and return the whole list 
        return animations
    
    #Return the frameSet list
    def getFrameSet(self):
        return frameSet

#Attempt to move all animation methods in the sprite class
#Currently not working as there is no way to track the ticks properly, as well as updating the currentFrame 
#I will try to go back and optimize this portion later
    # #~~~ Update frame animation ~~~
    def frameTiming(self, currentTime, previousTime, frameCoolDown, currentFrame, currentSet):
        if currentTime - previousTime >= frameCoolDown:
            currentFrame += 1   
            previousTime = currentTime
        #When all frames are played, reset to the starting frame
        if currentFrame >= frameSet[currentSet]:
            currentFrame = 0
        return (currentFrame, previousTime)


