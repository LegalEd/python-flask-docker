import pytest
import websockets


@pytest.mark.asyncio
async def test_websocket():
    async with websockets.connect('ws://localhost:8080/nostr') as websocket:
        data = 'hi'
        await websocket.send(data)
        res = await websocket.recv()
        assert res == "error Expecting value: line 1 column 1 (char 0)"


@pytest.mark.asyncio
async def test_websocket_json():
    async with websockets.connect('ws://localhost:8080/nostr') as websocket:
        data = '{}'
        await websocket.send(data)
        res = await websocket.recv()
        assert res.startswith("error 'id' is a required property")


@pytest.mark.asyncio
async def test_websocket_real():
    async with websockets.connect('ws://localhost:8080/nostr') as websocket:
        data = """{"id": "alanaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "pubkey": "alanaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                    "created_at": 1234567890,
                    "kind": 1,
                    "tags": [],
                    "content": "This is the first message",
                    "sig": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}"""
        await websocket.send(data)
        res = await websocket.recv()
        assert res == "Saving message"


@pytest.mark.asyncio
async def test_websocket_ban():
    async with websockets.connect('ws://localhost:8080/nostr') as websocket:
        data2 = """{"id": "banaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1", "pubkey": "banaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1",
            "created_at": 1234567890,
            "kind": 1,
            "tags": [],
            "content": "This is the second message",
            "sig": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}"""
        await websocket.send(data2)
        res2 = await websocket.recv()
        assert res2 == "Saving message"


@pytest.mark.asyncio
async def test_websocket_tom():
    async with websockets.connect('ws://localhost:8080/nostr') as websocket:
        data3 = """{"id": "tomaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1", "pubkey": "tomaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1",
            "created_at": 1234567890,
            "kind": 2,
            "tags": [],
            "content": "",
            "sig": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}"""
        await websocket.send(data3)
        res3 = await websocket.recv()
        assert res3 == "{'id': 'alanaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'pubkey': 'alanaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'created_at': 1234567890, 'kind': 1, 'tags': [], 'content': 'This is the first message', 'sig': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'}"
        res4 = await websocket.recv()
        assert res4 == "{'id': 'banaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1', 'pubkey': 'banaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1', 'created_at': 1234567890, 'kind': 1, 'tags': [], 'content': 'This is the second message', 'sig': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'}"
