import copy
import random


import numpy as np
import pygame
from gymnasium import spaces
from pettingzoo import ParallelEnv
from pettingzoo.utils import parallel_to_aec, wrappers

STATE_WIDTH, STATE_HEIGHT = 780, 720
TILE_SIZE = 60
GRID_WIDTH = STATE_WIDTH // TILE_SIZE
GRID_HEIGHT = STATE_HEIGHT // TILE_SIZE
CAR_HEIGHT = 60
CAR_WIDTH = 40
FPS = 200
BACKGROUND_COLOR = (160, 160, 160)
LOT_COLOR = (255, 255, 0)
CAR_SPEED = 40
NUMBER_OF_ACTIONS = 5
NO_OF_OBSTACLES = 5
NO_OF_AGENTS = 4
NO_OF_LOTS = 4
MAX_EPISODE_LENGTH = 100


def grid_to_pixels(x, y):
    return x * TILE_SIZE, y * TILE_SIZE


def map_orientation_to_numeric(orientation):
    orientations = ["up", "down", "left", "right"]
    return orientations.index(orientation)



def env(render_mode=None):
    internal_render_mode = render_mode if render_mode != "ansi" else "human"
    env = raw_env(render_mode=internal_render_mode)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env

def raw_env(render_mode=None):
    env = ParkingMultiEnv(render_mode=render_mode)
    env = parallel_to_aec(env)
    return env


