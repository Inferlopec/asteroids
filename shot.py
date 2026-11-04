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
        "speed": 900,
        "radius": 4,
        "pierce": 6,
        "cooldown": 0.55,
        "color": (255, 60, 60),
        "laser": True,  # Rendered as a long beam instead of a short tracer
    },
}


class Shot(CircleShape):
    def __init__(self, x, y, velocity, radius=SHOT_RADIUS, color=(255, 255, 255), pierce=1, laser=False):
        super().__init__(x, y, radius)
        self.velocity = velocity  # Shot velocity
        self.color = color
        self.pierce = pierce  # Asteroids this projectile can destroy before expiring
        self.laser = laser  # Render as a long beam (lance) instead of a short tracer

    def draw(self, screen):
        if self.velocity.length() == 0:
            return
        direction = self.velocity.normalize()
        if self.laser:
            # Laser beam: a short, thin, hot core with a soft glow that fades
            # both across its width (bright center -> transparent edges) and
            # along its length (bright at the head -> dim at the tail). The
            # glow is drawn directly in screen space as short segments with
            # per-segment alpha, so it stays aligned with the core at any angle
            # (no rotation/anchor fragility).
            length = 36
            tail = self.position - direction * length
            r, g, b = self.color
            # Hot core: brighten the weapon color toward white.
            core = (
                min(255, r + (255 - r) * 0.7),
                min(255, g + (255 - g) * 0.7),
                min(255, b + (255 - b) * 0.7),
            )
            # Glow: N segments from tail to head, each a 3-line width falloff
            # (bright center, dim edges) with alpha increasing toward the head.
            perp = pygame.Vector2(-direction.y, direction.x)
            segments = 12
            for i in range(segments):
                t0 = i / segments
                t1 = (i + 1) / segments
                p0 = tail + direction * (length * t0)
                p1 = tail + direction * (length * t1)
                alpha = int(150 * (0.35 + 0.65 * ((t0 + t1) / 2)))
                for off, width_alpha in ((0, 1.0), (1, 0.5), (-1, 0.5)):
                    a = int(alpha * width_alpha)
                    if a > 0:
                        seg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                        pygame.draw.line(
                            seg, (r, g, b, a),
                            (int((p0 + perp * off).x), int((p0 + perp * off).y)),
                            (int((p1 + perp * off).x), int((p1 + perp * off).y)), 1,
                        )
                        screen.blit(seg, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            pygame.draw.line(screen, core, tail, self.position, 2)
            pygame.draw.circle(screen, (255, 255, 255), self.position, 1)
            return
        # Render as a directional tracer: a short line trailing behind the head
        # plus a small filled head circle, both in the weapon's color.
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