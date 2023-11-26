from stable_baselines3 import PPO
from parking_env_feature import ParkingFeature

model = PPO.load("PEFlogs/parking_env_feature_final_model.zip", env=ParkingFeature(render_mode="human"))
vec_env = model.get_env()
obs = vec_env.reset()

for _ in range(1000):
    action, states = model.predict(obs)
    obs, rewards, dones, info = vec_env.step(action)
    vec_env.render()
