"""
Modul pro Hug command
"""

from random import randint
from discord import Member, Embed
from discord.ext import commands
from utils.control import load_cfg


class Hug(commands.Cog):
    """Třída hug příkazů"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, load_cfg("cmd_cooldown"), commands.BucketType.user)
    async def hug(self, ctx, member: Member):
        """Zaslání obětí"""
        if ctx.message.author.bot:
            return

        if ctx.channel.id != load_cfg("bot_spam_id"):
            return

        embed = Embed(title=f"{ctx.message.author} obejmul {member}", color=0xFF96F3)
        embed.set_image(url=f"https://cdn.nekos.life/hug/hug_0{randint(10,89)}.gif")
        await ctx.channel.send(embed=embed)


def setup(client):
    """Načtení modulu"""
    client.add_cog(Hug(client))
