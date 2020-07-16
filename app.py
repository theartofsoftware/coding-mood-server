from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.websockets import WebSocketDisconnect
import uvicorn


def create_app():
    app = Starlette()
    LIVE_SOCKETS = {}

    def register_websocket(websocket):
        websocket_id = id(websocket)
        LIVE_SOCKETS[websocket_id] = websocket

    def unregister_websocket(websocket):
        websocket_id = id(websocket)
        del LIVE_SOCKETS[websocket_id]

    @app.route('/')
    async def homepage(request):
        for websocket in LIVE_SOCKETS.values():
            await websocket.send_json({"code_state": "working"})
        return JSONResponse({"code_state": "working"})

    @app.websocket_route('/ws')
    async def websocket_endpoint(websocket):
        await websocket.accept()
        print("websocket opened")
        register_websocket(websocket)
        try:
            while True:
                mesg = await websocket.receive_text()
                print("Received message", mesg)
        except WebSocketDisconnect:
            print("Websocket disconnected")
        finally:
            unregister_websocket(websocket)
            await websocket.close()
            print("websocket closed")

    return app


if __name__ == '__main__':
    uvicorn.run(create_app(), host='0.0.0.0', port=5000)
