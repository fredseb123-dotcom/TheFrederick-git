"""
Ticket systém
"""

import discord
from utils.control import load_cfg, chperm
from utils.tickets import has_ticket, write_data, is_ticket, get_ticket, delete_by_id
from discord.ext import commands


class Ticket(commands.Cog):
    """Třída ping příkazů"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def tickets(self, ctx):
        """Vypíše info embed o ticketech"""

        await ctx.message.delete()
        embed = discord.Embed(
            title=":envelope: | Tickety",
            description="**Zneužití ticketů je trestáno!**\nPro vytvoření ticketu reaguj s ✉️",
            color=0xFFFFFF,
        )
        message = await ctx.channel.send(embed=embed)
        await message.add_reaction("✉️")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """Vytvoření ticketu"""

        if user == self.client.user:
            return

        if reaction.message.channel.id != load_cfg("ticket_channel_id"):
            return

        await reaction.message.remove_reaction(reaction.emoji, user)

        if has_ticket(user.id):
            await reaction.message.channel.send(
                f":grey_exclamation: {user.mention} již máš vytvořený ticket.",
                delete_after=load_cfg("error_timeout"),
            )
            return

        if reaction.emoji == "✉️":

            category = discord.utils.get(
                reaction.message.guild.categories, id=load_cfg("ticket_category_id")
            )
            channel = await reaction.message.guild.create_text_channel(
                user.id, category=category
            )
            await channel.set_permissions(
                reaction.message.guild.get_role(reaction.message.guild.id),
                view_channel=False,
            )
            await channel.set_permissions(
                reaction.message.guild.get_role(load_cfg("join_role_id")),
                view_channel=False,
            )
            await channel.set_permissions(user, view_channel=True)
            prefix = load_cfg("prefix")
            embed = discord.Embed(
                description=f"Sděl Nám svůj problém \
                    a vyčkej na odpověd.\nPro uzavření napiš `{prefix}close`.",
                color=0xFFFFFF,
            )
            await channel.send(f"Vítej {user.mention} v ticketu :grey_exclamation:")
            await channel.send(embed=embed)

            write_data(channel.id, user.id)

    @commands.command()
    async def close(self, ctx, member_id=None):
        """Uzavření a uložení zpráv z ticketu"""

        if is_ticket(ctx.channel.id) is False:
            return

        if not member_id:
            member_id = ctx.message.author.id

        messages = [
            f"{message.author} » {message.content}"
            async for message in ctx.channel.history(limit=100)
        ][::-1]

        with open(f"tickets/{member_id}.txt", "a") as ticket:
            ticket.write("\n".join(messages))
            ticket.write("\n---------------\n")

        channel_id = get_ticket(member_id)[0]
        channel = discord.utils.get(ctx.guild.channels, id=channel_id)
        await channel.delete()

        delete_by_id(member_id)

    @commands.command()
    async def log(self, ctx, member_id):
        """Zaslání logu ticketu"""

        if not chperm(ctx.message.author.roles, "log_permission"):
            return

        await ctx.message.delete()
        channel = discord.utils.get(ctx.guild.channels, id=load_cfg("staff_channel_id"))

        try:
            await channel.send(file=discord.File(f"tickets/{member_id}.txt"))
        except FileNotFoundError:
            await channel.send(
                ":grey_exclamation: Záznám s tímto ID nenalezen",
                delete_after=load_cfg("error_timeout"),
            )


def setup(client):
    """Načtení modulu"""

    client.add_cog(Ticket(client))
