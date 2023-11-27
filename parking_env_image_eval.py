from gymnasium import spaces
from gymnasium.wrappers import GrayScaleObservation
from stable_baselines3 import PPO
from stable_baselines3.common.preprocessing import is_image_space

from parking_env_image import ParkingImage

env = ParkingImage(render_mode="human")
env = GrayScaleObservation(env, keep_dim=True)

model = PPO.load("PEIlogs/best/best_model.zip", env)


vec_env = model.get_env()
obs = vec_env.reset()

for _ in range(1000):
    action, states = model.predict(obs)
    obs, rewards, dones, info = vec_env.step(action)
    vec_env.render()

    if dones:
        break