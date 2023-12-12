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
FPS = 200
BACKGROUND_COLOR = (160, 160, 160)
CAR_SPEED = 60
NUMBER_OF_ACTIONS = 5
NO_OF_OBSTACLES = 4


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
        self.off_screen_surface = None
        self.clock = None
        self.isopen = True
        self.car_images = None
        self.obstacle_image = None
        self.reward = 0

        self.current = ()


        self.image = None

        self.car_rect = None
        self.car_orientation = ""
        self.parking_rect = None
        self.obstacle_rects = np.array([])
        self.is_visited = set()
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
        while True:
            lot_tile = (self.np_random.integers(0, GRID_WIDTH), self.np_random.integers(0, GRID_HEIGHT))
            parking_rect = pygame.Rect(grid_to_pixels(*lot_tile), (TILE_SIZE, TILE_SIZE))
            if not parking_rect.colliderect(self.car_rect):
                return parking_rect

    def get_random_obstacle_positions(self):
        obstacle_rects = []
        while len(obstacle_rects) < NO_OF_OBSTACLES:
            obstacle_tile = (self.np_random.integers(0, GRID_WIDTH), self.np_random.integers(0, GRID_HEIGHT))
            obstacle_rect = pygame.Rect(grid_to_pixels(*obstacle_tile), (TILE_SIZE, TILE_SIZE))

            if not obstacle_rect.colliderect(self.car_rect) and not obstacle_rect.colliderect(self.parking_rect):
                overlap = False
                for existing_obstacle in obstacle_rects:
                    if obstacle_rect.colliderect(existing_obstacle):
                        overlap = True
                        break

                if not overlap:
                    obstacle_rects.append(obstacle_rect)
        return obstacle_rects

    def get_random_orientation(self):
        # 0 -up, 1 - down, 2 - left, 3 - right
        orient = self.np_random.choice(["up", "down", "left", "right"])
        return orient

    def reset(self, *, seed: Optional[int] = None, options: Optional[dict] = None):
        super().reset(seed=seed)
        self.car_rect = self.get_random_car_position()
        self.car_orientation = self.get_random_orientation()
        self.parking_rect = self.get_random_parking_position()
        self.obstacle_rects = self.get_random_obstacle_positions()
        self.fill_surface() # self.image ipdated in fill
        self.current = (self.car_rect.x, self.car_rect.y)

        if self.render_mode == "human":
            self.render()

        return self.image, {}

    def close(self):
        if self.off_screen_surface is not None:
            self.isopen = False
            pygame.quit()

    def fill_surface(self):
        if self.car_images is None:
            self.car_images = [pygame.image.load("assets/car-up.png"), pygame.image.load("assets/car-down.png"),
                          pygame.image.load("assets/car-left.png"), pygame.image.load("assets/car-right.png")]
            self.obstacle_image = pygame.image.load("assets/obstacle.png")
            pygame.init()
            pygame.display.init()
            pygame.display.set_caption("Car Parking Game")
        self.off_screen_surface = pygame.Surface((STATE_WIDTH, STATE_HEIGHT))
        self.off_screen_surface.fill(BACKGROUND_COLOR)
        car_sprite = None
        if self.car_orientation == "up":
            car_sprite = self.car_images[0]
        elif self.car_orientation == "down":
            car_sprite = self.car_images[1]
        elif self.car_orientation == "left":
            car_sprite = self.car_images[2]
        elif self.car_orientation == "right":
            car_sprite = self.car_images[3]

        self.off_screen_surface.blit(car_sprite, self.car_rect)
        for obstacle_rect in self.obstacle_rects:
            self.off_screen_surface.blit(self.obstacle_image, obstacle_rect)
        pygame.draw.rect(self.off_screen_surface, (100, 100, 100), self.parking_rect)

        self.image = pygame.surfarray.array3d(self.off_screen_surface)
        pygame.event.get()


    def render(self):
        if self.window is None:
            self.window = pygame.display.set_mode((STATE_WIDTH, STATE_HEIGHT))
        if self.clock is None:
            self.clock = pygame.time.Clock()
        self.window.blit(self.off_screen_surface, (0, 0))
        pygame.display.flip()
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

        self.current = (self.car_rect.x, self.car_rect.y)
        terminated = False
        if self.parking_rect.colliderect(self.car_rect):
            self.reward = 2000
            terminated = True
        else:
            for obstacle_rect in self.obstacle_rects:
                if self.car_rect.colliderect(obstacle_rect):
                    self.reward = -1000
                    terminated = True
                    break
            else:
                if self.current in self.is_visited:
                    self.reward = -1
                else:
                    self.is_visited.add(self.current)
                    self.reward = 10


        self.fill_surface()

        if self.render_mode == "human":
            self.render()

        return self.image, self.reward, terminated, False, {}




