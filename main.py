import pygame
from game.game_engine import GameEngine

# Initialize pygame and its mixer
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game engine instance
engine = GameEngine(WIDTH, HEIGHT)

def draw_replay_menu(screen):
    """Draws the replay options on the screen."""
    font = pygame.font.SysFont("Arial", 24)
    options = [
        "Play Again?",
        "Best of 3: Press 3",
        "Best of 5: Press 5",
        "Best of 7: Press 7",
        "Exit: Press ESC"
    ]
    
    for i, text in enumerate(options):
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 40))
        screen.blit(text_surface, text_rect)

def main():
    running = True
    while running:
        # Event handling is always active
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Check for replay input only when the game is over
            if engine.game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    engine.reset_game(3)
                elif event.key == pygame.K_5:
                    engine.reset_game(5)
                elif event.key == pygame.K_7:
                    engine.reset_game(7)
                elif event.key == pygame.K_ESCAPE:
                    running = False

        # Clear the screen each frame
        SCREEN.fill(BLACK)

        # Logic depends on game state
        if not engine.game_over:
            # --- Normal Gameplay ---
            engine.handle_input()
            engine.update()
            engine.render(SCREEN)
        else:
            # --- Game Over / Replay Screen ---
            engine.render(SCREEN) # Show "Player/AI Wins!"
            draw_replay_menu(SCREEN) # Show replay options

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()