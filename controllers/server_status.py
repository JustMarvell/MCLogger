from mcstatus import JavaServer

server = JavaServer.lookup("whenyahs2.mcsh.io:25565")

async def get_server_status():
    status = server.status()
    
    return f"The server has {status.players.online} player(s) online and replied in {status.latency} ms"