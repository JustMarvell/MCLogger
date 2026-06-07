import asyncssh
import settings
from rcon.source import Client as RconClient
import re
import asyncio

def _send_spark():
    with RconClient(settings.SERVER_HOST, int(settings.RCON_PORT), passwd=settings.RCON_PASSWORD) as rcon:
        rcon.run("spark health")

async def _read_log_tail(bytes=8192) -> str:
    async with asyncssh.connect(
        host=settings.SERVER_HOST,
        port=int(settings.SERVER_SFTP_PORT),
        username=settings.SERVER_SFTP_USER,
        password=settings.SERVER_SFTP_PASSWORD,
        known_hosts=None
    ) as conn:
        async with conn.start_sftp_client() as sftp:
            stat = await sftp.stat(settings.MC_LOG_PATH)
            offset = max(0, stat.size - bytes)
            async with sftp.open(settings.MC_LOG_PATH, 'r') as f:
                await f.seek(offset)
                return await f.read(stat.size - offset)

def find_last(pattern, text):
            matches = re.findall(pattern, text)
            return matches[-1] if matches else "N/A"

def _parse_spark(raw) -> dict:
    def find(pattern, text, g=1):
        m = re.search(pattern, text)
        return m.group(g) if m else "N/A"
    return {
        "tps":       find(r"5s, 10s, 1m, 5m, 15m:\s+[\d.*]+,\s+[\d.*]+,\s+\*?([\d.]+)", raw),
        "cpu_sys":   find(r"([\d]+)%,\s+[\d]+%,\s+[\d]+%\s+\(system\)", raw),
        "cpu_proc":  find(r"([\d]+)%,\s+[\d]+%,\s+[\d]+%\s+\(process\)", raw),
        "mem_used":  find(r"([\d.]+ GB) / [\d.]+ GB\s+\([\d]+%\)", raw),
        "mem_total": find(r"[\d.]+ GB / ([\d.]+ GB)\s+\([\d]+%\)", raw),
        "mem_pct":   find(r"[\d.]+ GB / [\d.]+ GB\s+\(([\d]+)%\)", raw),
        
        "disk_used":  find_last(r"([\d.]+ (?:[KMGT]B|TB)) / [\d.]+ (?:[KMGT]B|TB)\s+\([\d]+%\)", raw),
        "disk_total": find_last(r"[\d.]+ (?:[KMGT]B|TB) / ([\d.]+ (?:[KMGT]B|TB))\s+\([\d]+%\)", raw),
        "disk_pct":   find_last(r"[\d.]+ (?:[KMGT]B|TB) / [\d.]+ (?:[KMGT]B|TB)\s+\(([\d]+)%\)", raw),
    }

async def get_stats() -> dict:
    _send_spark()
    await asyncio.sleep(3)
    log = await _read_log_tail()
    return _parse_spark(log)