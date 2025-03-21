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
        self.invincible_timer = 0  # Invincibility timer

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

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
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
        self.invincible_timer = 3 # set invincibility timer


    def draw_lives(self, screen):
        for i in range(self.lives):
            offset = 30 * i
            forward = pygame.Vector2(0, 1).rotate(0)
            right = pygame.Vector2(0, 1).rotate(90) * PLAYER_RADIUS / 1.5
            a = pygame.Vector2(30 + offset, 30) + forward * PLAYER_RADIUS
            b = pygame.Vector2(30 + offset, 30) - forward * PLAYER_RADIUS - right
            c = pygame.Vector2(30 + offset, 30) - forward * PLAYER_RADIUS + right
            pygame.draw.polygon(screen, (255, 255, 255), [a, b, c], 2)

    def game_over(self, screen, main):
        font = pygame.font.Font(None, 74)
        small_font = pygame.font.Font(None, 50)
        options = ["NEW GAME", "EXIT"]
        selected_option = 0

        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pygame.K_s:
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pygame.K_SPACE:
                        if selected_option == 0:
                            main() # Restart game
                            return
                        elif selected_option == 1:
                            pygame.quit()
                            return

            screen.fill((0, 0, 0))
            game_over_text = font.render("GAME OVER", True, (255, 255, 255))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

            for i, option in enumerate(options):
                color = (255, 255, 255) if i == selected_option else (100, 100, 100)
                option_text = small_font.render(option, True, color)
                screen.blit(option_text, (SCREEN_WIDTH // 2 - option_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50 * i))

            pygame.display.flip()
            clock.tick(60) / 1000







