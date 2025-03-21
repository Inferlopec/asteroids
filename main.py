import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")

    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Initialize player

    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)

    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()

    shots = pygame.sprite.Group()
    Shot.containers = (shots, updatable, drawable)

    dt = 0

    #main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                return
        screen.fill((0, 0, 0))
        
        # Update and draw objects
        updatable.update(dt)
        for obj in drawable:
            obj.draw(screen)

        # Draw lives
        player.draw_lives(screen)

        # Check for collisions
        for asteroid in asteroids:
            if player.collides_with(asteroid):
               player.lives -= 1
               if player.lives > 0:
                   player.respawn()
               else:
                   player.game_over(screen, main)
                   return
        
        # Check for collisions between asteroids and shots
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    asteroid.split()
                    shot.kill()
                    break

        pygame.display.flip()

        # Limit frame rate to 60 fps
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()