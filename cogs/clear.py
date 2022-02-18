import discord
from discord.ext import commands
import asyncio


class Clear(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def clear(self, ctx, amount = 1):
        if amount <= 100:
            await ctx.channel.purge(limit = amount + 1)
        
    @commands.command()
    async def clearAll(self, ctx):
        messages = await ctx.channel.history(limit = 100).flatten()
        while len(messages) >= 1:
            await ctx.channel.purge(limit = 100)
            await asyncio.sleep(1)
            messages = await ctx.channel.history(limit = 100).flatten()
            await asyncio.sleep(1)
            

def setup(client):
    client.add_cog(Clear(client))

