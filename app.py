from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from env import AgroBridgeEnv
from models import AgroBridgeAction, StepResult

env: AgroBridgeEnv | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global env
    env = AgroBridgeEnv()
    yield
    if env is not None:
        await env.close()


app = FastAPI(
    title="AgroBridge OpenEnv",
    version="2.0",
    description=(
        "An OpenEnv-compatible reinforcement learning environment for "
        "intelligent agricultural labor matching in rural India. "
        "Built for the Meta × PyTorch OpenEnv Hackathon."
    ),
    lifespan=lifespan,
)


def _require_env() -> AgroBridgeEnv:
    if env is None:
        raise HTTPException(status_code=503, detail="Environment not initialised.")
    return env


@app.get("/", tags=["Health"])
async def root():
    return {"status": "running", "message": "AgroBridge OpenEnv is live", "version": "2.0"}


@app.post("/reset", response_model=StepResult, tags=["Environment"])
async def reset():
    """Reset the environment and start a new episode. Returns the initial observation."""
    return await _require_env().reset()


@app.post("/step", response_model=StepResult, tags=["Environment"])
async def step(action: AgroBridgeAction):
    """
    Take one step in the environment by assigning a farmer.

    The agent message should name the farmer and optionally explain the reasoning.
    Example: `{"message": "Assign Mahesh because he is a senior spraying expert."}`
    """
    e = _require_env()
    if e.current_task is None:
        raise HTTPException(status_code=400, detail="Call /reset before /step.")
    return await e.step(action)


@app.get("/state", tags=["Environment"])
async def state():
    """Return the full current environment state including all farmers and episode progress."""
    return _require_env().state()


@app.post("/close", tags=["Environment"])
async def close():
    """Cleanly close the environment and reset internal state."""
    await _require_env().close()
    return {"status": "closed"}