import pygame
import random
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from hud import HUD
from background import Background
from particle import Particle

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
    Particle.containers = (updatable, drawable)
    
    # Create game objects
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    AsteroidField()
    background = Background()
    
    # Game loop
    dt = 0
    running = True
    skip_next_update = False
    while running:
        # Process events
        should_pause = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                hud.save_high_score()
                return False  # Exit game completely
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                should_pause = True
        
        # If ESC pressed, immediately show pause menu (which blocks the game)
        if should_pause:
            result = hud.pause_menu(screen, drawable, player, hud, background)
            if result == "restart":
                return True  # Restart game session
            elif result == "exit":
                hud.save_high_score()
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
        background.update(dt)
        updatable.update(dt)
        
        # Draw game
        screen.fill((0, 0, 0))
        background.draw(screen)
        for obj in drawable:
            obj.draw(screen)
        hud.draw(screen, player)
        
        # Handle player-asteroid collisions
        if player.invincible_timer <= 0:
            for asteroid in asteroids:
                if player.collides_with_asteroid(asteroid):
                    player.lives -= 1
                    if player.lives > 0:
                        player.respawn()
                    else:
                        # Game over - return restart choice from HUD
                        hud.save_high_score()
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
        
        # Handle asteroid-asteroid collisions
        asteroid_list = list(asteroids)
        for i in range(len(asteroid_list)):
            for j in range(i + 1, len(asteroid_list)):
                a1, a2 = asteroid_list[i], asteroid_list[j]
                if a1.collides_with(a2):
                    # Calculate direction between centers (handle same position)
                    direction = a1.position - a2.position
                    if direction.length() == 0:
                        # If same position, use random direction
                        angle = random.uniform(0, 360)
                        direction = pygame.Vector2(1, 0).rotate(angle)
                    else:
                        direction = direction.normalize()
                    # Separate asteroids so they don't overlap
                    overlap = (a1.radius + a2.radius) - a1.position.distance_to(a2.position)
                    a1.position += direction * (overlap / 2)
                    a2.position -= direction * (overlap / 2)
                    # Change velocity (bounce)
                    velocity_change = direction * 20 * ASTEROID_BOUNCE_FACTOR
                    a1.velocity += velocity_change
                    a2.velocity -= velocity_change
                    # Cap speed so repeated bounces don't accelerate asteroids unboundedly
                    if a1.velocity.length() > ASTEROID_MAX_SPEED:
                        a1.velocity = a1.velocity.normalize() * ASTEROID_MAX_SPEED
                    if a2.velocity.length() > ASTEROID_MAX_SPEED:
                        a2.velocity = a2.velocity.normalize() * ASTEROID_MAX_SPEED
        
        # Update display
        pygame.display.flip()
        dt = clock.tick(144) / 1000
    
    return False

if __name__ == "__main__":
    main()