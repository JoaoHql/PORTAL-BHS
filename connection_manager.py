from typing import List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"Novo cliente conectado: {websocket.client}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"Cliente desconectado: {websocket.client}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
        print(f"Mensagem enviada para {websocket.client}: {message}")

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
        print(f"Broadcast de mensagem: {message}")