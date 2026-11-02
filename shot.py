from circleshape import CircleShape
from constants import *
import pygame

# Data-driven weapon definitions. Each weapon describes how the player's
# trigger behaves: how many projectiles fire, the fan angle they spread
# across, their speed/size, how many asteroids one projectile can destroy,
# the fire cooldown, and the tracer color.
WEAPONS = {
    "blaster": {
        "shots": 1,
        "spread_deg": 0,
        "speed": 500,
        "radius": 5,
        "pierce": 1,
        "cooldown": 0.3,
        "color": (255, 255, 255),
    },
    "spread": {
        "shots": 3,
        "spread_deg": 30,
        "speed": 500,
        "radius": 4,
        "pierce": 1,
        "cooldown": 0.4,
        "color": (120, 255, 140),
    },
    "lance": {
        "shots": 1,
        "spread_deg": 0,
        "speed": 650,
        "radius": 9,
        "pierce": 3,
        "cooldown": 0.55,
        "color": (255, 160, 60),
    },
}


class Shot(CircleShape):
    def __init__(self, x, y, velocity, radius=SHOT_RADIUS, color=(255, 255, 255), pierce=1):
        super().__init__(x, y, radius)
        self.velocity = velocity  # Shot velocity
        self.color = color
        self.pierce = pierce  # Asteroids this projectile can destroy before expiring

    def draw(self, screen):
        # Render as a directional tracer: a short line trailing behind the head
        # plus a small filled head circle, both in the weapon's color.
        if self.velocity.length() == 0:
            return
        direction = self.velocity.normalize()
        tail = self.position - direction * (self.radius * 2.5)
        line_width = max(2, self.radius // 2)
        pygame.draw.line(screen, self.color, tail, self.position, line_width)
        pygame.draw.circle(screen, self.color, self.position, max(1, int(self.radius * 0.6)))

    def update(self, dt):
        self.position += self.velocity * dt  # Update position
        # Remove shots that have left the screen so they don't accumulate
        if (
            self.position.x < -self.radius
            or self.position.x > SCREEN_WIDTH + self.radius
            or self.position.y < -self.radius
            or self.position.y > SCREEN_HEIGHT + self.radius
        ):
            self.kill()