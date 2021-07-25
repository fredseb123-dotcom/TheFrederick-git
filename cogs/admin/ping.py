"""
Modul měřící ping
"""
from time import time
from discord import Embed
from discord.ext import commands
from utils.control import chperm


class Ping(commands.Cog):
    """Třída ping příkazů"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        """Zaslání hodnoty odezvy"""

        if not chperm(ctx.message.author.roles, "ping_permission"):
            return

        start = time()
        message = await ctx.channel.send("Měřím ping...")
        end = time()
        await message.delete()
        embed = Embed(
            title=f"{round(self.client.latency * 1000)} ms | API {round((end-start) * 1000)} ms",
            colour=0xFFFFFF,
        )
        await ctx.channel.send(embed=embed)


def setup(client):
    """Načtení modulu"""
    client.add_cog(Ping(client))
