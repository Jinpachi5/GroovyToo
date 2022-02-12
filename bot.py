import discord
import random
from discord.ext import commands

client = commands.Bot(command_prefix = '!')


@client.event
async def on_ready():
    print('Bot is ready')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(aliases = ['8ball', 'ball'])
async def _8ball(ctx, *, question):
    responses = ['Yes', 'No', 'Maybe So']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command()
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit = amount)

@client.command()
async def emoji(ctx, emoji):
    await ctx.send(f':{emoji}:')

client.run('ODg3MDk3NjQ4MzU0NTgyNTk5.YT_MEA.-tUzXoGts8uC7_CZysxRboyPUrw')