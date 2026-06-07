import discord
from discord.ext import commands
from controllers import stats


async def setup(bot : commands.Bot):
    await bot.add_cog(Stats(bot=bot))
    
class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command()
    async def stats(self, ctx: commands.Context):
        """ Shows the Current Server Stats """
        await ctx.typing()
        try:
            with stats.get_rcon() as r:
                raw = r.command("spark health")
                await ctx.send(f"```{raw}```")

            d = stats.parse_spark(raw)
            e = discord.Embed(title="⚡ Server Stats", color=0x2ecc71)
            e.add_field(name="TPS", value=f"**{d['tps']}** / 20.0", inline=False)
            e.add_field(name="CPU", value=f"System: **{d['cpu_sys']}%** | Process: **{d['cpu_proc']}%**", inline=False)
            e.add_field(name="Memory", value=f"**{d['mem_used']} / {d['mem_total']}** ({d['mem_pct']}%)", inline=True)
            e.add_field(name="Disk", value=f"**{d['disk_used']} / {d['disk_total']}** ({d['disk_pct']}%)", inline=True)
            await ctx.send(embed=e)
        except Exception as ex:
            await ctx.send(f"❌ `{ex}`")