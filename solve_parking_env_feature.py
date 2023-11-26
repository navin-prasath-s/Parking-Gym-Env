from gymnasium.wrappers import TimeLimit
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.logger import configure
from stable_baselines3.common.monitor import Monitor
from parking_env_feature import ParkingFeature

tmp_path = "./PEFlogs/parking_env_feature_log/"
new_logger = configure(tmp_path, ["csv", "tensorboard", "log"])

checkpoint_callback = CheckpointCallback(
  save_freq=1000,
  save_path="./PEFlogs/models/",
  name_prefix="parking_env_feature",
  save_replay_buffer=True,
  save_vecnormalize=True,
)

def make_gym_env():
    env = ParkingFeature()
    env = TimeLimit(env, 1000)
    env = Monitor(env, "PEFlogs/monitor")
    return env

vec_env = make_vec_env(lambda: make_gym_env(), n_envs=12)

eval_callback = EvalCallback(vec_env, best_model_save_path="./logs/best/",
                             log_path="./PEFlogs/logged/", eval_freq=1000,
                             deterministic=True, render=False)

model = PPO("MlpPolicy", vec_env, verbose=1)

model.set_logger(new_logger)
model.learn(total_timesteps=10000, callback=[checkpoint_callback, eval_callback])
model.save("PEFlogs/parking_env_feature_final_model")