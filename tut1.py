import pygame
import random
pygame.init()



SCREENHEIGHT =480
SCREENWIDTH= 500
screen= pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
pygame.display.set_caption("First Game")

#images
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

score = 0
font =pygame.font.SysFont('poppins', 30)





#color
#BG =    (50,50,50)
GREEN = (0,255,0)
BLUE =  (0,0,255)
#RED =   (255,0,0)





#creating trash collector
class Collector(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 6
        self.left = False
        self.right = False
        self.standing = True
       # self.hitbox =(self.x +20, self.y, 28, 60)
        self.walkCount = 0


    def draw(self,screen):
        if self.walkCount +1 >= 27:
            self.walkCount = 0


        if not(self.standing):
            if self.left:
                screen.blit(walkLeft[self.walkCount//27],(self.x, self.y))

            elif self.right:
                screen.blit(walkRight[self.walkCount//27], (self.x, self.y))

            self.walkCount += 1
            
        else:
            if self.right:
                screen.blit(walkRight[0],(self.x, self.y))

            else:
                screen.blit(walkLeft[0],(self.x, self.y))

        #self.hitbox = (self.x +20, self.y, 28, 60)
        #pygame.draw.rect(screen,(255,0,0), self.hitbox, 2)

#the trash
class Trash(object):
    def __init__(self, x, y, width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        #self.vel = 3
        #self.hitbox =(self.x +20, self.y, 28, 60)
    
    def draw(self, screen):
        pygame.draw.rect(screen,BLUE, (self.x, self.y,self.height, self.width))

    def hit(self):
        print('collected')

trashes =[]
for _ in range(8):
    trash = Trash(random.randint(0, SCREENWIDTH - 25), random.randint(0, SCREENHEIGHT - 25), 25, 25)
    trashes.append(trash) 

#function
def redrawGameWindow():
    screen.blit(bg,(0,0))
    text = font.render("Score: "+ str(score), 1, BLUE)
    screen.blit(text, (390, 10))
    man.draw(screen)
    for trash in trashes:
        trash.draw(screen)
    pygame.display.update()
   
#this makes the window stays -- main
running = True
man = Collector(210,410,64,64)

while running:
    clock.tick(27)
    


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False

    elif keys[pygame.K_RIGHT] and man.x < SCREENWIDTH - man.width- man.vel:
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    
    else:
        man.standing =True

    if keys[pygame.K_UP] and man.y > man.vel:
           man.y -= man.vel

    if keys[pygame.K_DOWN] and man.y < SCREENWIDTH - man.height - man.vel:
            man.y += man.vel
        

    for trash in trashes:
        if man.x < trash.x + trash.width and man.x + man.width > trash.x:
            if man.y < trash.y + trash.height and man.y + man.height > trash.y:
                trash.x = random.randint(0, SCREENWIDTH - trash.width)
                trash.y = random.randint(0, SCREENHEIGHT - trash.height)
                trash.hit()
                score += 10
   
    
    
    redrawGameWindow()

pygame.quit()