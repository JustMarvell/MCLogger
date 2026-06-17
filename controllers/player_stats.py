import asyncssh
import aiohttp
import json
import settings
from pathlib import PurePosixPath
import hashlib, uuid

def _offline_uuid(username: str) -> str:
    h = bytearray(hashlib.md5(f"OfflinePlayer:{username}".encode("utf-8")).digest())
    h[6] = (h[6] & 0x0F) | 0x30
    h[8] = (h[8] & 0x3F) | 0x80
    u = uuid.UUID(bytes=bytes(h))
    return str(u)

def _stats_path(uuid: str) -> str:
    base = PurePosixPath(settings.MC_LOG_PATH).parent.parent
    return str(base / "world" / "stats" / f"{uuid}.json")

def _fmt_time(ticks: int) -> str:
    seconds = ticks // 20
    h, m = divmod(seconds // 60, 60)
    s = seconds % 60
    return f"{h}h {m}m {s}s"

def _fmt_block(key: str) -> str:
    return key.replace("minecraft:", "").replace("_", " ").title()

def _parse(data: dict) -> dict:
    stats = data.get("stats", {})
    custom = stats.get("minecraft:custom", {})
    killed = stats.get("minecraft:killed", {})
    mined  = stats.get("minecraft:mined", {})
    crafted = stats.get("minecraft:crafted", {})

    dist_keys = [v for k, v in custom.items() if k.endswith("_one_cm")]
    total_dist_m = sum(dist_keys) / 100

    top_mob     = max(killed, key=killed.get)  if killed  else None
    top_mined   = max(mined,  key=mined.get)   if mined   else None
    top_crafted = max(crafted, key=crafted.get) if crafted else None

    return {
        "playtime":       _fmt_time(custom.get("minecraft:play_time", 0)),
        "deaths":         custom.get("minecraft:deaths", 0),
        "player_kills":   custom.get("minecraft:player_kills", 0),
        "mob_kills":      sum(killed.values()),
        "top_mob":        f"{_fmt_block(top_mob)} ({killed[top_mob]})" if top_mob else "N/A",
        "distance_km":    f"{total_dist_m / 1000:.2f} km",
        "top_mined":      f"{_fmt_block(top_mined)} ({mined[top_mined]})" if top_mined else "N/A",
        "top_crafted":    f"{_fmt_block(top_crafted)} ({crafted[top_crafted]})" if top_crafted else "N/A",
    }

async def get_player_stats(username: str) -> dict:
    uuid_str = None
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.mojang.com/users/profiles/minecraft/{username}") as r:
            if r.status == 200:
                raw_id = (await r.json())["id"]
                uuid_str = f"{raw_id[:8]}-{raw_id[8:12]}-{raw_id[12:16]}-{raw_id[16:20]}-{raw_id[20:]}"

    if uuid_str is None:
        uuid_str = _offline_uuid(username)

    async with asyncssh.connect(
        host=settings.SERVER_HOST,
        port=int(settings.SERVER_SFTP_PORT),
        username=settings.SERVER_SFTP_USER,
        password=settings.SERVER_SFTP_PASSWORD,
        known_hosts=None
    ) as conn:
        async with conn.start_sftp_client() as sftp:
            async with sftp.open(_stats_path(uuid_str), "r") as f:
                raw = await f.read()

    return _parse(json.loads(raw))