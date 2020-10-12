import discord
import random
import os
from discord.ext import commands
from config/config.py import discord

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
client.run(token)
