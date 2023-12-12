from parking_env_feature import ParkingFeature

env = ParkingFeature(render_mode="human")
obs, info_ = env.reset()
print(obs)

for _ in range(100):
    action = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action)
    print(observation)
    if terminated or truncated:
        observation, info = env.reset()

