import gymnasium as gym
from typing import Optional

import numpy as np
import pygame
from gymnasium import spaces



STATE_WIDTH, STATE_HEIGHT = 720, 720
TILE_SIZE = 60
GRID_WIDTH = STATE_WIDTH // TILE_SIZE
GRID_HEIGHT = STATE_HEIGHT // TILE_SIZE
CAR_HEIGHT = 60
CAR_WIDTH = 40
FPS = 60
WHITE = (255, 255, 255)
CAR_SPEED = 60
NUMBER_OF_ACTIONS= 5


def grid_to_pixels(x, y):
    return x * TILE_SIZE, y * TILE_SIZE


def map_orientation_to_numeric(orientation):
    orientations = ["up", "down", "left", "right"]
    return orientations.index(orientation)


class ParkingImage(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": FPS, }

    def __init__(self, render_mode: Optional[str] = None):

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.screen_width = STATE_WIDTH
        self.screen_height = STATE_HEIGHT

        self.window = None
        self.clock = None
        self.isopen = True
        self.car_images = None
        self.reward = 0

        # self.orientation = -1
        # self.current = ()
        # self.lot = ()
        # self.delta = ()

        self.image = None

        self.car_rect = None
        self.car_orientation = ""
        self.parking_rect = None

        self.action_space = spaces.Discrete(NUMBER_OF_ACTIONS)
        self.observation_space = spaces.Box(low=0, high=255,
                                            shape=(STATE_HEIGHT, STATE_WIDTH, 3), dtype=np.uint8)

    def get_random_car_position(self):
        car_tile = (self.np_random.integers(0, GRID_WIDTH), self.np_random.integers(0, GRID_HEIGHT))
        car_rect = pygame.Rect(grid_to_pixels(*car_tile), (TILE_SIZE, TILE_SIZE))
        car_rect.x += (TILE_SIZE - CAR_WIDTH) // 2
        car_rect.y += (TILE_SIZE - CAR_HEIGHT) // 2
        return car_rect

    def get_random_parking_position(self):
        lot_tile = (self.np_random.integers(0, GRID_WIDTH), self.np_random.integers(0, GRID_HEIGHT))
        return pygame.Rect(grid_to_pixels(*lot_tile), (TILE_SIZE, TILE_SIZE))

    def get_random_orientation(self):
        # 0 -up, 1 - down, 2 - left, 3 - right
        return self.np_random.choice(["up", "down", "left", "right"])

    def reset(self, *, seed: Optional[int] = None, options: Optional[dict] = None):
        super().reset(seed=seed)
        self.car_rect = self.get_random_car_position()
        self.car_orientation = self.get_random_orientation()
        self.parking_rect = self.get_random_parking_position()
        self.image = np.zeros((STATE_HEIGHT, STATE_WIDTH, 3), dtype=np.uint8)

        if self.render_mode == "human":
            self.render()
            self.display_render()

        return self.image, {}

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            self.isopen = False
            pygame.quit()

    def render(self):
        if self.window is None:
            pygame.init()
            pygame.display.init()
            pygame.display.set_caption("Car Parking Game")
            self.window = pygame.display.set_mode((STATE_WIDTH, STATE_HEIGHT))

        if self.clock is None:
            self.clock = pygame.time.Clock()

        if self.car_images is None:
            self.car_images = [pygame.image.load("assets/car-up.png"), pygame.image.load("assets/car-down.png"),
                          pygame.image.load("assets/car-left.png"), pygame.image.load("assets/car-right.png")]


        self.window.fill(WHITE)
        car_sprite = None
        if self.car_orientation == "up":
            car_sprite = self.car_images[0]
        elif self.car_orientation == "down":
            car_sprite = self.car_images[1]
        elif self.car_orientation == "left":
            car_sprite = self.car_images[2]
        elif self.car_orientation == "right":
            car_sprite = self.car_images[3]

        self.window.blit(car_sprite, self.car_rect)
        pygame.draw.rect(self.window, (255, 255, 0), self.parking_rect)
        self.image = pygame.surfarray.array3d(self.window)


    def display_render(self):
        pygame.display.flip()
        pygame.time.delay(200)
        self.clock.tick(FPS)

    def step(self, action):
        if action == 3: # 3 to go straight
            if self.car_orientation == "up":
                self.car_rect.y -= CAR_SPEED
            elif self.car_orientation == "down":
                self.car_rect.y += CAR_SPEED
            elif self.car_orientation == "left":
                self.car_rect.x -= CAR_SPEED
            elif self.car_orientation == "right":
                self.car_rect.x += CAR_SPEED

        elif action == 4:  # 4 to go backwards
            if self.car_orientation == "up":
                self.car_rect.y += CAR_SPEED
            elif self.car_orientation == "down":
                self.car_rect.y -= CAR_SPEED
            elif self.car_orientation == "left":
                self.car_rect.x += CAR_SPEED
            elif self.car_orientation == "right":
                self.car_rect.x -= CAR_SPEED

        elif action == 1:  # 1 for turning left
            if self.car_orientation == "up":
                self.car_orientation = "left"
            elif self.car_orientation == "down":
                self.car_orientation = "right"
            elif self.car_orientation == "left":
                self.car_orientation = "down"
            elif self.car_orientation == "right":
                self.car_orientation = "up"

        elif action == 2:  # 2 for turning right
            if self.car_orientation == "up":
                self.car_orientation = "right"
            elif self.car_orientation == "down":
                self.car_orientation = "left"
            elif self.car_orientation == "left":
                self.car_orientation = "up"
            elif self.car_orientation == "right":
                self.car_orientation = "down"

        if self.car_rect.left < 0:
            self.car_rect.left = 0
        elif self.car_rect.right > STATE_WIDTH:
            self.car_rect.right = STATE_WIDTH
        if self.car_rect.top < 0:
            self.car_rect.top = 0
        elif self.car_rect.bottom > STATE_HEIGHT:
            self.car_rect.bottom = STATE_HEIGHT

        terminated = False
        if self.parking_rect.colliderect(self.car_rect):
            self.reward = 2000
            terminated = True
        else:
            self.reward = -1

        self.render()

        if self.render_mode == "human":
            self.display_render()

        return self.image, self.reward, terminated, False, {}




