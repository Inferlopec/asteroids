import pygame
import random
from circleshape import CircleShape
from constants import *


class Particle(CircleShape):
    """A short-lived particle that flies outward, shrinks, and disappears."""

    def __init__(self, x, y, radius, velocity, lifetime):
        super().__init__(x, y, radius)
        self.velocity = velocity
        self.lifetime = lifetime
        self.age = 0.0

    def update(self, dt):
        self.position += self.velocity * dt
        self.age += dt
        if self.age >= self.lifetime:
            self.kill()

    def draw(self, screen):
        # Linearly shrink from initial radius to 0 over the lifetime
        t = self.age / self.lifetime
        current_radius = self.radius * (1.0 - t)
        if current_radius < 1:
            return
        pygame.draw.circle(
            screen,
            PARTICLE_COLOR,
            (int(self.position.x), int(self.position.y)),
            int(current_radius),
        )


def spawn_explosion(position, asteroid_velocity, asteroid_radius):
    """Create a burst of particles at the given position.

    Particle count scales with the asteroid's radius so larger
    asteroids produce a bigger explosion.
    """
    # Interpolate particle count between min and max based on asteroid size
    t = asteroid_radius / ASTEROID_MAX_RADIUS
    count = int(PARTICLE_COUNT_MIN + t * (PARTICLE_COUNT_MAX - PARTICLE_COUNT_MIN))

    for _ in range(count):
        angle = random.uniform(0, 360)
        speed = random.uniform(PARTICLE_SPEED_MIN, PARTICLE_SPEED_MAX)
        outward = pygame.Vector2(speed, 0).rotate(angle)
        velocity = outward + asteroid_velocity * 0.5
        radius = random.uniform(PARTICLE_SIZE_MIN, PARTICLE_SIZE_MAX)
        lifetime = random.uniform(PARTICLE_LIFETIME_MIN, PARTICLE_LIFETIME_MAX)
        Particle(position.x, position.y, radius, velocity, lifetime)
