"""
Modul řídící chybová hlášení
"""

from discord.ext import commands
from utils.control import load_cfg


class Errors(commands.Cog):
    """Třída chybových příkazů"""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Odchycení chyby"""

        time = load_cfg("error_timeout")
        if isinstance(error, commands.MissingAnyRole):
            await ctx.message.reply("Na toto nemáte práva", delete_after=time)

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.reply("Potřebuji více informací", delete_after=time)

        if isinstance(error, commands.CommandNotFound):
            await ctx.message.reply("Neznámý příkaz", delete_after=time)

        if isinstance(error, commands.MemberNotFound):
            await ctx.message.reply("Neznámý uživatel", delete_after=time)

        if isinstance(error, commands.CheckAnyFailure):
            await ctx.message.reply("Interní chyba", delete_after=time)

        if isinstance(error, commands.NotOwner):
            await ctx.message.reply("Nejste mým pánem!", delete_after=time)

        if isinstance(error, commands.UserNotFound):
            await ctx.message.reply("Neznámý uživatel", delete_after=time)

        if isinstance(error, commands.TooManyArguments):
            await ctx.message.reply("Příliš mnoho parametrů", delete_after=time)

        if isinstance(error, commands.MissingPermissions):
            await ctx.message.reply("Na toto nemám oprávnění", delete_after=time)


def setup(client):
    """Načtení modulu"""
    client.add_cog(Errors(client))
