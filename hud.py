import pygame
import os
from constants import *

class HUD:
    def __init__(self):
        self.score = 0
        self.high_score = self.load_high_score()
        self.font_large = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
    
    def update_score(self, points):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
    
    def draw(self, screen, player):
        # Draw score
        score_text = self.font_large.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        # Draw high score
        high_score_text = self.font_small.render(f"High Score: {self.high_score}", True, (200, 200, 200))
        screen.blit(high_score_text, (10, 40))
        
        # Draw lives
        self.draw_lives(screen, player.lives)
    
    def draw_lives(self, screen, lives):
        for i in range(lives):
            offset = 30 * i
            pos_x = SCREEN_WIDTH - 80 + offset
            pos_y = 30
            
            # Create triangle representing ship
            forward = pygame.Vector2(0, 1)
            right = pygame.Vector2(1, 0) * PLAYER_RADIUS / 1.5
            
            a = pygame.Vector2(pos_x, pos_y - PLAYER_RADIUS)
            b = pygame.Vector2(pos_x - right.x, pos_y + PLAYER_RADIUS)
            c = pygame.Vector2(pos_x + right.x, pos_y + PLAYER_RADIUS)
            
            pygame.draw.polygon(screen, (255, 255, 255), [a, b, c], 2)
    
    def game_over(self, screen):
        options = ["NEW GAME", "EXIT"]
        selected = 0
        clock = pygame.time.Clock()
        
        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                    
                if event.type == pygame.KEYDOWN:
                    # Navigate menu
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        selected = (selected - 1) % len(options)
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(options)
                    # Select option    
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        return selected == 0  # Return True for new game, False for exit
        

            # Draw game over screen
            screen.fill((0, 0, 0))
            self._draw_game_over_screen(screen, selected, options)
            pygame.display.flip()
            clock.tick(60)
    
    def _draw_game_over_screen(self, screen, selected, options):
        # Title
        font_title = pygame.font.Font(None, 74)
        game_over_text = font_title.render("GAME OVER", True, (255, 0, 0))
        text_x = SCREEN_WIDTH // 2 - game_over_text.get_width() // 2
        screen.blit(game_over_text, (text_x, SCREEN_HEIGHT // 2 - 150))
        
        # Final score
        final_score_text = self.font_large.render(f"Final Score: {self.score}", True, (255, 255, 255))
        text_x = SCREEN_WIDTH // 2 - final_score_text.get_width() // 2
        screen.blit(final_score_text, (text_x, SCREEN_HEIGHT // 2 - 80))
        
        # High score
        high_score_text = self.font_large.render(f"High Score: {self.high_score}", True, (255, 255, 255))
        text_x = SCREEN_WIDTH // 2 - high_score_text.get_width() // 2
        screen.blit(high_score_text, (text_x, SCREEN_HEIGHT // 2 - 40))
        
        # Menu options
        font_menu = pygame.font.Font(None, 50)
        for i, option in enumerate(options):
            color = (255, 255, 255) if i == selected else (100, 100, 100)
            option_text = font_menu.render(option, True, color)
            text_x = SCREEN_WIDTH // 2 - option_text.get_width() // 2
            screen.blit(option_text, (text_x, SCREEN_HEIGHT // 2 + 50 * i))
    
    def calculate_score(self, asteroid_radius):
        if asteroid_radius <= ASTEROID_MIN_RADIUS:
            return 100  # Small asteroid
        elif asteroid_radius <= ASTEROID_MIN_RADIUS * 2:
            return 50   # Medium asteroid
        else:
            return 20   # Large asteroid
    
    def load_high_score(self):
        high_score_file = "high_score.txt"
        try:
            if os.path.exists(high_score_file):
                with open(high_score_file, "r") as file:
                    return int(file.read().strip())
        except:
            pass
        return 0
    
    def save_high_score(self):
        high_score_file = "high_score.txt"
        try:
            with open(high_score_file, "w") as file:
                file.write(str(self.high_score))
        except:
            pass
    
    def reset(self):
        self.score = 0