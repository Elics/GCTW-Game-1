import pygame

#Initialize pygame program
pygame.init()

#~~~ Create Game Window ~~~
#Window Dimension variables
winWidth = 500
winHeight = 500

#Initialize window 
win = pygame.display.set_mode((winWidth, winHeight))

#Create name of the window
pygame.display.set_caption("Our Game")


#~~~ Main Loop ~~~
#Toggles the Running status of the game (on/off)
run = True
while run:
    #Checks for any player interaction while running (mouse clicks, keyboard, etc.)
    for event in pygame.event.get():
        #Handle scenario when the player closes the window (X)
        if event.type == pygame.QUIT:
            run = False
        
#When the game is off, close the pygame program as well.
pygame.quit()
