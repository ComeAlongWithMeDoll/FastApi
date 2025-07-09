from fastapi import  WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.activate_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.activate_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.activate_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.activate_connections:
            await connection.send_text(message)