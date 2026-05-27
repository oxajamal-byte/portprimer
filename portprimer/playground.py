from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator


PLAYGROUND_HOST = "127.0.0.1"


@dataclass(frozen=True)
class PlaygroundService:
    port: int
    name: str
    message: str


PLAYGROUND_SERVICES: tuple[PlaygroundService, ...] = (
    PlaygroundService(8022, "Admin Door", "PortPrimer Playground Tour: safe local Admin Door practice service."),
    PlaygroundService(8080, "Web Door", "PortPrimer Playground Tour: safe local Web Door practice service."),
    PlaygroundService(15432, "Data Door", "PortPrimer Playground Tour: safe local Data Door practice service."),
    PlaygroundService(16379, "Data Door", "PortPrimer Playground Tour: safe local Cache Door practice service."),
    PlaygroundService(18080, "Web Door", "PortPrimer Playground Tour: safe local Web Door practice service."),
)


def playground_ports() -> list[int]:
    return [service.port for service in PLAYGROUND_SERVICES]


async def _handle_teaching_connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, message: str) -> None:
    writer.write(
        f"{message}\n"
        "This is not a real SSH, database, web, cache, or vulnerable service.\n"
        "It binds only to 127.0.0.1 and exists so you can see how open ports appear in a scan.\n".encode("utf-8")
    )
    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def start_playground_service(service: PlaygroundService) -> asyncio.AbstractServer:
    async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        await _handle_teaching_connection(reader, writer, service.message)

    return await asyncio.start_server(handler, host=PLAYGROUND_HOST, port=service.port)


@asynccontextmanager
async def playground_services(services: tuple[PlaygroundService, ...] = PLAYGROUND_SERVICES) -> AsyncIterator[list[asyncio.AbstractServer]]:
    servers: list[asyncio.AbstractServer] = []
    try:
        for service in services:
            servers.append(await start_playground_service(service))
        yield servers
    finally:
        for server in servers:
            server.close()
        await asyncio.gather(*(server.wait_closed() for server in servers))
