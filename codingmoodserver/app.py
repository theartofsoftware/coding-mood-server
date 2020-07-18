import re
import logging
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.websockets import WebSocketDisconnect
import uvicorn

from websocket_manager import WebsocketManager

LOGGER = logging.getLogger(__name__)

WORKING_STATE = {"state": "working"}
BROKEN_STATE = {"state": "broken"}
FIXING_STATE = {"state": "fixing"}


def extract_number_of_failures(test_run_output):
    num_of_failures = 0
    failures_match = re.search(r"(\d+) failed", test_run_output)
    if failures_match:
        num_of_failures = int(failures_match.group(1))
    return num_of_failures


def get_new_state(last_num_of_failures, num_of_failures):
    if num_of_failures == 0:
        return WORKING_STATE
    elif num_of_failures > last_num_of_failures:
        return BROKEN_STATE
    elif num_of_failures < last_num_of_failures:
        return FIXING_STATE
    return None


def create_app():
    app = Starlette()
    websocket_mgr = WebsocketManager()

    LAST_NUM_OF_FAILURES = 0
    LAST_STATE = None

    @app.route('/state', methods=("POST",))
    async def set_new_state(request):
        nonlocal LAST_NUM_OF_FAILURES
        nonlocal LAST_STATE

        raw_body = await request.body()
        data = raw_body.decode("utf-8")

        num_of_failures = extract_number_of_failures(data)
        new_state = get_new_state(LAST_NUM_OF_FAILURES, num_of_failures)

        if new_state and LAST_STATE != new_state:
            LOGGER.info("Broadcasting new state: %s", new_state)
            await websocket_mgr.broadcast(new_state)

        LAST_NUM_OF_FAILURES = num_of_failures
        LAST_STATE = new_state

        return JSONResponse({})

    @app.websocket_route('/ws')
    async def websocket_endpoint(websocket):
        await websocket.accept()
        LOGGER.info("websocket opened")
        websocket_mgr.register(websocket)
        try:
            while True:
                mesg = await websocket.receive_text()
                LOGGER.info("Received message", mesg)
        except WebSocketDisconnect:
            LOGGER.info("Websocket disconnected")
        finally:
            websocket_mgr.unregister(websocket)
            await websocket.close()
            LOGGER.info("websocket closed")

    return app


if __name__ == '__main__':
    uvicorn.run(create_app(), host='0.0.0.0', port=5000)
