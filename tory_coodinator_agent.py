from uagents import Agent, Context, Model
from typing import List, Dict
import asyncio
import requests

coordinator = Agent(
    name="coordinator_agent", 
    endpoint=["http://tory-coordinator-agent.up.railway.app:8090"],
    port=8090,
    mailbox=True
)

# Request models
class TokenomicsRequest(Model):
    uuid: str
    timestamp: int
    token: str

class UnlocksRequest(Model):
    uuid: str
    timestamp: int
    token: str

class FinancialsRequest(Model):
    uuid: str
    timestamp: int
    token: str

# Response models
class TokenomicsResponse(Model):
    uuid: str
    timestamp: int
    summary: str

class UnlocksResponse(Model):
    uuid: str
    timestamp: int
    summary: str

class FinancialsResponse(Model):
    uuid: str
    timestamp: int
    summary: str

# Structures to store responses
tokenomics_responses: List[Dict] = []
unlocks_responses: List[Dict] = []
financials_responses: List[Dict] = []

# Placeholder queues for sending messages
send_tokenomics_queue = asyncio.Queue()
send_unlocks_queue = asyncio.Queue()
send_financials_queue = asyncio.Queue()

# Agent addresses and names
TOKENOMICS_AGENT = "agent1qfanj06fl5awl2sg9wge4hfd26xg943r7p0jfh5d0q5lqcv2n2gcjkrewhj"
UNLOCKS_AGENT = "agent1qtvga6uw2uu0q4rylpcnvmde04mzt0e8v4p4szq4ghegu8h970xkk33d2hv"
FINANCIALS_AGENT = "agent1qvndjuj0rkxwllp060prw5scn2aq38zfcqkfp43u7n5alkx9u4zmqyxregu"

TOKENOMICS_AGENT_NAME = "TORY - Tokenomics Analyst Agent"
UNLOCKS_AGENT_NAME = "TORY - Token Unlock Analyst Agent"
FINANCIALS_AGENT_NAME = "TORY - Finance Statement Analyst Agent"

TOKENOMICS_AGENT_CREATED_AT = "2025-04-03T11:44:24Z"
UNLOCKS_AGENT_CREATED_AT = "2025-04-03T10:33:15Z"
FINANCIALS_AGENT_CREATED_AT = "2025-04-06T16:33:30Z"

def check_agent_validity(adr: str, name:str, date:str, agent:any):
    return adr == agent["address"] and name == agent["name"] and date == agent["created_at"]

# Startup event
@coordinator.on_event("startup")
async def startup(ctx: Context):
    global TOKENOMICS_AGENT, UNLOCKS_AGENT, FINANCIALS_AGENT
    ctx.logger.info("Coordinator Agent started and ready to receive requests.")

    # Agent search logic
    ctx.logger.info("🔎 Validating agent addresses via Agentverse API...")
    try:
        payload = {
            "search_text": "tag:TORY TORY",
            "sort": "relevancy",
            "direction": "asc",
            "offset": 0,
            "limit": 10
        }
        response = requests.post("https://agentverse.ai/v1/search/agents", json=payload)
        if response.status_code == 200:
            agents = response.json().get("agents", [])
            for agent in agents:
                ctx.logger.info(f"🔍 Found: {agent['name']} → {agent['address']} → {agent['created_at']}")
                if check_agent_validity(TOKENOMICS_AGENT, TOKENOMICS_AGENT_NAME, TOKENOMICS_AGENT_CREATED_AT, agent):
                    ctx.logger.info("✅ Tokenomic Agent Up & Running")
                elif check_agent_validity(UNLOCKS_AGENT, UNLOCKS_AGENT_NAME, UNLOCKS_AGENT_CREATED_AT, agent):
                    ctx.logger.info("✅ Unlocks Agent Up & Running")
                elif check_agent_validity(FINANCIALS_AGENT, FINANCIALS_AGENT_NAME, FINANCIALS_AGENT_CREATED_AT, agent):
                    ctx.logger.info("✅ Finance Agent Up & Running")                    
        else:
            ctx.logger.error("❌ Failed to fetch agent list from Agentverse.")
    except Exception as e:
        ctx.logger.error(f"⚠️ Agentverse search error: {e}")

# Tokenomics response handler
@coordinator.on_message(model=TokenomicsResponse)
async def handle_tokenomics_response(ctx: Context, sender: str, msg: TokenomicsResponse):
    ctx.logger.info(f"✅ Received Tokenomics response from {sender}: {msg.summary}")
    tokenomics_responses.append({
        "timestamp": msg.timestamp,
        "uuid": msg.uuid,
        "response": msg.summary
    })

# Unlocks response handler
@coordinator.on_message(model=UnlocksResponse)
async def handle_unlocks_response(ctx: Context, sender: str, msg: UnlocksResponse):
    ctx.logger.info(f"✅ Received Unlocks response from {sender}: {msg.summary}")
    unlocks_responses.append({
        "timestamp": msg.timestamp,
        "uuid": msg.uuid,
        "response": msg.summary
    })

# Financials response handler
@coordinator.on_message(model=FinancialsResponse)
async def handle_financials_response(ctx: Context, sender: str, msg: FinancialsResponse):
    ctx.logger.info(f"✅ Received Financials response from {sender}: {msg.summary}")
    financials_responses.append({
        "timestamp": msg.timestamp,
        "uuid": msg.uuid,
        "response": msg.summary
    })

# Polling interval handlers
@coordinator.on_interval(period=0.5)
async def poll_tokenomics(ctx: Context):
    if not send_tokenomics_queue.empty():
        item = await send_tokenomics_queue.get()
        ctx.logger.info(f"📤 Sending tokenomics request: {item}")
        await ctx.send(TOKENOMICS_AGENT, TokenomicsRequest(**item))

@coordinator.on_interval(period=0.5)
async def poll_unlocks(ctx: Context):
    if not send_unlocks_queue.empty():
        item = await send_unlocks_queue.get()
        ctx.logger.info(f"📤 Sending unlocks request: {item}")
        await ctx.send(UNLOCKS_AGENT, UnlocksRequest(**item))

@coordinator.on_interval(period=0.5)
async def poll_financials(ctx: Context):
    if not send_financials_queue.empty():
        item = await send_financials_queue.get()
        ctx.logger.info(f"📤 Sending financials request: {item}")
        await ctx.send(FINANCIALS_AGENT, FinancialsRequest(**item))
