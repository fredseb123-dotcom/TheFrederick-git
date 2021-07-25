"""
Modul pro Help command
"""

from discord.ext import commands
from utils.control import load_cfg


class Help(commands.Cog):
    """Třída ping příkazů"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        """Zaslání hodnoty odezvy"""
        if ctx.channel.id != load_cfg("bot_spam_id"):
            await ctx.message.delete()
            return

        await ctx.channel.send("Brzy v provozu...")


def setup(client):
    """Načtení modulu"""
    client.add_cog(Help(client))
