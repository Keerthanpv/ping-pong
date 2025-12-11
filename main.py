import pygame
from game.game_engine import GameEngine

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Clock and constants
BLACK = (0, 0, 0)
clock = pygame.time.Clock()
FPS = 60

# Game engine instance
engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        events = pygame.event.get()  
        SCREEN.fill(BLACK)

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        if not engine.game_over:
            engine.handle_input()
            engine.update()
        else:
            if not engine.show_replay_menu(events):
                running = False

        engine.render(SCREEN)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
