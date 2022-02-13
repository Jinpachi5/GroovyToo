from aiohttp import ClientConnectionError
import discord
from discord.ext import commands

class Youtube(commands.Cog):
    def __init__(self, client):
        self.client = client 

def setup(client):
    client.add_cog(Youtube(client))
