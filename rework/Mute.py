import discord
import traceback
from discord.ext import commands
from TFBotTime import TFT
from TFDBUtils import TFDB
from TFCFGUtils import TFCFG
from TFPermCheck import TFP

data = TFCFG.load_cfg()

class Mute(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["m"])
    async def mute(self, ctx, member: discord.Member, *, reason="None"):
        try:
            if TFP.chperm(ctx.message.author.roles, "mute_permission") == False:
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
            embed = discord.Embed(title=f":mute: Umlčen {member}", description=f"Důvod: {reason}\n{TFT.cas()}", color=discord.Color.red())
            embed.set_footer(text=f"Trestal {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
            channel = discord.utils.get(ctx.guild.channels, id=data["admin_log_channel_id"])
            await channel.send(embed=embed)
            try:
                await member.send(embed=embed)
            except Exception:
                pass
            TFDB.write_data("mute", f"{member.id}", f"{reason}", f"{ctx.message.author.id}", f"{TFT.cas()}", "None")
        except Exception:
            info = await self.client.application_info()
            await info.owner.send(f"```PY\n{str(traceback.format_exc())}```")

    @commands.command(aliases=["um"])
    async def unmute(self, ctx, member: discord.Member):
        try:
            if TFP.chperm(ctx.message.author.roles, "unmute_permission") == False:
                return
            role = discord.utils.get(ctx.guild.roles,id=data["mute_role_id"])
            if role.name not in str(member.roles):
                await ctx.message.reply("> Uživatel není umlčen")
                return
            await ctx.channel.purge(limit=1)
            await member.remove_roles(role)
            await member.move_to(None)
            embed = discord.Embed(title=f":white_check_mark: {member}", description=f"{TFT.cas()}", color=discord.Color.green())
            embed.set_footer(text=f"Odmlčel {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
            channel = discord.utils.get(ctx.guild.channels, id=data["admin_log_channel_id"])
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
    client.add_cog(Mute(client))