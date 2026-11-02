import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot

# Player class for the game
class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0  # Shot cooldown timer
        self.lives = 3 # Number of lives
        self.invincible_timer = PLAYER_INVINCIBILITY_TIME  # Invincibility timer
        self.moving_backwards = False #Flag to check if player is moving backwards



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

        
    
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOT_SPEED
        Shot(self.position.x, self.position.y, velocity)  # Create shot with velocity
        self.timer = PLAYER_SHOOT_COOLDOWN  # Reset cooldown timer

    def respawn(self):
        self.position = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.timer = 0
        self.invincible_timer = PLAYER_INVINCIBILITY_TIME









