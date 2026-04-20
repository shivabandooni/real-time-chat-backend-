from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

# ✅ Test route (browser me check karne ke liye)
@app.get("/")
def read_root():
    return {"message": "Server is working"}

# ✅ Active users
active_connections = {}

# ✅ WebSocket chat
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    active_connections[user_id] = websocket
    print(f"{user_id} connected")

    try:
        while True:
            data = await websocket.receive_json()

            receiver = data.get("to")
            message = data.get("message")

            msg = {
                "from": user_id,
                "to": receiver,
                "message": message
            }

            if receiver in active_connections:
                await active_connections[receiver].send_json(msg)

            await websocket.send_json(msg)

    except WebSocketDisconnect:
        print(f"{user_id} disconnected")
        del active_connections[user_id]