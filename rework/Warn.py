import discord
import traceback
from discord.ext import commands
from TFBotTime import TFT
from TFDBUtils import TFDB
from TFCFGUtils import TFCFG
from TFPermCheck import TFP

data = TFCFG.load_cfg()

class Warn(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["w"])
    async def warn(self, ctx, member: discord.Member, *, reason="None"):
        try:
            if TFP.chperm(ctx.message.author.roles, "tempban_permission") == False:
                return
            if member.top_role.position > ctx.message.author.top_role.position:
                await ctx.message.reply("> Nemužete potrestat tohoto uživatele")
                return
            await ctx.channel.purge(limit=1)
            channel = discord.utils.get(ctx.guild.channels, id=data["admin_log_channel_id"])
            if int(TFDB.count_all_by_id("warn", str(member.id))) == 2:
                embed = discord.Embed(colour=discord.Color.blue(), title=f':mans_shoe: Vyhozen {member}', description=f"Důvod: {reason}\n*Dosaženo 3 Warnů*\n{TFT.cas()}")
                embed.set_footer(text=f'Trestal {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
                await channel.send(embed=embed)
                try:
                    await member.send(embed=embed)
                except Exception:
                    pass
                TFDB.delete_by_id("warn", f"{member.id}")
                await member.kick(reason="Dosaženo 3 Warnů")
            else:
                embed = discord.Embed(colour=discord.Color.orange(), title=f':warning: Varování {member}', description=f"Důvod: {reason}\n{TFT.cas()}")
                embed.set_footer(text=f'Trestal {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
                await channel.send(embed=embed)
                try:
                    await member.send(embed=embed)
                except Exception:
                    pass
                TFDB.write_data("warn", f"{member.id}", f"{reason}", f"{ctx.message.author.id}", f"{TFT.cas()}", "None")
        except Exception:
            info = await self.client.application_info()
            await info.owner.send(f"```PY\n{str(traceback.format_exc())}```")

def setup(client):
    client.add_cog(Warn(client))