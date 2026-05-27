from __future__ import annotations

import asyncio
from dataclasses import dataclass


@dataclass(frozen=True)
class ScanResult:
    port: int
    status: str


async def scan_port(target: str, port: int, timeout: float, semaphore: asyncio.Semaphore) -> ScanResult:
    async with semaphore:
        try:
            _, writer = await asyncio.wait_for(asyncio.open_connection(target, port), timeout=timeout)
            writer.close()
            await writer.wait_closed()
            return ScanResult(port=port, status="open")
        except TimeoutError:
            return ScanResult(port=port, status="timeout")
        except OSError:
            return ScanResult(port=port, status="closed")


async def scan_ports(target: str, ports: list[int], timeout: float = 1.0, concurrency: int = 50) -> list[ScanResult]:
    if concurrency < 1 or concurrency > 50:
        raise ValueError("Concurrency must be between 1 and 50.")
    semaphore = asyncio.Semaphore(concurrency)
    tasks = [scan_port(target, port, timeout, semaphore) for port in ports]
    results = await asyncio.gather(*tasks)
    return sorted(results, key=lambda result: result.port)

