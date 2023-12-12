from parking_multi_env import ParkingMultiEnv
from parking_multi_env import env
from pettingzoo.test import parallel_api_test
from pettingzoo.test import performance_benchmark
from pettingzoo.test import test_save_obs

# parallel_api_test(env, num_cycles=1000)
# performance_benchmark(env)
test_save_obs(env)