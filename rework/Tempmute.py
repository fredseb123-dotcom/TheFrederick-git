import traceback
import discord
import asyncio
from discord.ext import commands
from TFBotTime import TFT
from TFDBUtils import TFDB
from TFCFGUtils import TFCFG
from TFPermCheck import TFP

data = TFCFG.load_cfg()

class Tempmute(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["tm"])
    async def tempmute(self, ctx, member: discord.Member, time="1m", *, reason="None"):
        try:
            if TFP.chperm(ctx.message.author.roles, "tempmute_permission") == False:
                return
            if member.top_role.position > ctx.message.author.top_role.position:
                await ctx.message.reply("> Nemužete potrestat tohoto uživatele")
                return
            role = discord.utils.get(ctx.guild.roles,id=data["mute_role_id"])
            if role.name in str(member.roles):
                await ctx.message.reply("> Uživatel je již umlčen")
                return
            await ctx.channel.purge(limit=1)
            await member.add_roles(role)
            await member.move_to(None)
            embed = discord.Embed(title=f":mute: :clock1: Umlčen {member}", description=reason + f"Důvod: {reason}\nDoba: {time}\n{TFT.cas()}", color=discord.Color.red())
            embed.set_footer(text=f"Trestal {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
            channel = discord.utils.get(ctx.guild.channels, id=data["admin_log_channel_id"])
            await channel.send(embed=embed)
            try:
                await member.send(embed=embed)
            except Exception:
                pass
            TFDB.write_data("tempmute", f"{member.id}", f"{reason}", f"{ctx.message.author.id}" ,f"{TFT.cas()}", f"{time}")
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
                await member.remove_roles(role)
            except Exception:
                return
            await member.move_to(None)
            embed = discord.Embed(title=f":white_check_mark: :clock1: {member}", description=f"Mute vypršel\n{TFT.cas()}", color=discord.Color.green())
            await channel.send(embed=embed)
            try:
                await member.send(embed=embed)
            except Exception:
                pass
            try:
                TFDB.delete_by_id("mute", f"{member.id}")
            except Exception:
                pass
            try:
                TFDB.delete_by_id("tempmute", f"{member.id}")
            except Exception:
                pass
        except Exception:
            info = await self.client.application_info()
            await info.owner.send(f"```PY\n{str(traceback.format_exc())}```")

def setup(client):
    client.add_cog(Tempmute(client))