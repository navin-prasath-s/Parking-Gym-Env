from gymnasium.wrappers import TimeLimit, FrameStack, GrayScaleObservation
from stable_baselines3 import PPO, DQN
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.logger import configure
from stable_baselines3.common.monitor import Monitor
from parking_multi_env import ParkingMultiEnv

from parking_env_feature import ParkingFeature

name = "multi"
tmp_path = f"./FeatureLogs/monitor/{name}"
new_logger = configure(tmp_path, ["csv", "tensorboard", "log"])

checkpoint_callback = CheckpointCallback(
  save_freq=50000,
  save_path=f"./FeatureLogs/models/{name}/checkpoint",
  name_prefix=f"{name}",
  save_replay_buffer=True,
  save_vecnormalize=True,
)
def make_gym_env():
    env = ParkingMultiEnv()
    env = Monitor(env, f"./FeatureLogs/monitor/{name}")
    return env

vec_env = make_vec_env(lambda: make_gym_env(), n_envs=14)

eval_callback = EvalCallback(vec_env, best_model_save_path=f"./FeatureLogs/models/{name}/best/",
                             log_path=f"./FeatureLogs/models/{name}/best/", eval_freq=5000,
                             deterministic=True, render=True)




model = DQN("MlpPolicy", vec_env, verbose=1, buffer_size=5000, exploration_fraction=0.8, seed=20, gradient_steps=200)

model.set_logger(new_logger)
model.learn(total_timesteps=1000000, callback=[checkpoint_callback, eval_callback], progress_bar=True)
model.save(f"./FeatureLogs/models/{name}/final/final_model")