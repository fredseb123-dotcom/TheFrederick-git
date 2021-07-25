"""
------------------------------------
By TheFrederick#8776 | NoctaneBuilds
------------------------------------
"""
from os import listdir, environ, system
from discord import Intents
from discord.ext import commands
from utils.control import load_cfg, start_seq

system("clear")
client = commands.Bot(
    command_prefix=load_cfg("prefix"),
    intents=Intents.all(),
    strip_after_prefix=True,
)
client.remove_command('help')

start_seq()
for direct in listdir("cogs"):
    for filename in listdir(f"cogs/{direct}"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{direct}.{filename[:-3]}")
    print(f"✅ | {direct.capitalize()} loaded")

client.run(environ["FREDERICK"])
