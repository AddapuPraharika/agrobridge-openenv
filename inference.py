from env import AgroBridgeEnv

env = AgroBridgeEnv()

state = env.reset()

print("Current Job:", state)

print("Environment State:", env.state())

action = 0

state, reward, done = env.step(action)

print("Reward:", reward)