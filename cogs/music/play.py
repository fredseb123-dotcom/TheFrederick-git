"""
Youtube
"""

import os
import discord
import youtube_dl
from youtube_dl.utils import YoutubeDLError
from utils.control import chperm, load_cfg
from discord import FFmpegPCMAudio
from discord.ext import commands


class Play(commands.Cog):
    """Třída music příkazů"""

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["p"])
    async def play(self, ctx, url):

        """Připojení + přehrání hudby z odkazu"""

        if not chperm(ctx.message.author.roles, "play_permission"):
            return

        if not ctx.message.author.voice:
            await ctx.message.reply(
                ":grey_exclamation: Musíš být v hlasovém kanále",
                delete_after=load_cfg("error_timeout"),
            )
            return

        ydl_opts = {
            "format": "bestaudio/best",
            "extractaudio": True,
            "audioformat": "mp3",
            "outtmpl": "download/song.%(ext)s",
            "restrictfilenames": True,
            "noplaylist": True,
            "nocheckcertificate": True,
        }

        for file in os.listdir("download"):
            if "song" in str(file):
                os.remove(f"download/{file}")

        channel = discord.utils.get(ctx.guild.channels, id=load_cfg("music_channel_id"))
        embed = discord.Embed(title=":mag: | Hledám", description=url, color=0xFFFFFF)
        await channel.send(embed=embed)

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
            except YoutubeDLError:
                embed = discord.Embed(
                    title=":x: | Nenalezeno", color=discord.Color.red()
                )
                await channel.send(embed=embed)

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if not voice:
            voice = await ctx.message.author.voice.channel.connect()

        for file in os.listdir("download"):
            if "song" in str(file):

                if voice.is_playing():
                    voice.stop()

                voice.play(FFmpegPCMAudio(f"download/{file}"))
                embed = discord.Embed(
                    title=":notes: | Přehrávaní odkazu",
                    description=f"Nyní hraje [tato]({url}) skladba",
                    color=0xFFFFFF,
                )
                await channel.send(embed=embed)


def setup(client):
    """Načtení modulu"""

    client.add_cog(Play(client))
