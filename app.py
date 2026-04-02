from fastapi import FastAPI
from env import AgroBridgeEnv, AgroBridgeAction

app = FastAPI()

env = AgroBridgeEnv()


@app.get("/")
async def root():
    return {"message": "AgroBridge OpenEnv environment is running"}


@app.post("/reset")
async def reset():
    result = await env.reset()

    return {
        "observation": result.observation,
        "reward": result.reward,
        "done": result.done
    }



@app.post("/step")
async def step(action: dict):

    message = action.get("message", "")

    result = await env.step(
        AgroBridgeAction(message=message)
    )

    return {
        "observation": result.observation,
        "reward": result.reward,
        "done": result.done
    }


@app.get("/state")
async def state():
    return env.state()