# from mcstatus import JavaServer
# import settings

# server = JavaServer.lookup(f"{settings.SERVER_HOST}:{settings.SERVER_PORT}")

# query = server.query()
# print(f"The server has the following players online: {', '.join(query.players.list)}")

# # import settings
# # from rcon.source import Client


# # print(settings.SERVER_HOST)
# # print(settings.SERVER_PORT)
# # print(settings.RCON_PASSWORD)
# # print(settings.RCON_PORT)

# # with Client(settings.SERVER_HOST, int(settings.RCON_PORT), passwd=settings.RCON_PASSWORD) as client:
# #     response = client.run('say', 'test')

# # print(response)
# import settings

# print(f"{settings.SERVER_HOST}:{settings.SERVER_PORT}")

# from mcstatus import JavaServer
# import settings

# def _get_server():
#     host = settings.SERVER_HOST
#     port = settings.SERVER_PORT
#     # Try SRV lookup first (no port), fall back to explicit port
#     try:
#         return JavaServer.lookup(host)
#     except:
#         return JavaServer.lookup(f"{host}:{port}")

# def get_server_status():
#     try:
#         server = _get_server()
#         status = server.status()
#         return f"🟢 Online — {status.players.online}/{status.players.max} players | {round(status.latency)}ms"
#     except Exception as e:
#         return f"🔴 Server unreachable: {e}"

# def get_online_players():
#     try:
#         server = _get_server()
#         query = server.query()
#         players = ", ".join(query.players.list) if query.players.list else "No players online"
#         return f"Online players ({query.players.online}): {players}"
#     except Exception as e:
#         return f"🔴 Could not fetch players: {e}"
    
# print(get_server_status())

from rcon.source import Client as RconClient
import settings

def get_server_status():
    try:
        with RconClient(settings.SERVER_HOST, int(settings.RCON_PORT), passwd=settings.RCON_PASSWORD) as rcon:
            response = rcon.run("list")
        return f"🟢 Online — {response}"
    except Exception as e:
        return f"🔴 Server unreachable: {e}"

def get_online_players():
    try:
        with RconClient(settings.SERVER_HOST, int(settings.RCON_PORT), passwd=settings.RCON_PASSWORD) as rcon:
            response = rcon.run("list")
        return f"📋 {response}"
    except Exception as e:
        return f"🔴 Could not fetch players: {e}"
    
print(get_online_players())