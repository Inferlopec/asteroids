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
    restart = False
    
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
    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Exit game completely
        
        # Clear screen
        screen.fill((0, 0, 0))
        
        # Update and draw game objects
        updatable.update(dt)
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