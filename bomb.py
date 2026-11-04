import pygame
from circleshape import CircleShape
from constants import *


class Bomb(CircleShape):
    """A droppable bomb that drifts and explodes on contact with an asteroid.

    The explosion (radius BOMB_EXPLOSION_RADIUS) is handled by main.py,
    which destroys every asteroid in range.
    """

    def __init__(self, x, y):
        super().__init__(x, y, BOMB_RADIUS)
        self.velocity = pygame.Vector2(0, 0)

    def draw(self, screen):
        cx, cy = int(self.position.x), int(self.position.y)
        # Pulsing ring with a filled core
        pulse = (pygame.time.get_ticks() / 200) % (2 * 3.14159)
        ring_radius = int(self.radius + 2 + 2 * ((pygame.math.Vector2(1, 0).rotate(pulse * 180 / 3.14159).x + 1) / 2))
        pygame.draw.circle(screen, BOMB_COLOR, (cx, cy), ring_radius, 2)
        pygame.draw.circle(screen, BOMB_COLOR, (cx, cy), max(1, int(self.radius * 0.5)))

    def update(self, dt):
        self.position += self.velocity * dt
        # Remove bombs that have left the screen
        if (
            self.position.x < -self.radius
            or self.position.x > SCREEN_WIDTH + self.radius
            or self.position.y < -self.radius
            or self.position.y > SCREEN_HEIGHT + self.radius
        ):
            self.kill()
