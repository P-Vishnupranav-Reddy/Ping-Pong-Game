import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)
INITIAL_WINNING_SCORE = 5

class GameEngine:
    def __init__(self, width, height):
        # -- 1. Set up dimensions --
        self.width = width
        self.height = height
        self.paddle_width = 10   # Define paddle dimensions first
        self.paddle_height = 100 # Define paddle dimensions first

        # -- 2. Create game objects --
        self.player = Paddle(10, height // 2 - self.paddle_height // 2, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - self.paddle_width - 10, height // 2 - self.paddle_height // 2, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        # -- 3. Initialize game state --
        self.player_score = 0
        self.ai_score = 0
        self.winning_score = INITIAL_WINNING_SCORE
        self.game_over = False
        self.winner_text = ""
        
        # -- 4. Load assets (fonts and sounds) --
        self.font = pygame.font.SysFont("Arial", 30)
        try:
            self.paddle_hit_sound = pygame.mixer.Sound("sounds/paddle_sound.wav")
            self.wall_bounce_sound = pygame.mixer.Sound("sounds/wallhit_sound.wav")
            self.score_sound = pygame.mixer.Sound("sounds/score_sound.wav")
        except pygame.error as e:
            print(f"Error loading sound file: {e}")
            self.paddle_hit_sound = self.wall_bounce_sound = self.score_sound = pygame.mixer.Sound(buffer=b'')

    def reset_game(self, winning_score):
        """Resets the entire game for a new match with a new score target."""
        self.player_score = 0
        self.ai_score = 0
        self.winning_score = winning_score
        self.game_over = False
        self.winner_text = ""
        self.ball.reset()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        if not self.game_over:
            self.ball.move(self.player, self.ai, self.paddle_hit_sound, self.wall_bounce_sound)

            if self.ball.x <= 0:
                self.ai_score += 1
                self.score_sound.play()
                self.ball.reset()
                self.check_win()
            elif self.ball.x >= self.width:
                self.player_score += 1
                self.score_sound.play()
                self.ball.reset()
                self.check_win()

            self.ai.auto_track(self.ball, self.height)
    
    def check_win(self):
        """Checks if a player has reached the dynamic winning score."""
        if self.player_score >= self.winning_score:
            self.winner_text = "Player Wins!"
            self.game_over = True
        elif self.ai_score >= self.winning_score:
            self.winner_text = "AI Wins!"
            self.game_over = True

    def render(self, screen):
        if self.game_over:
            win_font = pygame.font.SysFont("Arial", 50)
            text_surface = win_font.render(self.winner_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 50))
            screen.blit(text_surface, text_rect)
        else:
            pygame.draw.rect(screen, WHITE, self.player.rect())
            pygame.draw.rect(screen, WHITE, self.ai.rect())
            pygame.draw.ellipse(screen, WHITE, self.ball.rect())
            pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

            player_text = self.font.render(str(self.player_score), True, WHITE)
            ai_text = self.font.render(str(self.ai_score), True, WHITE)
            screen.blit(player_text, (self.width//4, 20))
            screen.blit(ai_text, (self.width * 3//4, 20))