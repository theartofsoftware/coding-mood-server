import pytest
from mock import AsyncMock
from codingmoodserver.websocket_manager import WebsocketManager


@pytest.mark.asyncio
async def test_broadcast():
    websocket_mgr = WebsocketManager()
    mock_sock = AsyncMock()
    mock_sock_2 = AsyncMock()
    websocket_mgr.register(mock_sock)
    websocket_mgr.register(mock_sock_2)
    await websocket_mgr.broadcast({"test": "message"})

    mock_sock.send_json.assert_called_with({"test": "message"})
    mock_sock_2.send_json.assert_called_with({"test": "message"})


@pytest.mark.asyncio
async def test_unregister_websockets():
    websocket_mgr = WebsocketManager()
    mock_sock = AsyncMock()
    mock_sock_2 = AsyncMock()
    websocket_mgr.register(mock_sock)
    websocket_mgr.register(mock_sock_2)
    websocket_mgr.unregister(mock_sock_2)
    await websocket_mgr.broadcast({"test": "message"})

    mock_sock.send_json.assert_called_with({"test": "message"})
    mock_sock_2.send_json.assert_not_called()
