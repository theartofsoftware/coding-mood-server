import asyncio


class WebsocketManager:
    def __init__(self):
        self.live_sockets = {}

    def register(self, websocket):
        websocket_id = id(websocket)
        self.live_sockets[websocket_id] = websocket

    def unregister(self, websocket):
        websocket_id = id(websocket)
        del self.live_sockets[websocket_id]

    async def broadcast(self, message):
        if self.live_sockets:
            await asyncio.wait([
                websocket.send_json(message)
                for websocket in self.live_sockets.values()
            ])
