import traceback
import discord
import asyncio
from discord.ext import commands
from TFBotTime import TFT
from TFDBUtils import TFDB
from TFCFGUtils import TFCFG
from TFPermCheck import TFP

data = TFCFG.load_cfg()

class Tempban(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["tb"])
    async def tempban(self, ctx, member: discord.Member, time="1m", *, reason="None"):
        try:
            if TFP.chperm(ctx.message.author.roles, "tempban_permission") == False:
                return
            if member.top_role.position > ctx.message.author.top_role.position:
                await ctx.message.reply("> Nemužete potrestat tohoto uživatele")
                return
            await ctx.channel.purge(limit=1)
            embed = discord.Embed(title=f":hammer: :clock1: Zabanován {member}", description=f"Důvod: {reason}\nDoba: {time}\nID: {member.id}\n{TFT.cas()}", color=discord.Color.red())
            embed.set_footer(text=f"Trestal {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
            channel = discord.utils.get(ctx.guild.channels, id=data["admin_log_channel_id"])
            await channel.send(embed=embed)
            TFDB.write_data("tempban", f"{member.id}", f"{reason}", f"{ctx.message.author.id}" ,f"{TFT.cas()}", f"{time}")
            try:
                await member.send(embed=embed)
            except Exception:
                pass
            await member.ban(reason=reason)
            if "s" in time:
                time = round(float(time.replace("s", "0"))) / 10
            elif "m" in time:
                time = round(float(time.replace("m", "0"))) / 10 * 60
            elif "h" in time:
                time = round(float(time.replace("h", "0"))) / 10 * 60 * 60
            elif "d" in time:
                time = round(float(time.replace("d", "0"))) / 10 * 60 * 60 * 24
            await asyncio.sleep(time)
            try:
                await ctx.guild.unban(member)
            except Exception:
                return
            embed = discord.Embed(title=f":white_check_mark: :clock1: {member}", description=f"Ban vypršel\n{TFT.cas()}", color=discord.Color.green())
            await channel.send(embed=embed)
            try:
                TFDB.delete_by_id("ban", f"{member.id}")
            except Exception:
                pass
            try:
                TFDB.delete_by_id("tempban", f"{member.id}")
            except Exception:
                pass
        except Exception as e:
            info = await self.client.application_info()
            await info.owner.send(f"```PY\n{str(traceback.format_exc())}```")

def setup(client):
    client.add_cog(Tempban(client))