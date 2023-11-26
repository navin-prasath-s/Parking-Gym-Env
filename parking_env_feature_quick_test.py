from parking_env_feature import ParkingFeature

env = ParkingFeature()

print(env.action_space)
print(env.observation_space)

obs, info_ = env.reset(seed=13)
print(obs)


obs, reward, terminated, truncated, info = env.step(3)
obs, reward, terminated, truncated, info = env.step(3)
obs, reward, terminated, truncated, info = env.step(3)
obs, reward, terminated, truncated, info = env.step(3)
obs, reward, terminated, truncated, info = env.step(3)
obs, reward, terminated, truncated, info = env.step(3)
obs, reward, terminated, truncated, info = env.step(3)
obs, reward, terminated, truncated, info = env.step(3)
obs, reward, terminated, truncated, info = env.step(3)
obs, reward, terminated, truncated, info = env.step(3)
obs, reward, terminated, truncated, info = env.step(3)
print(obs)
print(reward)