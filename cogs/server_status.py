from discord.ext import commands
import controllers.server_status as server_status
import discord

async def setup(bot : commands.Bot):
    await bot.add_cog(ServerStatus(bot=bot))

class ServerStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command()
    async def server_status(self, ctx: commands.Context):
        """ Show current server status """
        
        data = await server_status.get_server_status()
        embed = discord.Embed(title="Server Status", color=0x2ecc71 if data["online"] else 0xe74c3c)
        if data["online"]:
            embed.add_field(name="Status", value="🟢 Online", inline=True)
            embed.add_field(name="Players", value=f"{data['current']}/{data['max']}", inline=True)
        else:
            embed.add_field(name="Status", value="🔴 Offline", inline=True)
            embed.set_footer(text="When Yah S2")
        await ctx.send(embed=embed)
        
    @commands.hybrid_command()
    async def list_players(self, ctx: commands.Context):
        """ List available players """
        
        data = await server_status.get_online_players()
        embed = discord.Embed(title="Online Players", color=0x3498db)
        if data["online"]:
            players = "\n".join(f"• {p}" for p in data["players"]) if data["players"] else "No players online"
            embed.add_field(name=f"Players ({data['count']})", value=players, inline=False)
        else:
            embed.add_field(name="Status", value="🔴 Server unreachable", inline=False)
        embed.set_footer(text="When Yah S2")
        await ctx.send(embed=embed)