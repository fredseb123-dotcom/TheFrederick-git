"""
By TheFrederick#8776
"""

from os import listdir, environ
from discord import Intents, AllowedMentions
from discord.ext import commands
from utils.control import load_cfg, start_seq

client = commands.Bot(
    command_prefix=load_cfg("prefix"),
    intents=Intents.all(),
    strip_after_prefix=True,
    case_insensitive=True,
    help_command=None,
    allowed_mentios=AllowedMentions(
        users=True,
        everyone=False,
        roles=False,
        replied_user=True,
    ),
)

start_seq()
for direct in listdir("cogs"):
    for filename in listdir(f"cogs/{direct}"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{direct}.{filename[:-3]}")
    print(f"│ ✅ │ {direct.capitalize()}\n├────┼───────────────────────────")

client.run(environ["FREDERICK"])
