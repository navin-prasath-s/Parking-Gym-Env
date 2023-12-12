from parking_multi_env import ParkingMultiEnv

environment = ParkingMultiEnv(render_mode="human")

observations, infos = environment.reset()


while True:
    while environment.agents:
        actions = {agent: environment.action_space(agent).sample() for agent in environment.agents}
        observations, rewards, terminations, truncations, infos = environment.step(actions)
    environment.reset()

