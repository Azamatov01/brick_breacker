import gym
import pygame
import numpy as np
import random
from gym import spaces

class BrickBreakerEnv(gym.Env):
    def __init__(self):
        super(BrickBreakerEnv, self).__init__()

        self.WIDTH = 800
        self.HEIGHT = 600
        self.PADDLE_WIDTH = 100
        self.PADDLE_HEIGHT = 10
        self.BALL_RADIUS = 10
        self.BLOCK_WIDTH = 75
        self.BLOCK_HEIGHT = 30
        self.BLOCK_PADDING = 5

        self.paddle_x = self.WIDTH // 2 - self.PADDLE_WIDTH // 2
        self.paddle_y = self.HEIGHT - 30
        self.paddle_speed = 10

        self.ball_x = self.WIDTH // 2
        self.ball_y = self.HEIGHT // 2
        self.ball_dx, self.ball_dy = 4, -4
        self.ball_color = random.choice([pygame.Color('red'), pygame.Color('green'), pygame.Color('blue')])

        self.blocks = []
        for row in range(5):
            for col in range(10):
                x = col * (self.BLOCK_WIDTH + self.BLOCK_PADDING) + 10
                y = row * (self.BLOCK_HEIGHT + self.BLOCK_PADDING) + 10
                color = random.choice([pygame.Color('red'), pygame.Color('green'), pygame.Color('blue')])
                block = pygame.Rect(x, y, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)
                self.blocks.append((block, color))

        self.observation_space = spaces.Box(low=0, high=255, shape=(self.WIDTH, self.HEIGHT, 3), dtype=np.uint8)
        self.action_space = spaces.Discrete(3)

    def reset(self):
        self.paddle_x = self.WIDTH // 2 - self.PADDLE_WIDTH // 2
        self.paddle_y = self.HEIGHT - 30
        self.ball_x = self.WIDTH // 2
        self.ball_y = self.HEIGHT // 2
        self.ball_dx, self.ball_dy = 4, -4
        self.blocks = []
        for row in range(5):
            for col in range(10):
                x = col * (self.BLOCK_WIDTH + self.BLOCK_PADDING) + 10
                y = row * (self.BLOCK_HEIGHT + self.BLOCK_PADDING) + 10
                color = random.choice([pygame.Color('red'), pygame.Color('green'), pygame.Color('blue')])
                block = pygame.Rect(x, y, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)
                self.blocks.append((block, color))

        return np.zeros((self.WIDTH, self.HEIGHT, 3), dtype=np.uint8)

    def step(self, action):
        if action == 1:
            self.paddle_x -= self.paddle_speed
        elif action == 2:
            self.paddle_x += self.paddle_speed

        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        if self.ball_x - self.BALL_RADIUS <= 0 or self.ball_x + self.BALL_RADIUS >= self.WIDTH:
            self.ball_dx = -self.ball_dx
        if self.ball_y - self.BALL_RADIUS <= 0:
            self.ball_dy = -self.ball_dy
        if self.ball_y + self.BALL_RADIUS >= self.HEIGHT:
            return np.zeros((self.WIDTH, self.HEIGHT, 3), dtype=np.uint8), -1, True, {}

        paddle_rect = pygame.Rect(self.paddle_x, self.paddle_y, self.PADDLE_WIDTH, self.PADDLE_HEIGHT)
        if paddle_rect.collidepoint(self.ball_x, self.ball_y + self.BALL_RADIUS):
            self.ball_dy = -abs(self.ball_dy)

        ball_rect = pygame.Rect(self.ball_x - self.BALL_RADIUS, self.ball_y - self.BALL_RADIUS, self.BALL_RADIUS * 2, self.BALL_RADIUS * 2)
        for block, color in self.blocks[:]:
            if block.colliderect(ball_rect):
                if self.ball_color == color:
                    self.blocks.remove((block, color))

        reward = 1 if len(self.blocks) < len(self.blocks) else 0
        return np.zeros((self.WIDTH, self.HEIGHT, 3), dtype=np.uint8), reward, False, {}

    def render(self):
        pass

    def close(self):
        pygame.quit()
