import asyncio
import time
import settings

async def _tcp_ping(host: str, port: int) -> dict:
    try:
        t = time.perf_counter()
        _, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=3)
        latency = round((time.perf_counter() - t) * 1000, 2)
        writer.close()
        await writer.wait_closed()
        return {"online": True, "latency": latency}
    except Exception:
        return {"online": False, "latency": None}

async def ping_vps() -> dict:
    return await _tcp_ping(settings.SERVER_HOST, 22)

async def ping_mc() -> dict:
    return await _tcp_ping(settings.SERVER_HOST, int(settings.RCON_PORT))