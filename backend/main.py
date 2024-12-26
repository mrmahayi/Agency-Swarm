from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active WebSocket connections
active_connections: List[WebSocket] = []

# Mock agents data
agents = [
    {
        "name": "TaskOrchestrator",
        "status": "idle",
        "lastAction": "Ready"
    },
    {
        "name": "Researcher",
        "status": "idle",
        "lastAction": "Ready"
    },
    {
        "name": "Analyst",
        "status": "idle",
        "lastAction": "Ready"
    }
]

@app.get("/")
async def read_root():
    return {"message": "Agency Swarm Backend"}

@app.get("/agents")
async def get_agents():
    return agents

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Process the command
            response = process_command(data)
            # Broadcast status updates and results
            for connection in active_connections:
                await connection.send_json({
                    "type": "command_result",
                    "data": response
                })
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        active_connections.remove(websocket)

def process_command(command: str) -> Dict:
    # Mock command processing
    if command.lower().startswith("analyze"):
        return {
            "type": "text",
            "content": f"Analysis results for command: {command}"
        }
    else:
        return {
            "type": "text",
            "content": f"Processed command: {command}"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 