from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.websockets import WebSocketDisconnect
import uvicorn

from websocket_manager import WebsocketManager

WORKING_STATE = {"state": "working"}
BROKEN_STATE = {"state": "broken"}


def create_app():
    app = Starlette()
    websocket_mgr = WebsocketManager()

    @app.route('/')
    async def working_state(request):
        await websocket_mgr.broadcast(WORKING_STATE)
        return JSONResponse(WORKING_STATE)

    @app.route('/broken')
    async def broken_state(request):
        await websocket_mgr.broadcast(BROKEN_STATE)
        return JSONResponse(BROKEN_STATE)

    @app.websocket_route('/ws')
    async def websocket_endpoint(websocket):
        await websocket.accept()
        print("websocket opened")
        websocket_mgr.register(websocket)
        try:
            while True:
                mesg = await websocket.receive_text()
                print("Received message", mesg)
        except WebSocketDisconnect:
            print("Websocket disconnected")
        finally:
            websocket_mgr.unregister(websocket)
            await websocket.close()
            print("websocket closed")

    return app


if __name__ == '__main__':
    uvicorn.run(create_app(), host='0.0.0.0', port=5000)
