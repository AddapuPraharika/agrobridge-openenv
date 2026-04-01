from fastapi import FastAPI
from env import AgroBridgeEnv

app = FastAPI()

@app.get("/")
def run_env():
    env = AgroBridgeEnv()

    state = env.reset()
    action = 0

    state, reward, done = env.step(action)

    return {
        "job": state,
        "reward": reward,
        "done": done
    }