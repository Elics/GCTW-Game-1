import pygame

#~~~ Create Game Window ~~~
class Window():
    def __init__(self, windowName):
        #Window Variables
        self.windowSizes = [(800, 600), (1000, 600), (1200, 700)]
        self.filesList = [
            ("images\\backgrounds\\Menu.png", None),
            ("images\\backgrounds\\Start.png", None),
            ("images\\backgrounds\\Quit.png", None),
            ("images\\backgrounds\\Beach.png", 200),
            ("images\\backgrounds\\Shop1.png", None),
            ("images\\backgrounds\\Shop2.png", None),
            ("images\\backgrounds\\Shop3.png", None)
            ]
        self.backgroundList = []
        self.screenSizeIndex = 1

        #Setting up default window dimensions
        self.winWidth = self.windowSizes[1][0]
        self.winHeight = self.windowSizes[1][1]
        self.currentWindow = pygame.display.set_mode(self.windowSizes[1])
        
        #Set window name
        pygame.display.set_caption(windowName)

        #Add to backgroundsList
        Window.addBackground(self)
    
    #Update the window size and corresponding variables
    def setWindow(self):
        #Update window dimensions based on selection
        self.winWidth = self.windowSizes[self.screenSizeIndex][0]
        self.winHeight = self.windowSizes[self.screenSizeIndex][1]
        self.currentWindow = pygame.display.set_mode(self.windowSizes[self.screenSizeIndex])
        

    #~~ Image Backgrounds ~~
        #Start Screen: Start.png, None
        #Menu Screen: Menu.png, None
        #Quit Screen: Quit.png, None
        #Level 1: Beach.png, Lower Bounds = 200
    #Converts the images and resize them. Then adds them to the backgroundList for use
    def addBackground(self):
        for image in self.filesList:
            background = pygame.image.load(image[0])
            background = pygame.transform.smoothscale(background.convert_alpha(), (self.winWidth, self.winHeight))
            self.backgroundList.append((background, image[1]))

    #Update the scale of all backgrounds in the backgroundsList
    def updateBackground(self):
        for i in range(len(self.backgroundList)):
            tempList = list(self.backgroundList[i])
            
            tempList[0] = pygame.transform.smoothscale(tempList[0].convert_alpha(), (self.winWidth, self.winHeight))
            self.backgroundList[i] = tuple(tempList)
            
    #Add text/images to the screen to the screen
    def addUI(self, object, coordinates):
        #Create a temporary surface to scale the text/image
        temp_surface = pygame.Surface((self.windowSizes[1][0], self.windowSizes[1][1]), pygame.SRCALPHA, 32)
        #Add the text/image to the temp surface
        temp_surface.blit(object, coordinates)
        #Scale the temp surface to the current window size
        scaled_surface = pygame.transform.scale(temp_surface, (self.winWidth, self.winHeight))
        #Display the temp surface to the main window
        self.currentWindow.blit(scaled_surface, (0,0))

            
