import pygame
import random
import time
import collector
from cut_scene import IntroCutScene, LevelCompletedCutScene
from trash import Trash
from treasure import Treasure
from collector import Collector
from menu import Menu
from enemy import Enemy

pygame.init()

SCREENHEIGHT = 700
SCREENWIDTH = 900
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("First Game")

# Images
walkRight = [pygame.image.load('Images/Collectors/R1.png'), pygame.image.load('Images/Collectors/R2.png'), pygame.image.load('Images/Collectors/R3.png'), pygame.image.load('Images/Collectors/R4.png')]
walkLeft = [pygame.image.load('Images/Collectors/L1.png'), pygame.image.load('Images/Collectors/L2.png'), pygame.image.load('Images/Collectors/L3.png'), pygame.image.load('Images/Collectors/L4.png')]
bg = pygame.image.load('Images/Backgrounds/beach.png')

# Load enemy image
enemy_image = pygame.image.load('Images/Trashes/Cabbage.png').convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (100, 100))

# Create enemy group
enemy_group = pygame.sprite.Group()

# Load and scale images
BananaSkin = pygame.image.load('Images/Trashes/Rope.png').convert_alpha()
BananaSkin = pygame.transform.scale(BananaSkin, (50, 50))  # Scale the image to desired size

TreasureImage = pygame.image.load('Images/Trashes/Apple.png').convert_alpha()
TreasureImage = pygame.transform.scale(TreasureImage, (25, 25))  # Scale the image to desired size

# Initialize Trash and Treasure Groups
trash_group = pygame.sprite.Group()
treasure_group = pygame.sprite.Group()
last_treasure_spawn_time = time.time()
treasure_spawn_interval = 10  # seconds

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
    for treasure in treasure_group:
        treasure.draw(screen)
    
    enemy_group.draw(screen)  # Draw the enemy group
    pygame.display.update()

# Function to get a valid position for trash within defined boundaries
def get_valid_position(existing_sprites, x_min, x_max, y_min, y_max):
    while True:
        x = random.randint(x_min, x_max)
        y = random.randint(y_min, y_max)
        new_rect = pygame.Rect(x, y, 25, 25)
        if not any(new_rect.colliderect(sprite.rect) for sprite in existing_sprites):
            return (x, y)

# Main game loop
running = True
man = Collector(210, 410, 64, 64, walkRight, walkLeft)
menu = Menu(screen, font)
game_state = "cutscene"
intro_cutscene = IntroCutScene(screen, font)
level_completed_cutscene = LevelCompletedCutScene(screen, font)

trash_generation_duration = 30000  # 30 seconds in milliseconds
trash_generation_start_time = pygame.time.get_ticks()
enemy_spawn_time = None

# Define boundaries for trash generation (bottom half of the screen)
trash_y_min = SCREENHEIGHT // 2
trash_y_max = SCREENHEIGHT - 25
trash_x_min = 0
trash_x_max = SCREENWIDTH - 25

while running:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == 'menu':
                play_button_rect, options_button_rect, quit_button_rect = menu.draw_menu()
                if play_button_rect.collidepoint(event.pos):
                    game_state = "play"
                    enemy_spawn_time = time.time() + 5  # Set enemy spawn time to 5 seconds from now
                elif options_button_rect.collidepoint(event.pos):
                    game_state = "options"
                elif quit_button_rect.collidepoint(event.pos):
                    running = False
            elif game_state == "play":
                menu_text_rect = pygame.Rect(10, 10, 100, 50)
                if menu_text_rect.collidepoint(event.pos):
                    game_state = 'menu'
            elif game_state == 'options':
                back_button_rect = menu.draw_options()
                if back_button_rect.collidepoint(event.pos):
                    game_state = 'menu'

    if game_state == 'cutscene':
        if not intro_cutscene.update():
            game_state = 'menu'
        intro_cutscene.draw()
    elif game_state == 'menu':
        menu.draw_menu()
    elif game_state == "play":
        man.update()

        # Check if it's time to spawn the enemy
        if enemy_spawn_time and time.time() > enemy_spawn_time:
            waypoints = Enemy.generate_random_waypoints(SCREENWIDTH, SCREENHEIGHT)
            enemy_group.add(Enemy(waypoints, enemy_image))
            enemy_spawn_time = None  # Ensure enemy is only spawned once

        # Check for collisions with trash
        for trash in trash_group:
            if man.rect.colliderect(trash.rect):
                trash.hit()
                trash.kill()
                score += 10

        # Check for collisions with treasure
        for treasure in treasure_group:
            if man.rect.colliderect(treasure.rect):
                treasure.hit()
                treasure.kill()
                score += 50

        # Check for collisions with enemies
        for enemy in enemy_group:
            if man.rect.colliderect(enemy.rect):
                # Handle collision with enemy (e.g., decrease score, end game, etc.)
                #collector.kill()
                print("Collision with enemy!")
                # Implement your collision logic here

        # Update treasure group and remove expired treasures
        for treasure in treasure_group:
            treasure.update()

        # Spawn new treasure if enough time has passed
        current_time = time.time()
        if current_time - last_treasure_spawn_time > treasure_spawn_interval:
            new_treasure = Treasure(get_valid_position(trash_group.sprites() + treasure_group.sprites(), trash_x_min, trash_x_max, trash_y_min, trash_y_max), TreasureImage, duration=5)
            treasure_group.add(new_treasure)
            last_treasure_spawn_time = current_time

        # Generate trash for 30 seconds
        elapsed_time = pygame.time.get_ticks() - trash_generation_start_time
        if elapsed_time < trash_generation_duration:
            if len(trash_group) < 8:
                new_trash = Trash(get_valid_position(trash_group.sprites() + treasure_group.sprites(), trash_x_min, trash_x_max, trash_y_min, trash_y_max), BananaSkin)
                trash_group.add(new_trash)

        if not trash_group and elapsed_time >= trash_generation_duration:
            game_state = 'level_completed'

        # Update and draw enemy group
        enemy_group.update()

        redrawGameWindow()
    elif game_state == "level_completed":
        if not level_completed_cutscene.update():
            game_state = 'menu'
        level_completed_cutscene.draw()

pygame.quit()
