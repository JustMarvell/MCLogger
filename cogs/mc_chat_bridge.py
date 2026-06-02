import discord
from discord.ext import commands
import controllers.mc_log_watcher as watcher
import settings
import asyncio

cogs_logger = settings.logging.getLogger("cogs")

EMOJIS = {"chat": "💬", "join": "✅", "leave": "🚪", "death": "💀", "achievement": "🏆"}

async def setup(bot: commands.Bot):
    await bot.add_cog(MCChatBridge(bot=bot))

class MCChatBridge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel = None
        self.watch_task = None
        if self.bot.is_ready():
            asyncio.ensure_future(self._init_watcher())

    def cog_unload(self):
        if self.watch_task:
            self.watch_task.cancel()
            self.watch_task = None

    @commands.Cog.listener()
    async def on_ready(self):
        await self._init_watcher()

    async def _init_watcher(self):
        if self.watch_task and not self.watch_task.done():
            return
        self.channel = self.bot.get_channel(int(settings.DISCORD_CHANNEL_ID))
        if self.channel:
            self.watch_task = self.bot.loop.create_task(self._start_watcher())
            cogs_logger.info("MC log watcher started")
        else:
            cogs_logger.error("MC bridge channel not found")
            
    async def _start_watcher(self):
        while True:
            try:
                await watcher.watch_log(self._handle_event)
            except Exception as e:
                cogs_logger.error(f"Log watcher error: {e}, retrying in 10s...")
                await asyncio.sleep(10)

    async def _handle_event(self, event: dict):
        m = event["match"]
        t = event["type"]
        emoji = EMOJIS.get(t, "📋")

        match t:
            case "chat":
                embed = discord.Embed(color=2533376, title="`` Minecraft Chat ``:speech_balloon: ",)
                embed.add_field(
                    name=f"``<{m.group(1)}> :  {m.group(2)}``",
                    value=" ",
                    inline=False,
                )
            case "join":
                embed = discord.Embed(color=16185345, title="`` Joined the Server``:door: ",)
                embed.add_field(
                    name=f"``{m.group(1)} joined the game``",
                    value=" ",
                    inline=False,
                )
            case "leave":
                embed = discord.Embed(color=16185345, title="`` Left the Server``:door: ",)
                embed.add_field(
                    name=f"``{m.group(1)} left the game``",
                    value=" ",
                    inline=False,
                )
            case "death":
                embed = discord.Embed(color=16056834, title="`` Died``:skull: ",)
                embed.add_field(
                    name=f"``{m.group(1)} {m.group(2)}{m.group(3)}``",
                    value=" ",
                    inline=False,
                )
            case "achievement":
                embed = discord.Embed(color=16297217, title="`` Achievement``:trophy: ",)
                embed.add_field(
                    name=f"``{m.group(1)} {m.group(2)} [{m.group(3)}]``",
                    value=" ",
                    inline=False,
                )
            case _: return

        await self.channel.send(embed=embed)