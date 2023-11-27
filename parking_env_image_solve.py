import numpy as np
from gymnasium.wrappers import TimeLimit, GrayScaleObservation
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.logger import configure
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import VecFrameStack
from parking_env_image import ParkingImage

tmp_path = "./PEIlogs/monitor/"
new_logger = configure(tmp_path, ["csv", "tensorboard", "log"])

checkpoint_callback = CheckpointCallback(
  save_freq=1000,
  save_path="./PEIlogs/models/",
  name_prefix="parking_env_image",
  save_replay_buffer=True,
  save_vecnormalize=True,
)

def make_gym_env():
    env = ParkingImage()
    env = TimeLimit(env, 300)
    env = GrayScaleObservation(env, keep_dim=True)
    env = Monitor(env, "./PEIlogs/monitor")
    return env

vec_env = make_vec_env(lambda: make_gym_env(), n_envs=4)

vec_env = VecFrameStack(vec_env, 1, channels_order="last")

eval_callback = EvalCallback(vec_env, best_model_save_path="./PEIlogs/best/",
                             log_path="./PEIlogs/best/", eval_freq=1000,
                             deterministic=True, render=False)


print(vec_env.reset().shape)
model = PPO("CnnPolicy", vec_env, verbose=1)
model.set_logger(new_logger)

model.learn(total_timesteps=50000, callback=[checkpoint_callback, eval_callback])
model.save("PEIlogs/parking_env_image_final_model")