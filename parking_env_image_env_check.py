from stable_baselines3.common.env_checker import check_env
from parking_env_image import ParkingImage


env = ParkingImage()

check_env(env)