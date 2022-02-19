from tempfile import _TemporaryFileWrapper
import discord
from discord.ext import commands
import asyncio
import os
import youtube_dl


youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

queue = []
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
        global queue
        queue.append(url)
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        
        if voice.is_playing():
            await ctx.send('Song has been added to queue')

        if ctx.author.voice is None:
            await ctx.send('You are not connected to a voice channel')
        channel = ctx.author.voice.channel
        if voice is None:
            await channel.connect()
        else: 
            await voice.move_to(channel)

        async with ctx.typing():
            player = await YTDLSource.from_url(queue[0], loop=self.client.loop)
            voice.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('**Now playing:** {}'.format(player.title))
        del(queue[0])

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

    @commands.command()
    async def queue(self, ctx):
        await ctx.send(f'Your queue is now `{queue}!`')

    @commands.command()
    async def remove(ctx, number):
        global queue

        try:
            del(queue[int(number)])
            await ctx.send(f'Your queue is now `{queue}!`')
    
        except:
            await ctx.send('Your queue is either **empty** or the index is **out of range**')
        



def setup(client):
    client.add_cog(Youtube(client))
    
