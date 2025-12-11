import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height, sound_fx=None):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-6, 6])
        self.velocity_y = random.choice([-3, 3])
        self.sound_fx = sound_fx or {}

        self.sound_fx.setdefault('paddle', None)
        self.sound_fx.setdefault('wall', None)
        self.sound_fx.setdefault('score', None)

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top/bottom walls
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            if self.sound_fx['wall']:
                try:
                    self.sound_fx['wall'].play()
                except Exception:
                    pass

    def check_collision(self, player, ai):
        ball_rect = self.rect()
        p_rect = player.rect()
        a_rect = ai.rect()

        if ball_rect.colliderect(p_rect) and self.velocity_x < 0:
            self.x = p_rect.right
            self.velocity_x *= -1
            # Add angle effect based on hit position
            offset = ((self.y + self.height/2) - (p_rect.y + p_rect.height/2)) / (p_rect.height/2)
            self.velocity_y += int(offset * 3)
            if self.sound_fx['paddle']:
                try:
                    self.sound_fx['paddle'].play()
                except Exception:
                    pass

        # AI paddle collision (right)
        elif ball_rect.colliderect(a_rect) and self.velocity_x > 0:
            self.x = a_rect.left - self.width
            self.velocity_x *= -1
            offset = ((self.y + self.height/2) - (a_rect.y + a_rect.height/2)) / (a_rect.height/2)
            self.velocity_y += int(offset * 3)
            if self.sound_fx['paddle']:
                try:
                    self.sound_fx['paddle'].play()
                except Exception:
                    pass

        self.velocity_y = max(min(self.velocity_y, 10), -10)

    def reset(self, direction=None):
        """Reset ball to center and set direction."""
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_y = random.choice([-3, -2, 2, 3])

        speed_x = 6
        if direction == 'left':
            self.velocity_x = -abs(speed_x)
        elif direction == 'right':
            self.velocity_x = abs(speed_x)
        else:
            self.velocity_x *= -1  # Just reverse if no direction specified

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
