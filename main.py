import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from hud import HUD

def main():
    """Main game entry point that handles game sessions and restarts"""
    pygame.init()
    running = True
    
    while running:
        running = game_session()
    
    pygame.quit()

def game_session():
    """Run a complete game session, return True to restart or False to quit"""
    # Setup display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    
    # Game objects
    hud = HUD()
    clock = pygame.time.Clock()
    
    # Sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    # Set up containers for sprites
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    
    # Create game objects
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    AsteroidField()
    
    # Game loop
    dt = 0
    running = True
    skip_next_update = False
    while running:
        # Process events
        should_pause = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Exit game completely
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                should_pause = True
        
        # If ESC pressed, immediately show pause menu (which blocks the game)
        if should_pause:
            result = hud.pause_menu(screen, drawable, player, hud)
            if result == "restart":
                return True  # Restart game session
            elif result == "exit":
                return False  # Exit game
            # If "resume", skip the next update to avoid time jump
            skip_next_update = True
            pygame.display.flip()
            dt = clock.tick(144) / 1000
            continue
        
        # If we just resumed from pause, skip this update
        if skip_next_update:
            skip_next_update = False
            pygame.display.flip()
            dt = clock.tick(144) / 1000
            continue
        
        # Update game objects
        updatable.update(dt)
        
        # Draw game
        screen.fill((0, 0, 0))
        for obj in drawable:
            obj.draw(screen)
        hud.draw(screen, player)
        
        # Handle player-asteroid collisions
        if player.invincible_timer <= 0:
            for asteroid in asteroids:
                if player.collides_with(asteroid):
                    player.lives -= 1
                    if player.lives > 0:
                        player.respawn()
                    else:
                        # Game over - return restart choice from HUD
                        return hud.game_over(screen)
        
        # Handle shot-asteroid collisions
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    points = hud.calculate_score(asteroid.radius)
                    hud.update_score(points)
                    asteroid.split()
                    shot.kill()
                    break
        
        # Update display
        pygame.display.flip()
        dt = clock.tick(144) / 1000
    
    return False

if __name__ == "__main__":
    main()