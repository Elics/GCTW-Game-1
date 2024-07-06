import pygame

class Menu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        title = self.font.render("Main Menu", True, (255, 255, 255))
        play_button = self.font.render("Play", True, (255, 255, 255))
        options_button = self.font.render("Options", True, (255, 255, 255))
        quit_button = self.font.render("Quit", True, (255, 255, 255))
        
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 50))
        self.screen.blit(play_button, (self.screen.get_width() // 2 - play_button.get_width() // 2, 150))
        self.screen.blit(options_button, (self.screen.get_width() // 2 - options_button.get_width() // 2, 200))
        self.screen.blit(quit_button, (self.screen.get_width() // 2 - quit_button.get_width() // 2, 250))
        
        pygame.display.update()
        return (
            play_button.get_rect(topleft=(self.screen.get_width() // 2 - play_button.get_width() // 2, 150)),
            options_button.get_rect(topleft=(self.screen.get_width() // 2 - options_button.get_width() // 2, 200)),
            quit_button.get_rect(topleft=(self.screen.get_width() // 2 - quit_button.get_width() // 2, 250))
        )

    def draw_options(self):
        self.screen.fill((0, 0, 0))
        title = self.font.render("Options", True, (255, 255, 255))
        back_button = self.font.render("Back", True, (255, 255, 255))
        
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 50))
        self.screen.blit(back_button, (self.screen.get_width() // 2 - back_button.get_width() // 2, 250))
        
        pygame.display.update()
        return back_button.get_rect(topleft=(self.screen.get_width() // 2 - back_button.get_width() // 2, 250))
