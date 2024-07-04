import pygame

# Creating trash collector
class Collector(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, walkRight, walkLeft):
        super().__init__()
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
        self.walkRight = walkRight
        self.walkLeft = walkLeft

    def draw(self, screen):
        if self.walkCount + 1 >= 12:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                screen.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
            elif self.right:
                screen.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:
            if self.right:
                screen.blit(self.walkRight[0], (self.x, self.y))
            else:
                screen.blit(self.walkLeft[0], (self.x, self.y))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > self.vel:
            self.x -= self.vel
            self.left = True
            self.right = False
            self.standing = False
        elif keys[pygame.K_RIGHT] and self.x < 500 - self.width - self.vel:
            self.x += self.vel
            self.left = False
            self.right = True
            self.standing = False
        else:
            self.standing = True

        if keys[pygame.K_UP] and self.y > self.vel:
            self.y -= self.vel
        if keys[pygame.K_DOWN] and self.y < 500 - self.height - self.vel:
            self.y += self.vel

        self.rect.topleft = (self.x, self.y)
