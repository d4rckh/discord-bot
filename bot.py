import discord
import random
import os
from discord.ext import commands
from config/config.py import *

client = commands.Bot(command_prefix='!')
client.remove_command('help')

@client.event
async def on_ready():
    channel = discord.utils.get(client.get_all_channels(), name='general')
    print('\n Bot is online! :)')
    print('-'*21)

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f"`{extension} cog has been loaded.`")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f"`{extension} cog has been unloaded.`")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#chat logs
@client.event
async def on_message(message):
    with io.open("chatlogs.txt", "a", encoding="utf-8") as f:
        f.write(
            "[{}] | [{}] | [{}] @ {}: {}\n".format(message.guild,
                                                   message.channel,
                                                   message.author,
                                                   message.created_at,
                                                   message.content))
    f.close()
    print(
        Fore.WHITE + "[" + Fore.LIGHTRED_EX + '+' + Fore.WHITE + "]"
        + Fore.LIGHTRED_EX + "[{}] | [{}] | [{}] @ {}: {}".format(
            message.guild, message.channel, message.author,
            message.created_at, message.content))

    await client.process_commands(message)
#purge command
@client.command(pass_context=True)
async def purge(ctx, amount=5):
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.guild_permissions.ban_members:
        await ctx.channel.purge(limit=amount)
        await ctx.author.send(f"purged {amount} messages.")
        channel = client.get_channel(general_actions_log_channel_id)
        await channel.send(str(ctx.message.author)+ " " + f"just purged {amount} messages! ")

@client.command(pass_context=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    admin = ctx.message.author.guild_permissions.administrator
    banperm = ctx.message.author.guild_permissions.ban_members
    if reason == None:
        await ctx.send("you must enter a reason to warn")
    else:
        try:
            if admin or banperm:
                message = f"You have been warned from `` {ctx.guild.name} ``\
                    by `` {ctx.message.author} `` for `` {reason} ``"
                embed = discord.Embed(
                    colour=discord.Color.red()
                )
                embed.add_field(name="WARNED",
                                value=message,
                                inline=False)
                await member.send(embed=embed)
                embed = discord.Embed(title=
                                      "User was warned for {}".format(reason),
                                      description="**{}** has been warned!"
                                      .format(member),
                                      color=discord.Color.green())
                embed.set_author(name=ctx.message.author,
                                 icon_url=ctx.message.author.avatar_url)

                await ctx.send(embed=embed)
                author = ctx.message.author
                channel = client.get_channel(admin_actions_log_channel_id)
                await channel.send(f"{author} just warned {member} for {reason} ")
            else:
                embed = discord.Embed(title="Permission Denied.",
                                      description="You don't have \
                                      permission to use this command.",
                                      color=discord.Color.red())
                await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title="Permission Denied.",
                                  description="Bot doesn't have correct \
                                  permissions, or bot can't ban this user.",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)




@client.command(pass_context=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    admin = ctx.message.author.guild_permissions.administrator
    banperm = ctx.message.author.guild_permissions.ban_members

    if reason == None:
        await ctx.send("you must enter a reason to ban.")
    else:
        try:
            if admin or banperm:
                message = f"You have been banned from `` {ctx.guild.name} `` by `` {ctx.message.author} `` for `` {reason}``"
                embed = discord.Embed(
                    colour=discord.Color.red()
                )
                embed.add_field(name="BANNED",
                                value=message,
                                inline=False)
                await member.send(embed=embed)
                await ctx.guild.ban(member)
                embed = discord.Embed(title="User banned was banned for {}".format(reason),
                                      description="**{}** has been banned!".format(member),
                                      color=discord.Color.green())
                embed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)

                await ctx.send(embed=embed)
                author = ctx.message.author
                channel = client.get_channel(admin_actions_log_channel_id)
                await channel.send(f"{author} just banned {member} for {reason}")
            else:
                embed = discord.Embed(title="Permission Denied.",
                                      description="You don't have permission to use this command.",
                                      color=discord.Color.red())
                await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title="Permission Denied.",
                                  description="Bot doesn't have correct permissions, or bot can't ban this user.",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)

client.run(token)
