from rcon.source import Client as RconClient
import re
import settings
import asyncio

async def get_server_status() -> dict:
    try:
        def _run():
            with RconClient(settings.SERVER_HOST, int(settings.RCON_PORT), passwd=settings.RCON_PASSWORD) as rcon:
                return rcon.run("list")
        response = await asyncio.to_thread(_run)
        match = re.search(r"(\d+).*?(\d+)", response)
        current, max_ = (int(match.group(1)), int(match.group(2))) if match else (0, 0)
        return {"online": True, "current": current, "max": max_}
    except Exception:
        return {"online": False}

async def get_online_players() -> dict:
    try:
        def _run():
            with RconClient(settings.SERVER_HOST, int(settings.RCON_PORT), passwd=settings.RCON_PASSWORD) as rcon:
                return rcon.run("list")
        response = await asyncio.to_thread(_run)
        match = re.search(r"(\d+).*?(\d+) players online:?(.*)", response)
        players = [p.strip() for p in match.group(3).split(",") if p.strip()] if match else []
        return {"online": True, "count": len(players), "players": players}
    except Exception:
        return {"online": False, "count": 0, "players": []}