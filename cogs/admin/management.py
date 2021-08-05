"""
Modul řídící práci s moduly
"""

from os import listdir, path
from time import time
import discord
import yaml
from discord.ext import commands
from utils.control import side_by_side


class Management(commands.Cog):
    """Třída řídících příkazů"""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        """Přikazy vykonané po startu"""

        print("│ ⭐ │ Online\n└────┴───────────────────────────")

    @commands.command(aliases=["l"], hidden=True)
    @commands.is_owner()
    async def load(self, ctx, category, extension):
        """Nahrání modulu"""

        self.client.load_extension(f"cogs.{category}.{extension.lower()}")
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
    async def unload(self, ctx, category, extension):
        """Vypnutí modulu"""

        self.client.unload_extension(f"cogs.{category}.{extension.lower()}")
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
    async def reload(self, ctx, category, extension):
        """Reload modulu"""

        self.client.reload_extension(f"cogs.{category}.{extension.lower()}")
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
    async def modules(self, ctx, dir=None):
        """Status všech souborů"""

        blackList = ["download", "tickets", ".git"]

        symbols = {
            "py" : "🐍",
            "txt" : "📄",
            "yml" : "📕",
            "png" : "🎨",
            "ttf" : "❔"
        }

        tmp = []

        longest = 18

        for file in listdir(dir):

            if file in blackList:
                continue

            if path.isdir(file):
                category = []
                category.append("\n📁 " + file.capitalize())

                if file == "cogs":
                    tmp.append("\n".join(category))
                    cogCategories = []
                    for direct in listdir("cogs"):
                        subCategory=[]
                        cogFolder = "📁 " + direct.capitalize()

                        while len(cogFolder) != longest:
                            cogFolder += " "

                        subCategory.append(cogFolder)

                        for fileName in listdir(f"cogs/{direct}"):

                            if listdir(f"cogs/{direct}").index(fileName) == len(listdir(f"cogs/{direct}")) - 1:
                                symbol = "└─"
                            else:
                                symbol = "├─"

                            if fileName.endswith(".py"):
                                modulName = (fileName[:-3]).capitalize()
                                try:
                                    valid = self.client.cogs[modulName]
                                    del valid
                                    modul_satus = "🟢"
                                except KeyError:
                                    modul_satus = "🔴"
                                exactFile = f"{symbol} {modul_satus} {fileName}"
                            elif "_" in fileName:
                                continue
                            else:
                                exactFile = f"{symbol} :question: {fileName}"

                            while len(exactFile) != longest:
                                exactFile += " "

                            subCategory.append(exactFile)

                        cogCategories.append("".join(subCategory))
                    tmp.append(side_by_side(cogCategories, size=longest, space=2))

                else:
                    for fileName in listdir(file):
                        if "_" in fileName:
                            continue

                        if listdir(file).index(fileName) == len(listdir(file)) - 1:
                            symbol = "└─"
                        else:
                            symbol = "├─"

                        modulName = fileName.capitalize()
                        fileType=fileName.split(".")[1]
                        modulIcon = symbols[fileType]
                        category.append(f"{symbol} {modulIcon} {modulName}")

                    tmp.append("\n".join(category))

            else:
                if file.endswith(".py"):
                    file_name = file.capitalize()
                    tmp.append(f"\n🐍 {file_name}")

                elif file.endswith(".db"):
                    file_name = file.capitalize()
                    tmp.append(f"\n🗄️ {file_name}")

                elif "_" in fileName:
                    continue

                else:
                    tmp.append(file.capitalize())

        status = "\n".join(tmp)

        if isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.send(f"```\n{status}\n```")
        else:
            await ctx.message.delete()
            await ctx.send(f"```\n{status}\n```")

    @commands.command(aliases=["cat"], hidden=True)
    @commands.is_owner()
    async def readfile(self, ctx, path):
        """Zaslání modulů"""

        try:
            file_content = discord.File(path)
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
                    final.append(elem.split("_")[0].capitalize())

        perms = ", ".join(final)
        embed = discord.Embed(
            colour=discord.Color.blue(), title=f":mag: Práva {member}", description=perms
        )

        await ctx.message.delete()
        await ctx.message.author.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def ping(self, ctx):
        """Zaslání hodnoty odezvy"""

        start = time()
        message = await ctx.channel.send("Měřím ping...")
        end = time()
        await message.delete()
        embed = discord.Embed(
            title=f"VPS {round(self.client.latency * 1000)} ms | API {round((end-start) * 1000)} ms",
            colour=0xFFFFFF,
        )
        if isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.send(embed=embed)
        else:
            await ctx.message.delete()
            await ctx.message.author.send(embed=embed)


def setup(client):
    """Načtení modulu"""
    client.add_cog(Management(client))
