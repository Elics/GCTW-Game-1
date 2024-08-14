#




import time
import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, waypoints, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=waypoints[0])
        self.waypoints = waypoints
        self.current_waypoint = 0
        self.speed = 3  # Initial speed of the enemy
        self.last_speed_increase_time = time.time()

    def update(self):
        if self.waypoints:
            target = self.waypoints[self.current_waypoint]
            dx = target[0] - self.rect.x
            dy = target[1] - self.rect.y
            distance = (dx**2 + dy**2) ** 0.5

            if distance != 0:
                dx /= distance
                dy /= distance

            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

            if self.rect.collidepoint(target):
                self.current_waypoint = (self.current_waypoint + 1) % len(self.waypoints)
        
        # Increase speed every 2 seconds
        current_time = time.time()
        if current_time - self.last_speed_increase_time > 2:
            self.speed += 1
            self.last_speed_increase_time = current_time

    @staticmethod
    def generate_random_waypoints(screen_width, screen_height, num_waypoints = 4):
        margin =50
        return [(random.randint(0, screen_width), random.randint(0, screen_height)) for _ in range(num_waypoints)]















""""
import pygame
from pygame.math import Vector2
import math



enemyWalkRight = []
enemyWalkLeft = []


class Enemy(pygame.sprite.Sprite):
    def __init__(self, waypoints, image):
        pygame.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.speed = 2
        self.angle = 0
        self.original_image = image
        self.image = pygame.transform.rotate(self.original_image,self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self):
        self.move()
        self.rotate()
    
    def move(self):
        #define a target waypoint
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
        #enemy has reached the end of the path
            self.kill()

        dist = self.movement.length()
        if dist >= self.speed:
            self.pos +=self.movement.normalize() * self.speed

        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1


    def rotate(self):
        #calculate distance to next waypoint
        dist = self.target - self.pos
        #use distance to calculate angle
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
        #rotate image and update rectangle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos


 #       """
"""
import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, waypoints, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=waypoints[0])
        self.waypoints = waypoints
        self.current_waypoint = 0
        self.speed = 3  # Speed of the enemy movement

    def update(self):
        if self.waypoints:
            target = self.waypoints[self.current_waypoint]
            dx = target[0] - self.rect.x
            dy = target[1] - self.rect.y
            distance = (dx**2 + dy**2) ** 0.5

            if distance != 0:
                dx /= distance
                dy /= distance

            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

            if self.rect.collidepoint(target):
                self.current_waypoint += 1
                if self.current_waypoint >= len(self.waypoints):
                    self.current_waypoint = 0

                    
"""