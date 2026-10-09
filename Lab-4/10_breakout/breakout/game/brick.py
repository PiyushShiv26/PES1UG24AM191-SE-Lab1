"""
Brick: a single destructible block.
"""

import pygame


class Brick:
    NORMAL = "normal"
    STRONG = "strong"
    UNBREAKABLE = "unbreakable"

    COLORS = {
        NORMAL: (200, 90, 90),
        STRONG: (230, 170, 60),
        UNBREAKABLE: (120, 120, 130),
    }

    def __init__(
        self, x, y, width, height, hits_remaining=1, color=None,
        brick_type=NORMAL,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hits_remaining = hits_remaining
        self.brick_type = brick_type
        self.color = color if color is not None else self.COLORS[brick_type]

    def register_hit(self):
        if self.brick_type == self.UNBREAKABLE:
            return False

        self.hits_remaining -= 1
        return self.hits_remaining <= 0

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
