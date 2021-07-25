"""
Hudba
"""

import discord
import yaml
from discord import FFmpegPCMAudio
from discord.ext import commands
from utils.control import chperm, load_cfg, load_radio


class Music(commands.Cog):
    """Třída music příkazů"""

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["stop"])
    async def leave(self, ctx):
        """Odpojení"""

        if not chperm(ctx.message.author.roles, "leave_permission"):
            return

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if voice.is_connected():
            await ctx.message.guild.voice_client.disconnect()
            embed = discord.Embed(title=":wave: | Přehrávač odpojen", color=0xFFFFFF)
            channel = discord.utils.get(
                ctx.guild.channels, id=load_cfg("music_channel_id")
            )
            await channel.send(embed=embed)

        else:
            await ctx.channel.send(
                ":grey_exclamation: Přehrávač není připojen",
                delete_after=load_cfg("error_timeout"),
            )
            return

    @commands.command(aliases=["pa"])
    async def pause(self, ctx):
        """Pauznutí přehrávače"""

        if not chperm(ctx.message.author.roles, "pause_permission"):
            return

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.pause()
            embed = discord.Embed(
                title=":pause_button: | Přehrávač pozastaven", color=0xFFFFFF
            )
            channel = discord.utils.get(
                ctx.guild.channels, id=load_cfg("music_channel_id")
            )
            await channel.send(embed=embed)

        else:
            await ctx.channel.send(
                ":grey_exclamation: Není nic přehráváno",
                delete_after=load_cfg("error_timeout"),
            )
            return

    @commands.command(aliases=["re"])
    async def resume(self, ctx):
        """Spuštění přehrávače"""

        if not chperm(ctx.message.author.roles, "resume_permission"):
            return

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if voice.is_paused():
            voice.resume()
            embed = discord.Embed(
                title=":arrow_forward: | Přehrávač spuštěn", color=0xFFFFFF
            )
            channel = discord.utils.get(
                ctx.guild.channels, id=load_cfg("music_channel_id")
            )
            await channel.send(embed=embed)

        else:
            await ctx.channel.send(
                ":grey_exclamation: Přehrávač není pozastaven",
                delete_after=load_cfg("error_timeout"),
            )
            return

    @commands.command(aliases=["r"])
    async def radio(self, ctx, radio="evropa2"):
        """Připojení + radio"""

        if not chperm(ctx.message.author.roles, "radio_permission"):
            return

        if not ctx.message.author.voice:
            await ctx.message.reply(
                ":grey_exclamation: Musíš být v hlasovém kanále",
                delete_after=load_cfg("error_timeout"),
            )
            return

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if not voice:
            voice = await ctx.message.author.voice.channel.connect()

        if voice.is_playing():
            voice.stop()

        voice.play(FFmpegPCMAudio(load_radio(radio)))
        embed = discord.Embed(title=f":mega: | Rádio {radio}", color=0xFFFFFF)
        channel = discord.utils.get(ctx.guild.channels, id=load_cfg("music_channel_id"))
        await channel.send(embed=embed)

    @commands.command()
    async def radios(self, ctx):
        """Výpis dosupných rádiových stanic"""

        if not chperm(ctx.message.author.roles, "radios_permission"):
            return

        tmp = []
        with open("config/radios.yml", "r") as file:
            perm = yaml.load(file, Loader=yaml.FullLoader)
            for elem in perm:
                tmp.append(f"[{elem.capitalize()}]({perm[elem]})")

        embed = discord.Embed(
            title=":musical_note: | Rádiové stanice",
            description="\n".join(tmp),
            color=0xFFFFFF,
        )
        channel = discord.utils.get(ctx.guild.channels, id=load_cfg("music_channel_id"))
        await channel.send(embed=embed)


def setup(client):
    """Načtení modulu"""

    client.add_cog(Music(client))
