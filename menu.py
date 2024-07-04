import pygame

# Menu function
def draw_menu(screen, font):
    screen.fill((0, 0, 0))
    title = font.render("Main Menu", True, (255, 255, 255))
    play_button = font.render("Play", True, (255, 255, 255))
    options_button = font.render("Options", True, (255, 255, 255))
    quit_button = font.render("Quit", True, (255, 255, 255))
    
    screen.blit(title, (500 // 2 - title.get_width() // 2, 50))
    screen.blit(play_button, (500 // 2 - play_button.get_width() // 2, 150))
    screen.blit(options_button, (500 // 2 - options_button.get_width() // 2, 200))
    screen.blit(quit_button, (500 // 2 - quit_button.get_width() // 2, 250))
    
    pygame.display.update()
    return play_button.get_rect(topleft=(500 // 2 - play_button.get_width() // 2, 150)), options_button.get_rect(topleft=(500 // 2 - options_button.get_width() // 2, 200)), quit_button.get_rect(topleft=(500 // 2 - quit_button.get_width() // 2, 250))

# Function to handle options screen
def draw_options(screen, font):
    screen.fill((0, 0, 0))
    title = font.render("Options", True, (255, 255, 255))
    back_button = font.render("Back", True, (255, 255, 255))
    
    screen.blit(title, (500 // 2 - title.get_width() // 2, 50))
    screen.blit(back_button, (500 // 2 - back_button.get_width() // 2, 250))
    
    pygame.display.update()
    return back_button.get_rect(topleft=(500 // 2 - back_button.get_width() // 2, 250))
