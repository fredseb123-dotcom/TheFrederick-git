import discord
import traceback
from discord.ext import commands
from discord.ext.commands import MemberConverter
from TFDBUtils import TFDB
from TFCFGUtils import TFCFG
from TFPermCheck import TFP

data = TFCFG.load_cfg()

class Check(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["ch"])
    async def check(self, ctx, member):
        try:
            if TFP.chperm(ctx.message.author.roles, "check_permission") == False:
                return
            try:
                member = await MemberConverter().convert(ctx, member)
                member_id = member.id
            except Exception:
                member_id = int(member)
            overeni = ":no_entry_sign:"
            try:
                role = discord.utils.get(ctx.guild.roles,id=data["valid_role_id"])
                if role.name in str(member.roles):
                    overeni = f"{member.display_name}"
            except Exception:
                pass
            await ctx.channel.purge(limit=1)
            embed = discord.Embed(title=":mag: Info", color=discord.Color.blue())
            embed.add_field(name=':globe_with_meridians: ID', value=f'<@{member_id}> | {member_id}', inline=False)
            try:
                embed.add_field(name=':bust_in_silhouette: Vytvoření',value=(str(member.created_at)[:-7]), inline=False)
                embed.add_field(name=':arrow_right: Připojení', value=(str(member.joined_at)[:-7]), inline=False)
                embed.add_field(name=':left_right_arrow: Propojení', value=overeni, inline=False)
            except Exception:
                pass
            embed.add_field(name='\u200B\n:mute: Mute', value=TFDB.find_by_id("mute", member_id), inline=False)
            embed.add_field(name='\u200B\n:mute: :clock1: Tempmute', value=TFDB.find_by_id("tempmute", member_id), inline=False)
            embed.add_field(name='\u200B\n:hammer: Ban', value=TFDB.find_by_id("ban", member_id), inline=False)
            embed.add_field(name='\u200B\n:hammer: :clock1: Tempban', value=TFDB.find_by_id("tempban", member_id), inline=False)
            count = TFDB.count_all_by_id("warn", member_id)
            embed.add_field(name=f'\u200B\n:warning: | Warn {count}', value=TFDB.find_all_by_id("warn", member_id), inline=False)
            try:
                embed.set_thumbnail(url = member.avatar_url)
            except Exception:
                pass
            await ctx.message.author.send(embed=embed)
        except Exception:
            info = await self.client.application_info()
            await info.owner.send(f"```PY\n{str(traceback.format_exc())}```")

def setup(client):
    client.add_cog(Check(client))