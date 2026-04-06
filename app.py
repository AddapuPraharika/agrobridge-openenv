from fastapi import FastAPI
from contextlib import asynccontextmanager
from env import AgroBridgeEnv
from models import AgroBridgeAction

env = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global env
    env = AgroBridgeEnv()
    yield
    if env is not None:
        await env.close()


app = FastAPI(title="AgroBridge OpenEnv", version="1.0", lifespan=lifespan)


@app.get("/")
async def root():
    return {"status": "running", "message": "AgroBridge OpenEnv is live"}


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
    message = action.get("message", "")
    result = await env.step(AgroBridgeAction(message=message))
    return {
        "observation": result.observation,
        "reward": result.reward,
        "done": result.done,
    }


@app.get("/state")
async def state():
    return env.state()


@app.post("/close")
async def close():
    await env.close()
    return {"status": "closed"}