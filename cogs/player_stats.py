import discord
from discord.ext import commands
from controllers.player_stats import get_player_stats
import settings

cogs_logger = settings.logging.getLogger("cogs")

async def setup(bot: commands.Bot):
    await bot.add_cog(PlayerStats(bot=bot))

class PlayerStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def player_stats(self, ctx: commands.Context, username: str):
        """ View a player's statistics """
        await ctx.defer()
        try:
            d = await get_player_stats(username)
            e = discord.Embed(title=f"📊 {username}'s Stats", color=0x3498db)
            e.add_field(name="⏱ Playtime",        value=d["playtime"],     inline=True)
            e.add_field(name="💀 Deaths",          value=d["deaths"],       inline=True)
            e.add_field(name="⚔ Player Kills",    value=d["player_kills"], inline=True)
            e.add_field(name="🗡 Mob Kills",       value=d["mob_kills"],    inline=True)
            e.add_field(name="👑 Most Killed Mob", value=d["top_mob"],      inline=True)
            e.add_field(name="🗺 Distance Traveled",value=d["distance_km"], inline=True)
            e.add_field(name="⛏ Most Mined",      value=d["top_mined"],    inline=False)
            e.add_field(name="🔨 Most Crafted",    value=d["top_crafted"],  inline=False)
            e.set_footer(text="When Yah S2")
            await ctx.send(embed=e)
        except ValueError as ve:
            await ctx.send(f"❌ {ve}", ephemeral=True)
        except FileNotFoundError:
            await ctx.send(f"❌ No stats found for `{username}` — they may never have joined.", ephemeral=True)
        except Exception as ex:
            cogs_logger.error(f"player_stats error: {ex}")
            await ctx.send("❌ Failed to fetch stats.", ephemeral=True)