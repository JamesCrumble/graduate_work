from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        try:
            del self.active_connections[user_id]
        except KeyError:
            pass

    async def send_personal_message(self, message: str, user_id: str):
        try:
            websocket = self.active_connections[user_id]
            await websocket.send_text(message)
        except KeyError:
            pass

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)


manager = ConnectionManager()
