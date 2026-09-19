# FILE BOT CHÍNH - KHÔNG CHẠY ĐƯỢC TRÊN VERCEL, PHẢI HOST TRÊN RENDER/RAILWAY
import discord
from discord.ext import commands
import asyncio
import os
import yt_dlp
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("PREFIX", "!")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

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
    'source_address': '0.0.0.0',
}
ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data: data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

queues = {}
@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")

@bot.command(name="join")
async def join(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
        await ctx.send(f"Đã join {ctx.author.voice.channel.name}")

@bot.command(name="play", aliases=["p"])
async def play(ctx, *, query: str):
    if not ctx.voice_client:
        if ctx.author.voice: await ctx.author.voice.channel.connect()
        else: await ctx.send("Vào kênh thoại trước!"); return
    if not query.startswith("http"): query = f"ytsearch:{query}"
    player = await YTDLSource.from_url(query, loop=bot.loop, stream=True)
    guild_id = ctx.guild.id
    if guild_id not in queues: queues[guild_id] = []
    if ctx.voice_client.is_playing():
        queues[guild_id].append((player, ctx))
        await ctx.send(f"Đã thêm: {player.title}")
    else:
        ctx.voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop))
        await ctx.send(f"🎶 Đang phát: {player.title}")

async def play_next(ctx):
    guild_id = ctx.guild.id
    if queues.get(guild_id):
        player, original_ctx = queues[guild_id].pop(0)
        ctx.voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop))
        await original_ctx.send(f"Đang phát tiếp: {player.title}")

@bot.command(name="leave", aliases=["stop"])
async def leave(ctx):
    if ctx.voice_client:
        queues[ctx.guild.id] = []
        await ctx.voice_client.disconnect()
        await ctx.send("Đã thoát")

if TOKEN: bot.run(TOKEN)
else: print("Thiếu DISCORD_TOKEN trong .env")
