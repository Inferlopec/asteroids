import pygame
import random
from constants import *

class Star:
    def __init__(self, layer):
        self.layer = layer  # 0 = far, 1 = mid, 2 = near
        self.x = random.randint(0, SCREEN_WIDTH)
        # 50% stars start on screen, 50% start above (for continuous stream)
        if random.random() < 0.5:
            self.y = random.randint(0, SCREEN_HEIGHT)
        else:
            self.y = random.randint(-SCREEN_HEIGHT, 0)
        self.speed = (layer + 1) * 15  # pixels per second
        self.size = layer + 1  # 1, 2, or 3 pixels
        self.brightness = 80 + layer * 60  # 80, 140, 200
        # Direction: 350 degrees (slightly to the left of straight down)
        self.direction = pygame.Vector2(0, 1).rotate(-10)  # 350 deg = -10 deg from down
    
    def update(self, dt):
        # Move in the diagonal direction
        self.x += self.direction.x * self.speed * dt
        self.y += self.direction.y * self.speed * dt
        # When star exits bottom of screen, reset to top
        if self.y > SCREEN_HEIGHT:
            self.y = -self.size
            self.x = random.randint(0, SCREEN_WIDTH + 100)  # Extra width for diagonal
    
    def draw(self, screen):
        color = (self.brightness, self.brightness, self.brightness)
        if self.size == 1:
            screen.fill(color, (self.x, self.y, 1, 1))
        else:
            pygame.draw.circle(screen, color, (self.x, self.y), self.size)

class Background:
    def __init__(self, num_stars=BG_NUM_STARS):
        self.stars = []
        for _ in range(num_stars):
            layer = random.randint(0, 2)
            self.stars.append(Star(layer))
    
    def update(self, dt):
        for star in self.stars:
            star.update(dt)
    
    def draw(self, screen):
        for star in self.stars:
            star.draw(screen)