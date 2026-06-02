from discord.ext import commands
from rcon.source import Client as RconClient
import settings

cogs_logger = settings.logging.getLogger("cogs")

async def setup (bot : commands.Bot):
    await bot.add_cog(SendCommand(bot=bot))

class SendCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def send_command(self, ctx: commands.Context, command: str):
        """ Send a command to the minecraft server """

        try: 
            with RconClient(settings.SERVER_HOST, int(settings.RCON_PORT), passwd=settings.RCON_PASSWORD) as rcon:
                rcon.run(f"{command}")
            
            await ctx.send("Command sent", ephemeral=True)
        except Exception as e:
            cogs_logger.error(f"RCON ERROR: {e}")
            await ctx.send("Failed to send command", ephemeral=True)
        
    @send_command.error
    async def send_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command")