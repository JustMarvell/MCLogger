from mcstatus import JavaServer
import settings

server = JavaServer.lookup(f"{settings.SERVER_HOST}:{settings.SERVER_PORT}")

query = server.query()
print(f"The server has the following players online: {', '.join(query.players.list)}")

# import settings
# from rcon.source import Client


# print(settings.SERVER_HOST)
# print(settings.SERVER_PORT)
# print(settings.RCON_PASSWORD)
# print(settings.RCON_PORT)

# with Client(settings.SERVER_HOST, int(settings.RCON_PORT), passwd=settings.RCON_PASSWORD) as client:
#     response = client.run('say', 'test')

# print(response)
import settings

# print(f"{settings.SERVER_HOST}:{settings.SERVER_PORT}")