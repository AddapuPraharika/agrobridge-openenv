from env import AgroBridgeEnv

def log_start():
    print("[START] task=agrobridge env=agrobridge model=baseline", flush=True)

def log_step(step, action, reward, done):
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null", flush=True)

def log_end(success, steps, score, rewards):
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)

env = AgroBridgeEnv()

log_start()

rewards = []

state = env.reset()

for step in range(1, 4):
    action = step % 3
    state, reward, done = env.step(action)

    log_step(step, action, reward, done)

    rewards.append(reward)

    if done:
        break

score = sum(rewards) / len(rewards)

log_end(True, len(rewards), score, rewards)