"""
Modul pro ověření uživatele
"""

import discord
from utils.control import load_cfg
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw


class Verify(commands.Cog):
    """Třída ověřujících příkazů"""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        """Vykonání nutných příkazů"""

        if (
            message.channel.id == load_cfg("captcha_channel_id")
            and message.content == "Noctane"
        ):
            await message.delete()
            role = discord.utils.get(message.guild.roles, id=load_cfg("join_role_id"))
            await message.author.add_roles(role)

            img1 = Image.open("images/background.png")
            copy_img1 = img1.copy()
            font_1 = ImageFont.truetype("images/monofonto.ttf", 64)
            font_2 = ImageFont.truetype("images/monofonto.ttf", 48)
            draw = ImageDraw.Draw(copy_img1)
            draw.text((70, 35), "Vítej", (255, 255, 255), font=font_1)
            draw.text((70, 120), f"{message.author}", (255, 255, 255), font=font_2)
            copy_img1.save("images/welcome.png")

            channel = discord.utils.get(
                message.guild.channels, id=load_cfg("join_channel_id")
            )
            await channel.send(file=discord.File("images/welcome.png"))

            return

        if message.channel.id == load_cfg("captcha_channel_id"):
            await message.delete()
            return


def setup(client):
    """Načtení modulu"""
    client.add_cog(Verify(client))
