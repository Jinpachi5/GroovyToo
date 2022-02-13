import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix = '!')


@client.event
async def on_ready():
    print('Bot is ready')

@client.command
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')



@client.command()
async def clear(ctx, amount = 1):
    if amount <= 100:
        await ctx.channel.purge(limit = amount + 1)



client.run('ODg3MDk3NjQ4MzU0NTgyNTk5.YT_MEA.eQZgiZiG6Jr0BIK9YbRqDwJFtzQ')