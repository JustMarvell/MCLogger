import asyncio
import asyncssh
import re
import settings

PATTERNS = {
    "chat":        re.compile(r"\[.*?\] \[Server thread/INFO\]: \[Not Secure\] <(\w+)> (.+)"),
    "join":        re.compile(r"\[.*?\] \[Server thread/INFO\]: (\w+) joined the game"),
    "leave":       re.compile(r"\[.*?\] \[Server thread/INFO\]: (\w+) left the game"),
    "death":       re.compile(r"\[.*?\] \[Server thread/INFO\]: (\w+) (was|died|fell|drowned|burned|hit|tried|walked|withered|starved|suffocated|blew|went|discovered|left|experienced)(.*)"),
    "achievement": re.compile(r"\[.*?\] \[Server thread/INFO\]: (\w+) has (made the advancement|completed the challenge|reached the goal) \[(.+)\]"),
}

def parse_line(line: str) -> dict | None:
    for event, pattern in PATTERNS.items():
        if m := pattern.search(line):
            return {"type": event, "match": m}
    return None

async def watch_log(callback, poll_interval: int = 5):
    last_size = 0

    async with asyncssh.connect(
        host=settings.SERVER_HOST,
        port=int(settings.SERVER_SFTP_PORT),
        username=settings.SERVER_SFTP_USER,
        password=settings.SERVER_SFTP_PASSWORD,
        known_hosts=None
    ) as conn:
        async with conn.start_sftp_client() as sftp:
            while True:
                try:
                    stat = await sftp.stat(settings.MC_LOG_PATH)
                    current_size = stat.size

                    if current_size < last_size:
                        last_size = 0  # log rotated/server restarted

                    if current_size > last_size:
                        async with sftp.open(settings.MC_LOG_PATH, 'r') as f:
                            await f.seek(last_size)
                            chunk = await f.read(current_size - last_size)
                            last_size = current_size

                            for line in chunk.splitlines():
                                result = parse_line(line.strip())
                                if result:
                                    await callback(result)

                except Exception as e:
                    raise e

                await asyncio.sleep(poll_interval)