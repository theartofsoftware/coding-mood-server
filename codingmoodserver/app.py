import logging
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
import uvicorn

from websocket_manager import WebsocketManager
from coding_mood_service import CodingMoodService

LOGGER = logging.getLogger(__name__)


def create_app():
    app = Starlette()
    coding_mood_service = CodingMoodService(WebsocketManager())

    @app.route('/state', methods=("POST",))
    async def set_new_state(request):
        raw_body = await request.body()
        data = raw_body.decode("utf-8")
        await coding_mood_service.set_new_state(data)
        return HTMLResponse()

    @app.websocket_route('/ws')
    def websocket_endpoint(websocket):
        return coding_mood_service.handle_websocket(websocket)

    return app


if __name__ == '__main__':
    uvicorn.run(create_app(), host='0.0.0.0', port=5000)
