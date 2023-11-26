from stable_baselines3.common.env_checker import check_env
from parking_env_feature import ParkingFeature


env = ParkingFeature()

check_env(env)