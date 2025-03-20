import pygame
from constants import *
from player import Player


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Initialize player object
    clock = pygame.time.Clock()
    dt = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        screen.fill((0, 0, 0))
        
        # Update and draw player
        player.draw(screen)
        
        pygame.display.flip()

        # Limit the frame rate to 60 fps
        dt = clock.tick(60) / 1000
        
        



if __name__ == "__main__":
    main()