from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
from src.WsManager import WsManager
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
manager = WsManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 特定のオリジンを許可する場合はここで指定します
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def get():
    return HTMLResponse("Hello Render")

@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message: {data}") 
            await manager.broadcast(f'{data}')
    except WebSocketDisconnect:
        manager.disconnect(websocket)
