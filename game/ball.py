import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self, player, ai, paddle_hit_sound, wall_bounce_sound):
        """Moves the ball and handles collisions and sounds."""
        # Move horizontally
        self.x += self.velocity_x
        ball_rect = self.rect()

        # Check for horizontal collision with paddles
        if ball_rect.colliderect(player.rect()) or ball_rect.colliderect(ai.rect()):
            self.velocity_x *= -1
            paddle_hit_sound.play() # Play paddle hit sound
            # Snap ball to paddle edge to prevent getting stuck
            if self.velocity_x > 0: # Hit player paddle, now moving right
                 self.x = player.rect().right
            else: # Hit AI paddle, now moving left
                 self.x = ai.rect().left - self.width
        
        # Move vertically
        self.y += self.velocity_y
        ball_rect.y = self.y # Update rect y-position

        # Check for vertical collision with walls
        if ball_rect.top <= 0 or ball_rect.bottom >= self.screen_height:
            self.velocity_y *= -1
            wall_bounce_sound.play() # Play wall bounce sound

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)