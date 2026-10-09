"""
GameEngine: owns the paddle, ball, and bricks.

Starter version: single brick type, no lives yet, no score/combo yet.
Ball-brick collision also has a known bug (see game/collision.py) that
Task 1 asks you to fix. If the ball falls below the paddle, it just
resets to the starting position with no consequence - that's what
Task 2 builds on.
"""

import pygame

from game.paddle import Paddle
from game.ball import Ball
from game.brick import Brick
from game.collision import handle_ball_brick_collision
from game.renderer import WIDTH, HEIGHT

BRICK_ROWS = 4
BRICK_COLS = 8
BRICK_WIDTH = 68
BRICK_HEIGHT = 22
BRICK_GAP = 6
BRICK_TOP_MARGIN = 80
UNBREAKABLE_POSITIONS = {(2, 2), (2, 5)}
BASE_BRICK_POINTS = 100


class GameEngine:
    def __init__(self):
        self._reset_game()

    def _reset_game(self):
        self.paddle = Paddle(x=WIDTH / 2, y=HEIGHT - 30)
        self.ball = Ball(x=WIDTH / 2, y=HEIGHT - 50)
        self.bricks = self._build_bricks()
        self.lives = 3
        self.game_over = False
        self.score = 0
        self.combo_multiplier = 1

    def _build_bricks(self):
        bricks = []
        total_width = BRICK_COLS * (BRICK_WIDTH + BRICK_GAP) - BRICK_GAP
        start_x = (WIDTH - total_width) / 2
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = start_x + col * (BRICK_WIDTH + BRICK_GAP)
                y = BRICK_TOP_MARGIN + row * (BRICK_HEIGHT + BRICK_GAP)
                if row == 0:
                    brick_type = Brick.STRONG
                    hits_remaining = 3
                elif (row, col) in UNBREAKABLE_POSITIONS:
                    brick_type = Brick.UNBREAKABLE
                    hits_remaining = 1
                else:
                    brick_type = Brick.NORMAL
                    hits_remaining = 1
                bricks.append(
                    Brick(
                        x,
                        y,
                        BRICK_WIDTH,
                        BRICK_HEIGHT,
                        hits_remaining=hits_remaining,
                        brick_type=brick_type,
                    )
                )
        return bricks

    def _reset_ball(self):
        self.ball = Ball(x=WIDTH / 2, y=HEIGHT - 50)

    def handle_input(self, keys_pressed):
        if self.game_over:
            return

        dx = 0
        if keys_pressed[pygame.K_LEFT]:
            dx -= self.paddle.speed
        if keys_pressed[pygame.K_RIGHT]:
            dx += self.paddle.speed
        self.paddle.move(dx, WIDTH)

    def handle_keydown(self, key):
        if key == pygame.K_r and self.game_over:
            self._reset_game()

    def update(self):
        if self.game_over:
            return

        self.ball.update()
        self.ball.bounce_off_walls(WIDTH)

        if self.ball.get_rect().colliderect(self.paddle.get_rect()) and self.ball.vy > 0:
            self.ball.bounce_off_paddle(self.paddle.get_rect())

        for brick in self.bricks:
            if handle_ball_brick_collision(self.ball, brick):
                if brick.register_hit():
                    self.bricks.remove(brick)
                    self.score += BASE_BRICK_POINTS * self.combo_multiplier
                    self.combo_multiplier += 1
                break

        if self.ball.is_below(HEIGHT):
            self.lives -= 1
            self.combo_multiplier = 1
            if self.lives == 0:
                self.game_over = True
            else:
                self._reset_ball()

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.paddle, self.ball, self.bricks)
        hud_padding = 10
        hud_row_y = hud_padding + font.get_height() + 4
        renderer.draw_text(
            surface,
            font,
            f"Bricks left: {len(self.bricks)}",
            (hud_padding, hud_padding),
        )
        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}",
            (hud_padding, hud_row_y),
        )
        lives_text = font.render(f"Lives: {self.lives}", True, renderer.COLOR_TEXT)
        lives_x = surface.get_width() - lives_text.get_width() - hud_padding
        surface.blit(lives_text, (lives_x, hud_padding))
        combo_text = font.render(
            f"Combo: {self.combo_multiplier}x", True, renderer.COLOR_TEXT
        )
        combo_x = surface.get_width() - combo_text.get_width() - hud_padding
        surface.blit(combo_text, (combo_x, hud_row_y))
        if self.game_over:
            renderer.draw_banner(surface, font, "GAME OVER - Press R to restart")
