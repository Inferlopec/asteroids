import pygame
from circleshape import CircleShape
from constants import *

#Asteroid class for the game
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.radius = radius
        
    def draw(self, screen):
            pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)
    
    def update(self, dt):
            self.position += self.velocity * dt
        

        
        
        
