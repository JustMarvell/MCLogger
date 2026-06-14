from discord.ext import commands
import controllers.ping as ping
import discord
import asyncio

async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot=bot))

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def ping(self, ctx: commands.Context):
        """ Ping the VPS and Minecraft server """
        await ctx.defer()
        vps, mc = await asyncio.gather(ping.ping_vps(), ping.ping_mc())

        e = discord.Embed(title="Network Ping", color=0x3498db)
        e.add_field(
            name="VPS",
            value=f"🟢 `{vps['latency']}ms`" if vps["online"] else "🔴 Unreachable",
            inline=True
        )
        e.add_field(
            name="MC Server (Laptop)",
            value=f"🟢 `{mc['latency']}ms`" if mc["online"] else "🔴 Unreachable",
            inline=True
        )
        await ctx.send(embed=e)