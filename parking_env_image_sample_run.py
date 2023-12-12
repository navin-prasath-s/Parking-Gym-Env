from parking_env_image import ParkingImage

env = ParkingImage(render_mode="human")
obs, info_ = env.reset(seed=13)
print(obs)

for _ in range(100000):
    action = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action)
    print(reward)
    if terminated or truncated:
        observation, info = env.reset()
