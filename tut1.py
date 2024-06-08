import pygame
import random
pygame.init()
SCREENHEIGHT =900
SCREENWIDTH= 900
screen= pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
pygame.display.set_caption("First Game")
running = True

x=2500
y =250
width = 40
height = 60
vel =6
isJump =False
jumpCount = 10

actor = pygame.Rect(25,25,width,height)
trashs = []
for _ in range(8):
    trash = pygame.Rect(random.randint(0,500), random.randint(0,300),25,25)
    trashs.append(trash)


#color
BG =    (50,50,50)
GREEN = (0,255,0)
BLUE =  (0,0,255)
RED =   (255,0,0)



#this makes the window stays
while running:
    pygame.time.delay(50)
    
    
    screen.fill(BG)
    col = GREEN 
    for trash in trashs:
        if actor.colliderect(trash):
            trash.x = random.randint(0, SCREENWIDTH - trash.width)
            trash.y = random.randint(0, SCREENHEIGHT - trash.height)
    
    pygame.draw.rect(screen, col,(actor))
    for trash in trashs:
        pygame.draw.rect(screen,BLUE,trash)


    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running = False


    keys= pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and actor.x > vel:
        actor.x-=vel
    if keys[pygame.K_RIGHT] and actor.x < SCREENWIDTH - actor.width:
        actor.x += vel

    if not(isJump):
        if keys[pygame.K_UP] and actor.y>vel:
           actor.y -= vel

        if keys[pygame.K_DOWN] and actor.y < SCREENWIDTH - actor.height - vel:
            actor.y += vel
        
        if keys[pygame.K_SPACE]:
            isJump=True


    else:
        if jumpCount>=-10:
            neg =1
            if jumpCount < 0:
                neg =-1
            actor.y-=(jumpCount**2) *0.5 *neg
            jumpCount-=1

        else:
            isJump =False
            jumpCount=10        
    
    
    
    pygame.display.flip()

pygame.quit()