"""
Modul pro mazání zpráv
"""

import discord
from discord.ext import commands
from utils.control import chperm, load_cfg


class Clear(commands.Cog):
    """Třída clear příkazů"""

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["c"])
    async def clear(self, ctx, amount=5, *, reason="None"):
        """Clear command"""

        if not chperm(ctx.message.author.roles, "clear_permission"):
            return

        if amount > load_cfg("clear_limit"):
            await ctx.message.reply(
                "> Překročen limit", delete_after=load_cfg("error_timeout")
            )
            return

        if ctx.channel.id in load_cfg("clear_blacklisted_channels_ids"):
            await ctx.message.reply(
                "> Zde nemůžeš mazat zprávy", delete_after=load_cfg("error_timeout")
            )
            return

        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        embed = discord.Embed(
            colour=discord.Color.orange(),
            title=f":wastebasket: {amount} zpráv",
            description=f"Důvod: {reason}",
        )
        embed.set_footer(
            text=f"Smazal {ctx.message.author}", icon_url=ctx.message.author.avatar_url
        )
        await ctx.channel.send(embed=embed)

    @commands.command(aliases=["sc"])
    async def sclear(self, ctx, amount=5):
        """Silent clear command"""

        if not chperm(ctx.message.author.roles, "sclear_permission"):
            return

        if amount > load_cfg("clear_limit"):
            await ctx.message.reply(
                "> Překročen limit", delete_after=load_cfg("error_timeout")
            )
            return

        if ctx.channel.id in load_cfg("clear_blacklisted_channels_ids"):
            await ctx.message.reply(
                "> Zde nemůžeš mazat zprávy", delete_after=load_cfg("error_timeout")
            )
            return

        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)


def setup(client):
    """Načtení modulu"""
    client.add_cog(Clear(client))
