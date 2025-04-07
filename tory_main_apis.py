from fastapi import FastAPI, Request as FastAPIRequest, Query
from fastapi.middleware.cors import CORSMiddleware
from tory_coodinator_agent import (
    coordinator,
    send_tokenomics_queue,
    send_unlocks_queue,
    send_financials_queue,
    tokenomics_responses,
    unlocks_responses,
    financials_responses
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok"}

# ---- POST endpoints to enqueue messages ----

@app.post("/send/tokenomics")
async def send_tokenomics(request: FastAPIRequest):
    data = await request.json()
    uuid = data.get("uuid")
    timestamp = data.get("timestamp")
    token = data.get("token")
    print(f"✅ Queuing tokenomics: {token}, {uuid}, {timestamp}")
    await send_tokenomics_queue.put({"uuid": uuid, "timestamp": timestamp, "token": token})
    return {"status": "queued", "uuid": uuid, "timestamp": timestamp, "token": token}

@app.post("/send/unlocks")
async def send_unlocks(request: FastAPIRequest):
    data = await request.json()
    uuid = data.get("uuid")
    timestamp = data.get("timestamp")
    token = data.get("token")
    print(f"✅ Queuing unlocks: {token}, {uuid}, {timestamp}")
    await send_unlocks_queue.put({"uuid": uuid, "timestamp": timestamp, "token": token})
    return {"status": "queued", "uuid": uuid, "timestamp": timestamp, "token": token}

@app.post("/send/financials")
async def send_financials(request: FastAPIRequest):
    data = await request.json()
    uuid = data.get("uuid")
    timestamp = data.get("timestamp")
    token = data.get("token")
    print(f"✅ Queuing financials: {token}, {uuid}, {timestamp}")
    await send_financials_queue.put({"uuid": uuid, "timestamp": timestamp, "token": token})
    return {"status": "queued", "uuid": uuid, "timestamp": timestamp, "token": token}

# ---- GET endpoints to fetch/poll responses ----

@app.get("/history/tokenomics")
async def get_tokenomics_response(uuid: str = Query(...), timestamp: int = Query(...)):
    for i, entry in enumerate(tokenomics_responses):
        if entry["uuid"] == uuid and entry["timestamp"] == timestamp:
            return tokenomics_responses.pop(i)
    return {"error": "Response not found"}

@app.get("/history/unlocks")
async def get_unlocks_response(uuid: str = Query(...), timestamp: int = Query(...)):
    for i, entry in enumerate(unlocks_responses):
        if entry["uuid"] == uuid and entry["timestamp"] == timestamp:
            return unlocks_responses.pop(i)
    return {"error": "Response not found"}

@app.get("/history/financials")
async def get_financials_response(uuid: str = Query(...), timestamp: int = Query(...)):
    for i, entry in enumerate(financials_responses):
        if entry["uuid"] == uuid and entry["timestamp"] == timestamp:
            return financials_responses.pop(i)
    return {"error": "Response not found"}

# ---- Launch agent + FastAPI together ----

if __name__ == "__main__":
    import uvicorn
    import threading
    import asyncio
    import os

    os.environ["UAGENTS_PORT"] = "8000"

    threading.Thread(target=lambda: asyncio.run(coordinator.run_async()), daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=8085)
