from stable_baselines3 import PPO, DQN
from stable_baselines3.common.evaluation import evaluate_policy

from parking_env_feature import ParkingFeature

model = DQN.load("FeatureLogs/models/dqn_feature_default/best/best_model.zip", env=ParkingFeature(render_mode="human"))
# mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10, deterministic=True, render=False)
# print(mean_reward)
# print(std_reward)

vec_env = model.get_env()
obs = vec_env.reset()

for _ in range(1000):
    action, states = model.predict(obs)
    obs, rewards, dones, info = vec_env.step(action)
    print(obs)
    vec_env.render("human")


