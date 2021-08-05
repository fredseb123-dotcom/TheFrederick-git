import discord
import traceback
import asyncio
from discord.ext import commands
from TFBotTime import TFT
from TFDBUtils import TFDB
from TFCFGUtils import TFCFG
from TFPermCheck import TFP

data = TFCFG.load_cfg()

class Mute(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ttmt(self, ctx, member: discord.Member, time: int, d: str, *, reason=None):
        role = discord.utils.get(ctx.guild.roles,id=843495301121572874)
        await member.add_roles(role)

        embed = discord.Embed(title="muted!", description=f"{member.mention} has been tempmuted ", colour=discord.Colour.light_gray())
        embed.add_field(name="reason:", value=reason, inline=False)
        embed.add_field(name="time left for the mute:", value=f"{time}{d}", inline=False)
        await ctx.send(embed=embed)

        if d == "s":
            await asyncio.sleep(time)

        if d == "m":
            await asyncio.sleep(time*60)

        if d == "h":
            await asyncio.sleep(time*60*60)

        if d == "d":
            await asyncio.sleep(time*60*60*24)

        await member.remove_roles(role)

        embed = discord.Embed(title="unmute (temp) ", description=f"unmuted -{member.mention} ", colour=discord.Colour.light_gray())
        await ctx.send(embed=embed)

        return

def setup(client):
    client.add_cog(Mute(client))