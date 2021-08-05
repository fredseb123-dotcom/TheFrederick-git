"""
Modul řídící support
"""

import discord
from discord.ext import commands
from utils.control import load_cfg, time_now


class Support(commands.Cog):
    """Třída Support příkazů"""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Připojení do čekárny"""

        if member.bot:
            return

        if not after.channel:
            return

        if after.channel.id == load_cfg("support_channel_id"):
            support = discord.utils.get(
                after.channel.guild.channels, id=load_cfg("support_notify_channel_id")
            )
            staff = discord.utils.get(
                after.channel.guild.roles, id=load_cfg("support_role_id")
            )
            embed = discord.Embed(
                colour=0xFFFFFF,
                title=":grey_exclamation: Čekárna",
                description=f"Čekající: {member.mention}\n{staff.mention}\n{time_now()}",
            )
            await support.send(embed=embed)


def setup(client):
    """Načtení modulu"""

    client.add_cog(Support(client))
