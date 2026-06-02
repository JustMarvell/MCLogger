from discord.ext import commands
import controllers.server_status as server_status

async def setup(bot : commands.Bot):
    await bot.add_cog(ServerStatus(bot=bot))

class ServerStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command()
    async def server_status(self, ctx: commands.Context):
        """ Show current server status """
        
        status = await server_status.get_server_status()
        
        await ctx.send(status)