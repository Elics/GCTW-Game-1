import pygame

#Creates sprite animations. Takes any image file and cut up the files to get single images/frames.
#getAnimations() = Takes a whole set of frames and insert them into the corresponding lists. 
class Sprite():
    #Get the image file and load it as the sprite sheet
    #NOTE: Maybe make frameSet and animationSet a parameter as each animation may require a different number of frames per set
    def __init__(self, filename, scale, frameSet, animationsNumber):
        #Store file and images in file
        self.filename = filename
        self.spriteSheet = pygame.image.load(filename)
        #Keep the scale as an attribute
        self.scale = scale

        #~~ Animation Set Lists ~~
        #The amount of frames for each set of animations (ex. walking takes 4 frames)
        self.frameSet = frameSet
        #Final Animations in single list
        self.animations = []
        #Add each animation set to the list
        for i in range(animationsNumber):
            self.animations.append([])

    #Base on the given file, take a portion of it to create a single frame and display it on the screen
    #Frame Number, x-coord, y-coord, width, height, scale image
    def getFrame(self, order, x, y, w, h):
        #Create empty image (rectangle) which will hold the sprite frame
        frame = pygame.Surface((w,h))

        #Maintains the transparency of the sprite
        frame.set_colorkey((0,0,0))
        
        #Shows the single frame
        #Get the spriteSheet, location of the surface, and the portion of the spriteSheet (row)
        frame.blit(self.spriteSheet, (0,0), ((order*w),y,w,h))

        #Increasing the scale of the picture (sprite image, [width, height])
        frame = pygame.transform.scale(frame, (w * self.scale, h * self.scale))

        return frame
    
    #Get the whole set of frames for each animations and insert to corresponding animation set list
    def getAnimations(self):
        #Index of the current animation set
        setIndex = 0

        #Goes through each animation set and collects the proper amount of frames per row using frameSet list
        #Ex. Walk Animation = 4 frames, Splice the image in a row 4 times
        for set in self.frameSet:
            for i in range(set):
                self.animations[setIndex].append(self.getFrame(i, 0, setIndex * 32, 32, 32))
            setIndex += 1

        return self.animations
    
    #Get the inverted version of animations sets
    def getInvertedAnimations(self, frameNumber, animationNumber, copiedNumber):
        #For inverted animations, such as walkLeft
        #Add the number of frames to frameSets to be tracked
        self.frameSet.append(frameNumber) 
        #Then loop through each walkRight frames and invert them horizontally for a walkRight
        for frame in self.animations[animationNumber]:
            self.animations[copiedNumber].append(pygame.transform.flip(frame, True, False))

        #Update the set of animations
        return self.animations

    #Returns the currentFrame and previous tick time as a tuple. This method calculates the 
    #previous time spent on the last frame and update the current frame accordingly.
    #When all frames are shown, it will reset the current frame to 0, looping the animation again
    #~~~ Update frame animation ~~~
    def frameTiming(self, currentTime, previousTime, frameCoolDown, currentFrame, currentSet):
        if currentTime - previousTime >= frameCoolDown:
            currentFrame += 1   
            previousTime = currentTime
        #When all frames are played, reset to the starting frame
        if currentFrame >= self.frameSet[currentSet]:
            currentFrame = 0
        return (currentFrame, previousTime)


