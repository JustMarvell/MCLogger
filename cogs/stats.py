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
            ssh = stats.get_ssh()
            
            cpu_model = stats.ssh_run(ssh, "grep -m1 'model name' /proc/cpuinfo | cut -d: -f2")
            cpu_cores = stats.ssh_run(ssh, "nproc")
            cpu_load = stats.ssh_run(ssh, "top -bn1 | grep 'Cpu(s)' | awk '{print $2+$4}'")
            
            ram_total = stats.ssh_run(ssh, "free -h | awk '/^Mem/{print $2}'")
            ram_used = stats.ssh_run(ssh, "free -h | awk '/^Mem/{print $3}'")
            ram_type = stats.ssh_run(ssh, "sudo dmidecode -t memory 2>/dev/null | grep -m1 'Type:' | awk '{print $2}'") or "N/A"
            ram_speed = stats.ssh_run(ssh, "sudo dmidecode -t memory 2>/dev/null | grep -m1 'Speed:' | awk '{print $2,$3}'") or "N/A"

            disk_total = stats.ssh_run(ssh, "df -h / | awk 'NR==2{print $2}'")
            disk_used = stats.ssh_run(ssh, "df -h / | awk 'NR==2{print $3}'")
            disk_pct = stats.ssh_run(ssh, "df -h / | awk 'NR==2{print $5}'")

            uptime = stats.ssh_run(ssh, "uptime -p")
            os_name = stats.ssh_run(ssh, "grep PRETTY_NAME /etc/os-release | cut -d= -f2 | tr -d '\"'")

            ssh.close()
            
            embed = discord.Embed(title="Server Stats", color=0x2ecc71)
            embed.add_field(name="OS", value=os_name, inline=False)
            embed.add_field(
                name="CPU",
                value=f"`{cpu_model.strip()}` ({cpu_cores} cores)\nLoad: **{cpu_load}%**",
                inline=False
            )
            embed.add_field(
                name="RAM",
                value=f"Used: **{ram_used} / {ram_total}**\nType: {ram_type} @ {ram_speed}",
                inline=True
            )
            embed.add_field(
                name="Disk (/)",
                value=f"Used: **{disk_used} / {disk_total}** ({disk_pct})",
                inline=True
            )
            embed.add_field(name="Uptime", value=uptime, inline=False)

            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"Failed to fetch stats: `{e}`", ephemeral=True)