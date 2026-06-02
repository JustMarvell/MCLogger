from discord.ext import commands
from rcon.source import Client as RconClient
import settings

cogs_logger = settings.logging.getLogger("cogs")

async def setup(bot : commands.Bot):
    await bot.add_cog(SendToMC(bot=bot))

class SendToMC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command()
    async def send_message(self, ctx: commands.Context, message: str):
        """ Send a Message To the minecraft server """

        try:
            with RconClient(settings.SERVER_HOST, int(settings.RCON_PORT), passwd=settings.RCON_PASSWORD) as DiscordClient:
                DiscordClient.run(f"say [Discord] {ctx.message.author.display_name} : {message}")
            
            await ctx.send("Message sent", ephemeral=True)
        except Exception as e:
            cogs_logger.error(f"RCON ERROR: {e}")
            await ctx.send("Message Failed to send", ephemeral=True)