class ParkingMultiEnv(ParallelEnv):
    metadata = {"render_modes": ["human"], "name": "parking_multi_v0"}

    def __init__(self, render_mode=None):
        super().__init__()

        self.agents = ["player_" + str(r) for r in range(NO_OF_AGENTS)]

        self.agent_rects = {}
        self.agent_orientations = {}

        self.parking_rects = []
        self.obstacle_rects = []
        self.possible_agents = self.agents[:]
        self.successfully_parked = []

        self.render_mode = render_mode
        self.window = None
        self.off_screen_surface = None
        self.image = None
        self.clock = None
        self.isopen = True
        self.time_step = 0

        self.prng = None
        self.car_images = None
        self.obstacle_image = None



    def get_random_orientation(self, no_of_agents):
        # 0 -up, 1 - down, 2 - left, 3 - right
        generated_orientation = []
        while len(generated_orientation) < no_of_agents:
            generated_orientation.append(self.prng.choice(["up", "down", "left", "right"]))
        return generated_orientation

    def get_random_positions(self, num_rectangles, occupied_rects):
        generated_rects = []
        while len(generated_rects) < num_rectangles:
            new_rect = self.get_random_position(occupied_rects + generated_rects)
            generated_rects.append(new_rect)
        return generated_rects

    def get_random_position(self, occupied_rects):
        while True:
            position_tile = (
                self.prng.randint(0, GRID_WIDTH - 1),
                self.prng.randint(0, GRID_HEIGHT - 1)
            )
            position_rect = pygame.Rect(grid_to_pixels(*position_tile), (TILE_SIZE, TILE_SIZE))
            overlap = any(position_rect.colliderect(existing_rect) for existing_rect in occupied_rects)
            if not overlap:
                return position_rect


    def action_space(self, agent):
        return spaces.Discrete(NUMBER_OF_ACTIONS)

    def observation_space(self, agent):
        return spaces.Box(low=0, high=255, shape=(STATE_WIDTH, STATE_HEIGHT, 3), dtype=np.uint8)

    def state(self):
        return self.image

    def close(self):
        if self.window is not None:
            pygame.quit()
            self.window = None
            self.isopen = False

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

        for i in range(len(self.parking_rects)):
            pygame.draw.rect(self.off_screen_surface, (255, 255, 0), self.parking_rects[i])

        for i in range(len(self.obstacle_rects)):
            self.off_screen_surface.blit(self.obstacle_image, self.obstacle_rects[i])

        # render agents
        for agent in self.agents:
            orientation = self.agent_orientations[agent]
            car_sprite = None
            if orientation == "up":
                car_sprite = self.car_images[0]
            elif orientation == "down":
                car_sprite = self.car_images[1]
            elif orientation == "left":
                car_sprite = self.car_images[2]
            elif orientation == "right":
                car_sprite = self.car_images[3]
            self.off_screen_surface.blit(car_sprite, self.agent_rects[agent])

        for i in range(len(self.successfully_parked)):
            orientation = self.successfully_parked[i][1]
            car_sprite = None
            if orientation == "up":
                car_sprite = self.car_images[0]
            elif orientation == "down":
                car_sprite = self.car_images[1]
            elif orientation == "left":
                car_sprite = self.car_images[2]
            elif orientation == "right":
                car_sprite = self.car_images[3]
            self.off_screen_surface.blit(car_sprite, self.successfully_parked[i][0])

        self.image = pygame.surfarray.array3d(self.off_screen_surface)
        pygame.event.get()


    def render(self):
        if self.window is None:
            self.window = pygame.display.set_mode((STATE_WIDTH, STATE_HEIGHT))
        if self.clock is None:
            self.clock = pygame.time.Clock()
        self.window.blit(self.off_screen_surface, (0, 0))
        pygame.time.delay(150)
        pygame.display.flip()
        self.clock.tick(FPS)


    def reset(self, seed=None, options=None):
        self.prng = random.Random()
        if seed is not None:
            self.prng.seed(seed)
        else:
            self.prng.seed()
        self.successfully_parked = []
        self.time_step = 0
        self.agents = copy.copy(self.possible_agents)
        self.agent_orientations = dict(zip(self.agents, self.get_random_orientation(NO_OF_AGENTS)))

        self.parking_rects = self.get_random_positions(NO_OF_LOTS, [])
        self.obstacle_rects = self.get_random_positions(NO_OF_OBSTACLES, self.parking_rects)
        self.agent_rects = dict(zip(self.agents,
                                    self.get_random_positions(NO_OF_AGENTS, self.parking_rects + self.obstacle_rects)))



        infos = {i: {} for i in self.agents}

        self.fill_surface()  # self.image updated there
        observations = {i: self.image for i in self.agents}

        if self.render_mode == "human":
            self.render()

        return observations, infos

    def step(self, actions):
        rewards = {i: 0 for i in self.agents}
        terminated = {i: False for i in self.agents}
        truncated = {i: False for i in self.agents}
        infos = {i: {} for i in self.agents}

        self.time_step += 1

        if self.time_step >= MAX_EPISODE_LENGTH:  # Truncated
            self.agents = []

        agents_to_remove = set()

        for agent in actions.keys():
            action = actions[agent]
            if action == 3:  # 3 to go straight
                if self.agent_orientations[agent] == "up":
                    self.agent_rects[agent].y -= CAR_SPEED
                elif self.agent_orientations[agent] == "down":
                    self.agent_rects[agent].y += CAR_SPEED
                elif self.agent_orientations[agent] == "left":
                    self.agent_rects[agent].x -= CAR_SPEED
                elif self.agent_orientations[agent] == "right":
                    self.agent_rects[agent].x += CAR_SPEED
            elif action == 4:  # 4 to go straight
                if self.agent_orientations[agent] == "up":
                    self.agent_rects[agent].y += CAR_SPEED
                elif self.agent_orientations[agent] == "down":
                    self.agent_rects[agent].y -= CAR_SPEED
                elif self.agent_orientations[agent] == "left":
                    self.agent_rects[agent].x += CAR_SPEED
                elif self.agent_orientations[agent] == "right":
                    self.agent_rects[agent].x -= CAR_SPEED
            elif action == 1:  # 1 for turning left
                if self.agent_orientations[agent] == "up":
                    self.agent_orientations[agent] = "left"
                elif self.agent_orientations[agent] == "down":
                    self.agent_orientations[agent] = "right"
                elif self.agent_orientations[agent] == "left":
                    self.agent_orientations[agent] = "down"
                elif self.agent_orientations[agent] == "right":
                    self.agent_orientations[agent] = "up"
            elif action == 2:  # 1 for turning left
                if self.agent_orientations[agent] == "up":
                    self.agent_orientations[agent] = "right"
                elif self.agent_orientations[agent] == "down":
                    self.agent_orientations[agent] = "left"
                elif self.agent_orientations[agent] == "left":
                    self.agent_orientations[agent] = "up"
                elif self.agent_orientations[agent] == "right":
                    self.agent_orientations[agent] = "down"
            if self.agent_rects[agent].left < 0:
                self.agent_rects[agent].left = 0
            elif self.agent_rects[agent].right > STATE_WIDTH:
                self.agent_rects[agent].right = STATE_WIDTH
            if self.agent_rects[agent].top < 0:
                self.agent_rects[agent].top = 0
            elif self.agent_rects[agent].bottom > STATE_HEIGHT:
                self.agent_rects[agent].bottom = STATE_HEIGHT

            for other_agent in self.agents:
                if agent != other_agent:
                    if self.agent_rects[agent].colliderect(self.agent_rects[other_agent]):
                        rewards[agent] = rewards[agent]-500
                        rewards[other_agent] = rewards[agent]-500
                        terminated[agent] = True
                        terminated[other_agent] = True
                        agents_to_remove.add(agent)
                        agents_to_remove.add(other_agent)

            for obstacle_rect in self.obstacle_rects:
                if self.agent_rects[agent].colliderect(obstacle_rect):
                    rewards[agent] = rewards[agent] - 500
                    terminated[agent] = True
                    agents_to_remove.add(agent)

            for parking_rect in self.parking_rects:
                if self.agent_rects[agent].colliderect(parking_rect):
                    rewards[agent] = rewards[agent] + 2000
                    terminated[agent] = True
                    agents_to_remove.add(agent)
                    self.successfully_parked.append([parking_rect, self.agent_orientations[agent]])

            rewards[agent] = rewards[agent] - 1

        self.fill_surface()
        observations = {i: self.image for i in self.agents}

        for agent in agents_to_remove:
            del self.agent_rects[agent]
            del self.agent_orientations[agent]
            self.agents.remove(agent)

        if self.render_mode == "human":
            self.render()

        return observations, rewards, terminated, truncated, infos

environment = ParkingMultiEnv(render_mode="human")
observations, infos = environment.reset()



