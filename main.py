import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def game_over(screen):
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
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

        for i, option in enumerate(options):
            color = (255, 255, 255) if i == selected_option else (100, 100, 100)
            option_text = small_font.render(option, True, color)
            screen.blit(option_text, (SCREEN_WIDTH // 2 - option_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50 * i))

        pygame.display.flip()
        clock.tick(144) / 1000

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


    AsteroidField.containers = (updatable,)
    AsteroidField()

    
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
        if player.invincible_timer <= 0:
            for asteroid in asteroids:
                if player.collides_with(asteroid):
                    player.lives -= 1
                    if player.lives > 0:
                        player.respawn()
                    else:
                        game_over(screen)
                        return
        
        # Check for collisions between asteroids and shots
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    asteroid.split()
                    shot.kill()
                    break

        pygame.display.flip()

        # Limit frame rate to 144 fps
        dt = clock.tick(144) / 1000

if __name__ == "__main__":
    main()