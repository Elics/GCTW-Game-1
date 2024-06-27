import pygame
import random
from cut_scene import IntroCutScene

pygame.init()

SCREENHEIGHT = 500
SCREENWIDTH = 500
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("First Game")

# Images
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

score = 0
font = pygame.font.SysFont('poppins', 30)

# Colors
TEXT_COL = (244, 244, 244)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Text rendering function
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Creating trash collector
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
        self.walkCount = 0
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect(center=(250, 250))

    def draw(self, screen):
        if self.walkCount + 1 >= 12:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                screen.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
            elif self.right:
                screen.blit(walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:
            if self.right:
                screen.blit(walkRight[0], (self.x, self.y))
            else:
                screen.blit(walkLeft[0], (self.x, self.y))

    def update(self, cut_scene_manager):
        if self.rect.centerx > SCREENWIDTH:
            cut_scene_manager.start_cut_scene(IntroCutScene(self))

        if cut_scene_manager.cut_scene is None:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                self.rect.x -= 5
            if pressed[pygame.K_RIGHT]:
                self.rect.x += 5

# The trash
class Trash(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.height, self.width))

    def hit(self):
        print('collected')

trashes = []
for _ in range(8):
    trash = Trash(random.randint(0, SCREENWIDTH - 25), random.randint(0, SCREENHEIGHT - 25), 25, 25)
    trashes.append(trash)

# Menu function
def draw_menu():
    screen.fill(BLACK)
    title = font.render("Main Menu", True, WHITE)
    play_button = font.render("Play", True, WHITE)
    options_button = font.render("Options", True, WHITE)
    quit_button = font.render("Quit", True, WHITE)
    
    screen.blit(title, (SCREENWIDTH // 2 - title.get_width() // 2, 50))
    screen.blit(play_button, (SCREENWIDTH // 2 - play_button.get_width() // 2, 150))
    screen.blit(options_button, (SCREENWIDTH // 2 - options_button.get_width() // 2, 200))
    screen.blit(quit_button, (SCREENWIDTH // 2 - quit_button.get_width() // 2, 250))
    
    pygame.display.update()
    return play_button.get_rect(topleft=(SCREENWIDTH // 2 - play_button.get_width() // 2, 150)), options_button.get_rect(topleft=(SCREENWIDTH // 2 - options_button.get_width() // 2, 200)), quit_button.get_rect(topleft=(SCREENWIDTH // 2 - quit_button.get_width() // 2, 250))

# Function to handle options screen
def draw_options():
    screen.fill(BLACK)
    title = font.render("Options", True, WHITE)
    back_button = font.render("Back", True, WHITE)
    
    screen.blit(title, (SCREENWIDTH // 2 - title.get_width() // 2, 50))
    screen.blit(back_button, (SCREENWIDTH // 2 - back_button.get_width() // 2, 250))
    
    pygame.display.update()
    return back_button.get_rect(topleft=(SCREENWIDTH // 2 - back_button.get_width() // 2, 250))

# Function to redraw game window
def redrawGameWindow():
    screen.blit(bg, (0, 0))
    text = font.render("Score: " + str(score), 1, BLUE)
    screen.blit(text, (390, 10))
    menu_text = font.render("Menu", 1, BLUE)
    screen.blit(menu_text, (10, 10))
    man.draw(screen)
    for trash in trashes:
        trash.draw(screen)
    pygame.display.update()
    return menu_text.get_rect(topleft=(10, 10))


# This makes the window stay -- main
running = True
man = Collector(210, 410, 64, 64)
cut_scene_manager = IntroCutScene(screen, font)
game_state = "cutscene"
intro_cutscene = IntroCutScene(screen, font)

while running:
    clock.tick(27)



    if game_state == 'cutscene':
        if not intro_cutscene.update():
            game_state = 'menu'
        intro_cutscene.draw()
    elif game_state == 'menu':
        play_button_rect, options_button_rect, quit_button_rect = draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    game_state = "play"
                elif options_button_rect.collidepoint(event.pos):
                    game_state = "options"
                elif quit_button_rect.collidepoint(event.pos):
                    running = False
    elif game_state == "play":
        menu_text_rect = redrawGameWindow()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_text_rect.collidepoint(event.pos):
                    game_state = 'menu'

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and man.x > man.vel:
            man.x -= man.vel
            man.left = True
            man.right = False
            man.standing = False
        elif keys[pygame.K_RIGHT] and man.x < SCREENWIDTH - man.width - man.vel:
            man.x += man.vel
            man.left = False
            man.right = True
            man.standing = False
        elif keys[pygame.K_SPACE]:
            game_state = 'menu'
        else:
            man.standing = True

        if keys[pygame.K_UP] and man.y > man.vel:
            man.y -= man.vel
        if keys[pygame.K_DOWN] and man.y < SCREENHEIGHT - man.height - man.vel:
            man.y += man.vel

        for trash in trashes:
            if man.x < trash.x + trash.width and man.x + man.width > trash.x:
                if man.y < trash.y + trash.height and man.y + man.height > trash.y:
                    trash.x = random.randint(0, SCREENWIDTH - trash.width)
                    trash.y = random.randint(0, SCREENHEIGHT - trash.height)
                    trash.hit()
                    score += 10
    elif game_state == 'options':
        back_button_rect = draw_options()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    game_state = 'menu'
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
pygame.quit()
