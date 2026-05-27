import asyncio

from portprimer.playground import PLAYGROUND_HOST, PlaygroundService, start_playground_service


def test_playground_service_binds_only_to_localhost():
    async def run_check():
        server = await start_playground_service(PlaygroundService(0, "test door", "test teaching service"))
        try:
            sockets = server.sockets or []
            assert sockets
            assert {socket.getsockname()[0] for socket in sockets} == {PLAYGROUND_HOST}
        finally:
            server.close()
            await server.wait_closed()

    asyncio.run(run_check())


def test_playground_service_sends_plain_text_message():
    async def run_check():
        server = await start_playground_service(PlaygroundService(0, "test door", "test teaching service"))
        try:
            port = (server.sockets or [])[0].getsockname()[1]
            reader, writer = await asyncio.open_connection(PLAYGROUND_HOST, port)
            data = await reader.read(200)
            writer.close()
            await writer.wait_closed()
        finally:
            server.close()
            await server.wait_closed()
        text = data.decode("utf-8")
        assert "test teaching service" in text
        assert "not a real SSH" in text
        assert "127.0.0.1" in text

    asyncio.run(run_check())
