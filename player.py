import pygame
import random
from circleshape import CircleShape
from constants import *
from shot import Shot, WEAPONS
from particle import Particle

# Player class for the game
class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0  # Shot cooldown timer
        self.lives = 3 # Number of lives
        self.invincible_timer = PLAYER_INVINCIBILITY_TIME  # Invincibility timer
        self.moving_backwards = False #Flag to check if player is moving backwards
        self.weapon = "blaster"  # Currently equipped weapon (key into WEAPONS)
        self.shield_timer = 0  # Seconds of shield invincibility remaining



    # Represent player as an arrow with a tail notch (5 points)
    def ship_points(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90)
        r = self.radius
        nose = self.position + forward * r
        wing_right = self.position - forward * r * 0.7 + right * r * 0.7
        tail_right = self.position - forward * r * 0.4 + right * r * 0.3
        tail_center = self.position - forward * r * 0.2
        tail_left = self.position - forward * r * 0.4 - right * r * 0.3
        wing_left = self.position - forward * r * 0.7 - right * r * 0.7
        return [nose, wing_right, tail_right, tail_center, tail_left, wing_left]

    def collides_with_asteroid(self, asteroid):
        """Polygon-circle collision: true if the asteroid's circle overlaps
        the ship's polygon (edge intersection or circle centre inside polygon)."""
        points = self.ship_points()
        cx, cy = asteroid.position.x, asteroid.position.y
        r = asteroid.radius

        # Quick reject: circle centre far outside the polygon's bounding box
        min_x = min(p.x for p in points) - r
        max_x = max(p.x for p in points) + r
        min_y = min(p.y for p in points) - r
        max_y = max(p.y for p in points) + r
        if not (min_x <= cx <= max_x and min_y <= cy <= max_y):
            return False

        # Check each edge for intersection with the circle
        n = len(points)
        for i in range(n):
            ax, ay = points[i].x, points[i].y
            bx, by = points[(i + 1) % n].x, points[(i + 1) % n].y
            # Closest point on segment AB to circle centre
            dx, dy = bx - ax, by - ay
            len_sq = dx * dx + dy * dy
            if len_sq == 0:
                t = 0.0
            else:
                t = max(0.0, min(1.0, ((cx - ax) * dx + (cy - ay) * dy) / len_sq))
            closest_x = ax + t * dx
            closest_y = ay + t * dy
            dist_sq = (cx - closest_x) ** 2 + (cy - closest_y) ** 2
            if dist_sq <= r * r:
                return True

        # No edge hit — check if circle centre is inside the polygon
        inside = False
        for i in range(n):
            xi, yi = points[i].x, points[i].y
            xj, yj = points[(i + 1) % n].x, points[(i + 1) % n].y
            if ((yi > cy) != (yj > cy)) and (cx < (xj - xi) * (cy - yi) / (yj - yi) + xi):
                inside = not inside
        return inside

    def draw(self, screen):
        points = self.ship_points()
        pygame.draw.polygon(screen, (0, 0, 0), points)  # fill to occlude stars
        color = (255, 0, 0) if self.invincible_timer > 0 else (255, 255, 255)
        pygame.draw.polygon(screen, color, points, 2)
        # Pulsing shield bubble while the shield power-up is active
        if self.shield_timer > 0:
            pulse = (pygame.time.get_ticks() / 300) % (2 * 3.14159)
            wave = (pygame.math.Vector2(1, 0).rotate(pulse * 180 / 3.14159).x + 1) / 2  # 0..1
            shield_radius = self.radius + 12 + 4 * wave
            alpha = int(90 + 60 * wave)
            bubble = pygame.Surface((int(shield_radius * 2) + 4, int(shield_radius * 2) + 4), pygame.SRCALPHA)
            pygame.draw.circle(bubble, (*SHIELD_COLOR, alpha), (int(shield_radius) + 2, int(shield_radius) + 2), int(shield_radius), 2)
            screen.blit(bubble, bubble.get_rect(center=(int(self.position.x), int(self.position.y))))

    # Rotation amount in degrees
    def rotate(self, amount):
        self.rotation += amount


    def update(self, dt):
        self.moving_backwards = False # Reset moving backwards flag every frame
        
        keys = pygame.key.get_pressed() 

        if keys[pygame.K_s]: # Check if player is moving backwards and set flag
            self.moving_backwards = True
            self.move(-dt)

        # Invert rotation direction if moving backwards
        rotation_direction = -1 if self.moving_backwards else 1
        # Calculate rotation amount
        rotation_amount = PLAYER_TURN_SPEED * dt

        if keys[pygame.K_d]:
            self.rotate(rotation_amount * rotation_direction)
        if keys[pygame.K_a]:
            self.rotate(-rotation_amount * rotation_direction)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_SPACE] and self.timer <= 0:
            self.shoot()
        if self.timer > 0:
            self.timer -= dt
        if self.invincible_timer > 0:
            self.invincible_timer -= dt
        if self.shield_timer > 0:
            self.shield_timer -= dt
        # Wrap around the screen edges so the ship reappears on the opposite side
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius

        
    
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        cfg = WEAPONS[self.weapon]
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        # Spawn projectiles from the nose of the ship, not its center
        origin = self.position + forward * self.radius
        count = cfg["shots"]
        for i in range(count):
            # Fan the shots across the weapon's spread angle (0 for single shots)
            if count > 1:
                offset = cfg["spread_deg"] * (i / (count - 1) - 0.5)
            else:
                offset = 0
            velocity = forward.rotate(offset) * cfg["speed"]
            Shot(origin.x, origin.y, velocity, cfg["radius"], cfg["color"], cfg["pierce"])
        # Small muzzle flash at the nose
        for _ in range(2):
            flash_vel = forward.rotate(random.uniform(-30, 30)) * random.uniform(40, 90)
            Particle(origin.x, origin.y, random.uniform(2, 4), flash_vel, 0.12, cfg["color"])
        self.timer = cfg["cooldown"]  # Reset cooldown timer

    def respawn(self):
        self.position = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.timer = 0
        self.invincible_timer = PLAYER_INVINCIBILITY_TIME
        self.weapon = "blaster"  # Reset to default weapon on death
        self.shield_timer = 0  # Shield does not carry over death









