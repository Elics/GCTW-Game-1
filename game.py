import pygame
import random
from cut_scene import IntroCutScene, LevelCompletedCutScene
from trash import Trash
from collector import Collector
from menu import draw_menu, draw_options

pygame.init()

SCREENHEIGHT = 500
SCREENWIDTH = 500
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("First Game")

# Images
walkRight = [pygame.image.load('Images/Collectors/R1.png'), pygame.image.load('Images/Collectors/R2.png'), pygame.image.load('Images/Collectors/R3.png'), pygame.image.load('Images/Collectors/R4.png')]
walkLeft = [pygame.image.load('Images/Collectors/L1.png'), pygame.image.load('Images/Collectors/L2.png'), pygame.image.load('Images/Collectors/L3.png'), pygame.image.load('Images/Collectors/L4.png')]
bg = pygame.image.load('Images/Backgrounds/bg.jpg')

# Load and scale images
BananaSkin = pygame.image.load('Images/Trashes/BananaSkin.png').convert_alpha()
BananaSkin = pygame.transform.scale(BananaSkin, (25, 25))  # Scale the image to desired size

trash_group = pygame.sprite.Group()
for _ in range(8):
    trash = Trash((random.randint(0, SCREENWIDTH - 25), random.randint(0, SCREENHEIGHT - 25)), BananaSkin)
    trash_group.add(trash)

clock = pygame.time.Clock()

score = 0
font = pygame.font.SysFont('poppins', 30)

# Colors
TEXT_COL = (244, 244, 244)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Function to redraw game window
def redrawGameWindow():
    screen.blit(bg, (0, 0))
    text = font.render("Score: " + str(score), 1, BLUE)
    screen.blit(text, (390, 10))
    menu_text = font.render("Menu", 1, BLUE)
    screen.blit(menu_text, (10, 10))
    man.draw(screen)
    for trash in trash_group:
        trash.draw(screen)
    pygame.display.update()
    return menu_text.get_rect(topleft=(10, 10))

# Main game loop
running = True
man = Collector(210, 410, 64, 64, walkRight, walkLeft)
game_state = "play"
intro_cutscene = IntroCutScene(screen, font)
level_completed_cutscene = LevelCompletedCutScene(screen, font)

while running:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == 'cutscene':
        if not intro_cutscene.update():
            game_state = 'menu'
        intro_cutscene.draw()
    elif game_state == 'menu':
        play_button_rect, options_button_rect, quit_button_rect = draw_menu(screen, font)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    game_state = "play"
                elif options_button_rect.collidepoint(event.pos):
                    game_state = "options"
                elif quit_button_rect.collidepoint(event.pos):
                    running = False
    elif game_state == "play":
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if redrawGameWindow().collidepoint(event.pos):
                    game_state = 'menu'

        man.update()
        for trash in trash_group:
            if man.rect.colliderect(trash.rect):
                trash.kill()
                score += 10

        if not trash_group:
            game_state = 'level_completed'

        redrawGameWindow()
    elif game_state == 'options':
        back_button_rect = draw_options(screen, font)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    game_state = 'menu'
    elif game_state == "level_completed":
        if not level_completed_cutscene.update():
            game_state = 'menu'
        level_completed_cutscene.draw()

pygame.quit()
