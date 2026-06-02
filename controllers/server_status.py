from mcstatus import JavaServer
import settings

server = JavaServer.lookup(f"{settings.SERVER_HOST}:{settings.SERVER_PORT}")

async def get_server_status():
    status = server.status()
    
    return f"The server has {status.players.online} player(s) online and replied in {status.latency} ms"

async def get_online_players():
    query = server.query()
    
    return f"The server has the following player(s) online: {query.players.list}"