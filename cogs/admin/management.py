"""
Modul řídící práci s moduly
"""

import os
import discord
import yaml
from utils.control import load_cfg
from discord.ext import commands


class Management(commands.Cog):
    """Třída řídících příkazů"""

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["l"], hidden=True)
    @commands.is_owner()
    async def load(self, ctx, extension):
        """Nahrání modulu"""

        self.client.load_extension(f"cogs.{extension.lower()}")
        embed = discord.Embed(
            title=f":white_check_mark: {extension}",
            colour=discord.Color.green(),
        )

        if isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.send(embed=embed)
        else:
            await ctx.message.delete()
            await ctx.message.author.send(embed=embed)

    @commands.command(aliases=["ul", "u"], hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, extension):
        """Vypnutí modulu"""

        self.client.unload_extension(f"cogs.{extension.lower()}")
        embed = discord.Embed(
            title=f":x: {extension}",
            colour=discord.Color.red(),
        )

        if isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.send(embed=embed)
        else:
            await ctx.message.delete()
            await ctx.message.author.send(embed=embed)

    @commands.command(aliases=["rl"], hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, extension):
        """Reload modulu"""

        self.client.reload_extension(f"cogs.{extension.lower()}")
        embed = discord.Embed(
            title=f":arrows_counterclockwise: {extension}",
            colour=discord.Color.blue(),
        )

        if isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.send(embed=embed)
        else:
            await ctx.message.delete()
            await ctx.message.author.send(embed=embed)

    @commands.command(aliases=["?"], hidden=True)
    @commands.is_owner()
    async def modules(self, ctx):
        """Status modulů"""

        tmp = []
        for filename in os.listdir(load_cfg("cogs_path")):
            if filename.endswith(".py"):
                modul_name = (filename[:-3]).capitalize()
                try:
                    valid = self.client.cogs[modul_name]
                    del valid
                    modul_satus = ":green_circle:"
                except KeyError:
                    modul_satus = ":red_circle:"
                tmp.append(f"{modul_satus} {modul_name}")
            else:
                tmp.append(f":file_folder: {filename}")
        count = len(tmp) - 1
        tmp = "\n".join(tmp)
        embed = discord.Embed(colour=discord.Color.blue())
        embed.add_field(
            name=f":mag: Moduly | {count} | {round(self.client.latency * 1000)} ms",
            value=f"{tmp}",
        )

        if isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.send(embed=embed)
        else:
            await ctx.message.delete()
            await ctx.message.author.send(embed=embed)

    @commands.command(aliases=["cat"], hidden=True)
    @commands.is_owner()
    async def readfile(self, ctx, path):
        """Obsah modulů"""

        try:
            file_content = discord.File(f"{path}")
        except FileNotFoundError:
            return

        if isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.send(file=file_content)
        else:
            await ctx.message.delete()
            await ctx.message.author.send(file=file_content)

    @commands.command(aliases=["perm"], hidden=True)
    @commands.is_owner()
    async def permission(self, ctx, member: discord.Member):
        """Zobrazí permisse uživatele z perms.yml"""

        final = []
        with open("config/perms.yml") as file:
            perm = yaml.load(file, Loader=yaml.FullLoader)
        for role in member.roles:
            for elem in perm:
                if role.id in perm[elem]:
                    final.append(elem.capitalize()[:-11])

        perms = "\n".join(final)
        embed = discord.Embed(
            colour=discord.Color.blue(), title=":mag: Práva", description=perms
        )

        await ctx.message.delete()
        await ctx.message.author.send(embed=embed)


def setup(client):
    """Načtení modulu"""

    client.add_cog(Management(client))
