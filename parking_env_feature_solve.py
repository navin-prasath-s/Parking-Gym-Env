from gymnasium.wrappers import TimeLimit, FrameStack, GrayScaleObservation
from stable_baselines3 import PPO, DQN
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.logger import configure
from stable_baselines3.common.monitor import Monitor

from parking_env_feature import ParkingFeature

name = "PPOent_coef_high"
tmp_path = f"./FeatureLogsPPO/monitor/{name}"
new_logger = configure(tmp_path, ["csv", "tensorboard", "log"])

checkpoint_callback = CheckpointCallback(
  save_freq=1000,
  save_path=f"./FeatureLogs/models/{name}/checkpoint",
  name_prefix=f"{name}",
  save_replay_buffer=True,
  save_vecnormalize=True,
)
def make_gym_env():
    env = ParkingFeature()
    env = TimeLimit(env, 150)
    env = Monitor(env, f"./FeatureLogs/monitor/{name}")
    return env

vec_env = make_vec_env(lambda: make_gym_env(), n_envs=14)

eval_callback = EvalCallback(vec_env, best_model_save_path=f"./FeatureLogs/models/{name}/best/",
                             log_path=f"./FeatureLogs/models/{name}/best/", eval_freq=3000,
                             deterministic=True, render=True)




# model = DQN("MlpPolicy", vec_env, verbose=1, buffer_size=200, exploration_fraction=0.9, seed=20, learning_rate=0.1)
model = PPO("MlpPolicy", vec_env, verbose=1, ent_coef=0.8)

model.set_logger(new_logger)
model.learn(total_timesteps=100000, callback=[checkpoint_callback, eval_callback], progress_bar=True)
model.save(f"./FeatureLogs/models/{name}/final/final_model")