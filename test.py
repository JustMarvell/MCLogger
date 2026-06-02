from mcstatus import JavaServer

server = JavaServer.lookup("144.31.46.4:14740")

query = server.query()
print(f"The server has the following players online: {', '.join(query.players.list)}")