from tempfile import _TemporaryFileWrapper
import discord
from discord.ext import commands
import os



activity = discord.Activity(type = discord.ActivityType.listening, name = "a song")
class Youtube(commands.Cog):
    def __init__(self, client):
        self.client = client

    activity = discord.Activity(type = discord.ActivityType.listening, name = "a song")
    #Commands
    @commands.command()
    async def ping(self, ctx):
        await self.client.change_presence(activity = activity, status = discord.Status.idle)
        await ctx.send('Pong!')

    @commands.command()
    async def play(self, ctx, url : str):
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        if ctx.author.voice is None:
            await ctx.send('You are not connected to a voice channel')
        channel = ctx.author.voice.channel
        if voice is None:
            await channel.connect()
        else: 
            await voice.move_to(channel)

    @commands.command()
    async def leave(self, ctx):
        #voice = voiceClient
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        try:
            await voice.disconnect()
        except:
            await ctx.send('You idiot! I am not in a voice channel.')

    @commands.command()
    async def pause(self, ctx):
        #voice = voiceClient
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send('No audio is playing')


    @commands.command()
    async def resume(self, ctx):
        #voice = voiceClient
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send('No audio is playing')

    @commands.command()
    async def stop(self, ctx):
        #voice = voiceClient
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        voice.stop()
        



def setup(client):
    client.add_cog(Youtube(client))
    
