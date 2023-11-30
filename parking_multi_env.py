import gymnasium as gym
from typing import Optional
import numpy as np
import pygame
from gymnasium import spaces
import pettingzoo
from pettingzoo.utils import agent_selector
from pettingzoo import ParallelEnv
from pettingzoo.utils import parallel_to_aec, wrappers
from pettingzoo.utils.env import AgentID

STATE_WIDTH, STATE_HEIGHT = 780, 720
TILE_SIZE = 60
GRID_WIDTH = STATE_WIDTH // TILE_SIZE
GRID_HEIGHT = STATE_HEIGHT // TILE_SIZE
CAR_HEIGHT = 60
CAR_WIDTH = 40
FPS = 200
WHITE = (255, 255, 255)
CAR_SPEED = 60
NUMBER_OF_ACTIONS= 5
NO_OF_OBSTACLES = 4
NO_OF_AGENTS = 4


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
        self.possible_agents = self.agents[:]
        self.render_mode = render_mode
        self.window = None
        self.off_screen_surface = None
        self.clock = None
        self.isopen = True

        self.car_images = None
        self.obstacle_image = None

        self.action_space = {i: spaces.Discrete(NUMBER_OF_ACTIONS) for i in self.agents}
        self.observation_spaces = {i: spaces.Box(low=0, high=255,
                                            shape=(STATE_HEIGHT, STATE_WIDTH, 3), dtype=np.uint8) for i in self.agents}

    def action_space(self, agent):
        return self.action_spaces[agent]

    def observation_space(self, agent):
        return self.observation_spaces[agent]

    def close(self):
        if self.window is not None:
            pygame.quit()
            self.window = None
            self.isopen = False


    def reset(self, seed=None, options=None):
        """
        Reset needs to initialize the `agents` attribute and must set up the
        environment so that render(), and step() can be called without issues.
        Here it initializes the `num_moves` variable which counts the number of
        hands that are played.
        Returns the observations for each agent
        """
        # self.agents = self.possible_agents[:]
        # self.num_moves = 0
        # observations = {agent: NONE for agent in self.agents}
        # infos = {agent: {} for agent in self.agents}
        # self.state = observations
        #
        # return observations, infos
