from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import os

app = FastAPI()

clients = {}

@app.get("/")
async def root():
    return {
        "name": "SecureComm Signaling Server",
        "status": "running"
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    client_id = None

    try:
        while True:
            message = await websocket.receive_text()

            if client_id is None:
                client_id = message
                clients[client_id] = websocket
                continue

            if ":" in message:
                target, data = message.split(":", 1)

                if target in clients:
                    await clients[target].send_text(data)

    except WebSocketDisconnect:
        pass

    finally:
        if client_id in clients:
            del clients[client_id]
