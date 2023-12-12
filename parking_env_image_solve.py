import numpy as np
from gymnasium.wrappers import TimeLimit, GrayScaleObservation
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.logger import configure
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import VecFrameStack, VecTransposeImage
from parking_env_image import ParkingImage

name = "ppo_crazy_high"
tmp_path = f"./ImageLogs/monitor/{name}"
new_logger = configure(tmp_path, ["csv", "tensorboard", "log"])

checkpoint_callback = CheckpointCallback(
  save_freq=500,
  save_path=f"./ImageLogs/models/{name}/checkpoint",
  name_prefix=f"{name}",
  save_replay_buffer=True,
  save_vecnormalize=True,
)

def make_gym_env():
    env = ParkingImage()
    env = TimeLimit(env, 400)
    env = GrayScaleObservation(env, keep_dim=True)
    env = Monitor(env, f"./ImageLogs/monitor/{name}")
    return env

vec_env = make_vec_env(lambda: make_gym_env(), n_envs=1)
vec_env = VecFrameStack(vec_env, 3, channels_order="last")

eval_vec_env = make_vec_env(lambda: make_gym_env(), n_envs=1)
eval_vec_env = VecFrameStack(eval_vec_env, 3, channels_order="last")
eval_vec_env = VecTransposeImage(eval_vec_env)
eval_callback = EvalCallback(eval_vec_env, best_model_save_path=f"./ImageLogs/models/{name}/best/",
                             log_path=f"./ImageLogs/models/{name}/best/", eval_freq=50,
                             deterministic=True, render=False)



model = PPO("CnnPolicy", vec_env, verbose=2, n_steps=512, ent_coef=0.5, learning_rate=0.01, clip_range=0.6)
model.set_logger(new_logger)
model.learn(total_timesteps=50000, callback=[checkpoint_callback, eval_callback], progress_bar=True)
model.save(f"./ImageLogs/models/{name}/final/final_model")