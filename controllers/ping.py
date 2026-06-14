import asyncio
import time
import settings

async def ping_vps() -> dict:
    proc = await asyncio.create_subprocess_exec(
        "ping", "-c", "1", "-W", "2", settings.SERVER_HOST,
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    out, _ = await proc.communicate()
    if proc.returncode == 0:
        import re
        m = re.search(r"time=([\d.]+)", out.decode())
        return {"online": True, "latency": float(m.group(1)) if m else None}
    return {"online": False, "latency": None}

async def ping_mc() -> dict:
    try:
        from rcon.source import Client as RconClient
        def _run():
            t = time.perf_counter()
            with RconClient(settings.SERVER_HOST, int(settings.RCON_PORT), passwd=settings.RCON_PASSWORD):
                pass
            return round((time.perf_counter() - t) * 1000, 2)
        latency = await asyncio.to_thread(_run)
        return {"online": True, "latency": latency}
    except Exception:
        return {"online": False, "latency": None}