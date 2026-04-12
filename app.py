from fastapi import FastAPI
from env import AgroBridgeEnv
from models import AgroBridgeAction

app = FastAPI()
env = None


@app.on_event("startup")
async def startup():
    global env
    env = AgroBridgeEnv()


@app.get("/")
async def root():
    return {"message": "AgroBridge OpenEnv environment is running"}


@app.post("/reset")
async def reset():
    result = await env.reset()
    return {
        "observation": result.observation.echoed_message,
        "reward": result.reward,
        "done": result.done
    }


@app.post("/step")
async def step(action: AgroBridgeAction):
    result = await env.step(action)
    return {
        "observation": result.observation.echoed_message,
        "reward": result.reward,
        "done": result.done
    }


@app.get("/state")
async def state():
    return env.state()
