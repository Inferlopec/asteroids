import pygame
import random
from circleshape import CircleShape
from constants import *
from shot import WEAPONS

# Letter shown on each pickup icon (weapons + shield)
PICKUP_LABELS = {
    "spread": "W",
    "lance": "L",
    "shield": "S",
}


class Pickup(CircleShape):
    """A floating item that drifts, wraps the screen, blinks, and expires.

    Kinds: "weapon" (spread/lance), "shield", "life". `kind` + `apply()` are
    the extension point for future booster power-ups (speed, ...).
    """

    def __init__(self, x, y, kind, weapon=None):
        super().__init__(x, y, PICKUP_RADIUS)
        self.kind = kind
        self.weapon = weapon
        if kind == "weapon":
            self.color = WEAPONS[weapon]["color"]
            self.label = PICKUP_LABELS.get(weapon, "?")
        elif kind == "shield":
            self.color = SHIELD_COLOR
            self.label = PICKUP_LABELS["shield"]
        elif kind == "life":
            self.color = LIFE_PICKUP_COLOR
            self.label = "+"
        # Random gentle drift
        angle = random.uniform(0, 360)
        self.velocity = pygame.Vector2(PICKUP_DRIFT_SPEED, 0).rotate(angle)
        self.lifetime = PICKUP_LIFETIME
        self.age = 0.0
        self.spin_angle = random.uniform(0, 360)
        self.spin_speed = random.uniform(40, 90)
        self.font = pygame.font.Font(None, 20)

    def update(self, dt):
        self.position += self.velocity * dt
        self.age += dt
        self.spin_angle += self.spin_speed * dt
        # Wrap around the screen edges
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius
        if self.age >= self.lifetime:
            self.kill()

    def draw(self, screen):
        # Blink during the final 2 seconds (skip alternate frames)
        if self.lifetime - self.age < 2.0 and int(self.age * 10) % 2 == 0:
            return
        cx, cy = int(self.position.x), int(self.position.y)
        if self.kind == "life":
            # Red circle with a "+" cross
            pygame.draw.circle(screen, self.color, (cx, cy), self.radius, 2)
            arm = self.radius * 0.5
            pygame.draw.line(screen, self.color, (cx - arm, cy), (cx + arm, cy), 2)
            pygame.draw.line(screen, self.color, (cx, cy - arm), (cx, cy + arm), 2)
            return
        if self.kind == "shield":
            # Cyan circle with an "S" label
            pygame.draw.circle(screen, self.color, (cx, cy), self.radius, 2)
            label = self.font.render(self.label, True, self.color)
            screen.blit(label, label.get_rect(center=(cx, cy)))
            return
        # Rotating square outline in the weapon's color
        size = self.radius
        points = []
        for i in range(4):
            angle = self.spin_angle + i * 90
            points.append((cx + int(size * 0.8 * pygame.math.Vector2(1, 0).rotate(angle).x),
                           cy + int(size * 0.8 * pygame.math.Vector2(1, 0).rotate(angle).y)))
        pygame.draw.polygon(screen, self.color, points, 2)
        # Letter label in the center
        label = self.font.render(self.label, True, self.color)
        screen.blit(label, label.get_rect(center=(cx, cy)))

    def apply(self, player):
        """Apply this pickup's effect to the player."""
        if self.kind == "weapon":
            player.weapon = self.weapon
        elif self.kind == "shield":
            player.shield_timer = SHIELD_DURATION
        elif self.kind == "life":
            player.lives = min(player.lives + 1, PLAYER_MAX_LIVES)

    @classmethod
    def spawn(cls, kind, x, y):
        """Spawn a pickup of the given kind at (x, y)."""
        if kind == "weapon":
            weapons = [w for w in WEAPONS if w != "blaster"]
            return cls(x, y, "weapon", random.choice(weapons))
        return cls(x, y, kind)
