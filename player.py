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



    # Represent player as triangle
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        color = (255, 0, 0) if self.invincible_timer > 0 else (255, 255, 255)
        pygame.draw.polygon(screen, color, self.triangle(), 2)

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









