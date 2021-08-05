"""
Modul pro kick uživatele
"""

import discord
from discord.errors import Forbidden
from discord.ext import commands
from utils.control import chperm, time_now, load_cfg


class Kick(commands.Cog):
    """Třída kick příkazů"""

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["k"])
    async def kick(self, ctx, member: discord.Member, *, reason="None"):
        """Kick command"""

        if not chperm(ctx.message.author.roles, "kick_permission"):
            return

        await ctx.channel.purge(limit=1)
        channel = discord.utils.get(ctx.guild.channels, id=load_cfg("staff_channel_id"))
        embed = discord.Embed(
            colour=discord.Color.blue(),
            title=f":mans_shoe: Vyhozen {member}",
            description=f"Důvod: {reason}\n{time_now()}",
        )
        embed.set_footer(
            text=f"Trestal {ctx.message.author}", icon_url=ctx.message.author.avatar_url
        )
        try:
            await member.send(embed=embed)
        except Forbidden:
            pass
        await channel.send(embed=embed)
        await member.kick(reason=reason)


def setup(client):
    """Načtení modulu"""
    client.add_cog(Kick(client))
