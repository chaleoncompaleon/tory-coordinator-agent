# Tory Coordinator Agent & FastAPI Gateway

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3) ![tag:finance](https://img.shields.io/badge/finance-202537) ![tag:tory](https://img.shields.io/badge/TORY-0827a3)

The **Tory Coordinator Agent** is the central hub that manages communication between a frontend app and three specialized uAgents:

- Tokenomics Analyst Agent
- Token Unlock Analyst Agent
- Financial Statement Analyst Agent

The Coordinator listens for incoming data, forwards them to the appropriate agents, stores their responses, and exposes a FastAPI gateway to interact with external systems.

---

## Features
- ✅ Validates deployed agents via Agentverse on startup
- 📩 Queues and sends tokenomics, unlocks, and financials requests to designated agents
- 📤 Receives AI-generated insights as agent responses
- 🧠 Exposes FastAPI endpoints to send requests and poll for results

---

## How It Works
1. The FastAPI backend receives a POST request with a payload: `uuid`, `timestamp`, `token` data.
2. The payload is queued and processed by the coordinator.
3. The coordinator sends it to the corresponding agent via `ctx.send(...)`.
4. The agent processes the input using an external AI API and replies.
5. The coordinator stores the response in memory.
6. The frontend/client can GET the result using the same `uuid` and `timestamp`.

---

## 🛠 How To Run Locally

1. Clone the repo
```bash
git clone https://github.com/chaleoncompaleon/tory-coordinator-agent
cd tory-coordinator-agent
```


2. Install dependencies
We recommend using a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```


3. Run the coordinator + FastAPI
This will:
- Start the coordinator agent
- Validate deployed agent metadata
- Launch the FastAPI server on http://localhost:8085

```bash
python tory_main_apis.py
```

---

## FastAPI Endpoints

### 1. Tokenomics
#### POST `/send/tokenomics`
Queue a tokenomics analysis request.
```bash
curl -X POST http://localhost:8085/send/tokenomics \
  -H "Content-Type: application/json" \
  -d '{
    "uuid": "123e4567-e89b-12d3-a456-426614174000",
    "timestamp": 1712428800,
    "token": "<tokenomics-json-data>"
  }'
```

#### GET `/history/tokenomics`
Retrieve the latest tokenomics result.
```bash
curl "http://localhost:8085/history/tokenomics?uuid=123e4567-e89b-12d3-a456-426614174000&timestamp=1712428800"
```

---

### 2. Unlocks
#### POST `/send/unlocks`
Queue an unlocks analysis request.
```bash
curl -X POST http://localhost:8085/send/unlocks \
  -H "Content-Type: application/json" \
  -d '{
    "uuid": "123e4567-e89b-12d3-a456-426614174000",
    "timestamp": 1712428800,
    "token": "<unlock-history-json>"
  }'
```

#### GET `/history/unlocks`
Retrieve the latest unlocks result.
```bash
curl "http://localhost:8085/history/unlocks?uuid=123e4567-e89b-12d3-a456-426614174000&timestamp=1712428800"
```

---

### 3. Financials
#### POST `/send/financials`
Queue a financials analysis request.
```bash
curl -X POST http://localhost:8085/send/financials \
  -H "Content-Type: application/json" \
  -d '{
    "uuid": "123e4567-e89b-12d3-a456-426614174000",
    "timestamp": 1712428800,
    "token": "<financial-metrics-json-array>"
  }'
```

#### GET `/history/financials`
Retrieve the latest financials result.
```bash
curl "http://localhost:8085/history/financials?uuid=123e4567-e89b-12d3-a456-426614174000&timestamp=1712428800"
```

---

## Requirements
```
uagents
fastapi
requests
uvicorn
```

---

## License
MIT

