import pygame
import random
from circleshape import CircleShape
from constants import *


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.radius = radius
        
    def draw(self, screen):
            pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)
    
    def update(self, dt):
            self.position += self.velocity * dt
    
    def split(self):
        self.kill()
        # Check if the radius of the asteroid is less than the minimum radius
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
             # Generate a random angle between 20 and 50 degrees
            random_angle = random.uniform(20, 50)
            
            # Create two new vectors rotated by random_angle and -random_angle
            velocity1 = self.velocity.rotate(random_angle) * 1.2
            velocity2 = self.velocity.rotate(-random_angle) * 1.2
            
            # Compute the new radius of the smaller asteroids
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            
            # Create two new Asteroid objects at the current position with the new radius
            Asteroid(self.position.x, self.position.y, new_radius).velocity = velocity1
            Asteroid(self.position.x, self.position.y, new_radius).velocity = velocity2
             

        

        
        
        
