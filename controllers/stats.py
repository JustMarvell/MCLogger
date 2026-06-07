import settings
from discord.ext import commands
import re, os
from mcrcon import MCRcon

def get_rcon():
    return MCRcon(host=settings.SERVER_HOST, password=settings.RCON_PASSWORD, port=int(settings.RCON_PORT))

def parse_spark(raw):
    def find(pattern, text, g=1):
        m = re.search(pattern, text)
        return m.group(g) if m else "N/A"

    return {
        "tps": find(r"10s, 1m, 5m, 15m:\s+[\d.]+, \*([\d.]+)", raw),
        "cpu_sys": find(r"([\d]+)%.*\(system\)", raw),
        "cpu_proc": find(r"([\d]+)%.*\(process\)", raw),
        "mem_used": find(r"([\d.]+ GB) / [\d.]+ GB", raw),
        "mem_total": find(r"[\d.]+ GB / ([\d.]+ GB)", raw),
        "mem_pct": find(r"\(([\d]+)%\)", raw),
        "disk_used": find(r"([\d.]+ [KMGT]B) / [\d.]+ [KMGT]B\s+\([\d]+%\)", raw),
        "disk_total": find(r"[\d.]+ [KMGT]B / ([\d.]+ [KMGT]B)\s+\([\d]+%\)", raw),
        "disk_pct": find(r"[\d.]+ [KMGT]B / [\d.]+ [KMGT]B\s+\(([\d]+)%\)", raw),
    }