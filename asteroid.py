import pygame
import random
from circleshape import CircleShape
from constants import *
from particle import spawn_explosion

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.radius = radius
        # Random lumpy shape: per-vertex radii between 60% and 100% of the base radius
        self.num_vertices = random.randint(ASTEROID_MIN_VERTICES, ASTEROID_MAX_VERTICES)
        self.shape = [radius * random.uniform(0.6, 1.0) for _ in range(self.num_vertices)]
        # Random initial rotation and spin speed
        self.spin_angle = random.uniform(0, 360)
        self.spin_speed = random.uniform(ASTEROID_SPIN_MIN, ASTEROID_SPIN_MAX)

    def draw(self, screen):
        points = []
        for i, vertex_radius in enumerate(self.shape):
            angle = self.spin_angle + (i / self.num_vertices) * 360
            point = self.position + pygame.Vector2(vertex_radius, 0).rotate(angle)
            points.append(point)
        pygame.draw.polygon(screen, (0, 0, 0), points)  # fill to occlude stars
        pygame.draw.polygon(screen, (255, 255, 255), points, 2)
    
    def update(self, dt):
        self.position += self.velocity * dt
        self.spin_angle += self.spin_speed * dt
        # Wrap around the screen edges so asteroids reappear on the opposite side
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius
    
    def split(self):
        pos = self.position.copy()
        vel = self.velocity.copy()
        radius = self.radius
        self.kill()
        spawn_explosion(pos, vel, radius)
        if radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            random_angle = random.uniform(20, 50)
            velocity1 = self.velocity.rotate(random_angle) * 1.2
            velocity2 = self.velocity.rotate(-random_angle) * 1.2
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            # Create the first new asteroid with the new radius and assign the calculated velocity
            Asteroid(self.position.x, self.position.y, new_radius).velocity = velocity1
            # Create the second new asteroid with the new radius and assign the calculated velocity
            Asteroid(self.position.x, self.position.y, new_radius).velocity = velocity2







