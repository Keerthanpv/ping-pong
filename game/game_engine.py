import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)

        try:
            paddle_sound = pygame.mixer.Sound("sounds/paddle.wav")
            wall_sound = pygame.mixer.Sound("sounds/wall.wav")
            score_sound = pygame.mixer.Sound("sounds/decide.mp3")
        except Exception as e:
            print(f"⚠️ Sound loading error: {e}")
            paddle_sound = wall_sound = score_sound = None

        sound_fx = {
            "paddle": paddle_sound,
            "wall": wall_sound,
            "score": score_sound
        }

        self.ball = Ball(width // 2, height // 2, 10, 10, width, height, sound_fx=sound_fx)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.large_font = pygame.font.SysFont("Arial", 60)
        self.medium_font = pygame.font.SysFont("Arial", 40)
        self.game_over = False
        self.winner_text = ""
        self.winning_score = 5  

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        if self.game_over:
            return

        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x + self.ball.width < 0:  # Ball went past player
            self.ai_score += 1
            if self.ball.sound_fx["score"]:
                self.ball.sound_fx["score"].play()
            self.ball.reset(direction='right')

        elif self.ball.x > self.width:  # Ball went past AI
            self.player_score += 1
            if self.ball.sound_fx["score"]:
                self.ball.sound_fx["score"].play()
            self.ball.reset(direction='left')

        self.ai.auto_track(self.ball, self.height)

        self.check_game_over()

    def check_game_over(self):
        if self.player_score >= self.winning_score:
            self.winner_text = "Player Wins!"
            self.game_over = True
        elif self.ai_score >= self.winning_score:
            self.winner_text = "AI Wins!"
            self.game_over = True

    def render(self, screen):
        screen.fill(BLACK)
        if not self.game_over:
            pygame.draw.rect(screen, WHITE, self.player.rect())
            pygame.draw.rect(screen, WHITE, self.ai.rect())
            pygame.draw.ellipse(screen, WHITE, self.ball.rect())
            pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

            player_text = self.font.render(str(self.player_score), True, WHITE)
            ai_text = self.font.render(str(self.ai_score), True, WHITE)
            screen.blit(player_text, (self.width // 4, 20))
            screen.blit(ai_text, (self.width * 3 // 4, 20))
        else:
            text_surface = self.large_font.render(self.winner_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 60))
            screen.blit(text_surface, text_rect)

            options = [
                "Press 3 for Best of 3",
                "Press 5 for Best of 5",
                "Press 7 for Best of 7",
                "Press ESC to Exit",
            ]
            for i, line in enumerate(options):
                option_surface = self.medium_font.render(line, True, WHITE)
                option_rect = option_surface.get_rect(center=(self.width // 2, self.height // 2 + 40 + i * 50))
                screen.blit(option_surface, option_rect)

    def show_replay_menu(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key in (pygame.K_3, pygame.K_5, pygame.K_7):
                    self.winning_score = int(event.unicode)
                    self.reset_game()
                    return True
        return True

    def reset_game(self):
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.winner_text = ""
        self.ball.reset()
        self.player.y = self.height // 2 - self.paddle_height // 2
        self.ai.y = self.height // 2 - self.paddle_height // 2
