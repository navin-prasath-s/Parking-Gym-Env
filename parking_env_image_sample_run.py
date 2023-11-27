from parking_env_image import ParkingImage

env = ParkingImage()
obs, info_ = env.reset(seed=13)
print(obs)

for _ in range(100):
    action = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action)
    print(observation)
    if terminated or truncated:
        observation, info = env.reset()
