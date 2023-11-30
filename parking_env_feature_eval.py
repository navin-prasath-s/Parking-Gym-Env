from stable_baselines3 import PPO, DQN
from parking_env_feature import ParkingFeature

model = PPO.load("FeatureLogs/models/ppo_default/checkpoint/ppo_default_280000_steps.zip", env=ParkingFeature(render_mode="human"))
vec_env = model.get_env()
obs = vec_env.reset()

for _ in range(100):
    action, states = model.predict(obs)
    obs, rewards, dones, info = vec_env.step(action)
    print(obs)
    vec_env.render()

    # if dones:
    #     break
