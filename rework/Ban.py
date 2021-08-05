import discord
import traceback
from discord.ext import commands
from TFBotTime import TFT
from TFDBUtils import TFDB
from TFCFGUtils import TFCFG
from TFPermCheck import TFP

data = TFCFG.load_cfg()

class Ban(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["b"])
    async def ban(self, ctx, member: discord.Member, *, reason = "None"):
        try:
            if TFP.chperm(ctx.message.author.roles, "ban_permission") == False:
                return
            if member.top_role.position > ctx.message.author.top_role.position:
                await ctx.message.reply("> Nemužete potrestat tohoto uživatele")
                return
            await ctx.channel.purge(limit=1)
            channel = discord.utils.get(ctx.guild.channels, id=data["admin_log_channel_id"])
            embed = discord.Embed(colour=discord.Color.red(), title=f":hammer: Zabanován {member}", description=f"Důvod: {reason}\nID: {member.id}\n{TFT.cas()}")
            embed.set_footer(text=f'Trestal {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
            await channel.send(embed=embed)
            try:
                await member.send(embed=embed)
            except Exception:
                pass
            await member.ban(reason=reason)
            TFDB.write_data("ban", f"{member.id}", f"{reason}", f"{ctx.message.author.id}", f"{TFT.cas()}", "None")
        except Exception:
            info = await self.client.application_info()
            await info.owner.send(f"```PY\n{str(traceback.format_exc())}```")

    @commands.command(aliases=["ub"])
    async def unban(self, ctx, id, *, member):
        try:
            if TFP.chperm(ctx.message.author.roles, "unban_permission") == False:
                return
            await ctx.channel.purge(limit=1)
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')
            for ban_entry in banned_users:
                user = ban_entry.user
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    channel = discord.utils.get(ctx.guild.channels, id=data["admin_log_channel_id"])
                    await ctx.guild.unban(user)
                    embed = discord.Embed(title=f":white_check_mark: {member}", description=f"{TFT.cas()}", color=discord.Color.green())
                    embed.set_footer(text=f"Odbanoval {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
                    await channel.send(embed=embed)
                    try:
                        TFDB.delete_by_id("ban", f"{id}")
                    except Exception:
                        pass
                    try:
                        TFDB.delete_by_id("tempban", f"{id}")
                    except Exception:
                        pass
        except Exception:
            info = await self.client.application_info()
            await info.owner.send(f"```PY\n{str(traceback.format_exc())}```")

def setup(client):
    client.add_cog(Ban(client))
