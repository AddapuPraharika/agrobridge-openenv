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
    return {"message": "AgroBridge OpenEnv is running"}


@app.post("/reset")
async def reset():
    result = await env.reset()
    return {
        "observation": result.observation,
        "reward": result.reward,
        "done": result.done,
    }


@app.post("/step")
async def step(action: dict):
    result = await env.step(AgroBridgeAction(message=action.get("message", "")))
    return {
        "observation": result.observation,
        "reward": result.reward,
        "done": result.done,
    }


@app.get("/state")
async def state():
    return env.state()
