import re
import logging

from starlette.websockets import WebSocketDisconnect

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


class CodingMoodService:
    def __init__(self, websocket_mgr):
        self.last_num_of_failures = 9
        self.last_state = WORKING_STATE
        self.websocket_mgr = websocket_mgr

    async def set_new_state(self, test_run_output):
        num_of_failures = extract_number_of_failures(test_run_output)
        new_state = get_new_state(self.last_num_of_failures, num_of_failures)

        if new_state and self.last_state != new_state:
            LOGGER.info("Broadcasting new state: %s", new_state)
            await self.websocket_mgr.broadcast(new_state)

        self.last_num_of_failures = num_of_failures
        self.last_state = new_state

    async def handle_websocket(self, websocket):
        await websocket.accept()
        LOGGER.info("websocket opened")
        self.websocket_mgr.register(websocket)
        try:
            while True:
                mesg = await websocket.receive_text()
                LOGGER.debug("Received message", mesg)
        except WebSocketDisconnect:
            LOGGER.info("Websocket disconnected")
        finally:
            self.websocket_mgr.unregister(websocket)
            await websocket.close()
            LOGGER.info("websocket closed")
