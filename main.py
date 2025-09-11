# Discord Bot that plays audio from YouTube.
# @author: minjii1079

import discord
import os
import logging
import yt_dlp
import asyncio

from discord.ext import commands
from dotenv import load_dotenv
from discord import app_commands

# Load environment variable from .env file 
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Function to search using yt-dlp, within it's own thread to avoid any blocking
async def search_ytdlp_async(query, ytdlp_opts):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: _extract_info(query, ytdlp_opts))

# Calls yt-dlp to get the song without downloading it (indicated by download=False)
def _extract_info(query, ytdlp_opts):
    with yt_dlp.YoutubeDL(ytdlp_opts) as ytdlp:
        return ytdlp.extract_info(query, download=False)

# Create logging handler to log to discord.log
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: Bot ready, syncs commands globally
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} is now online!")

# /play command which plays a song based on user input
@bot.tree.command(name="play", description="Play a song, and add it to the queue.")
@app_commands.describe(song_query="Search query for the song to play")
async def play(interaction: discord.Interaction, song_query: str):

    # Defer response for processing time
    await interaction.response.defer()
    voice_channel = interaction.user.voice.channel

    # Check if the user is in a voice channel, otherwise return
    if not voice_channel:
        await interaction.followup.send("You need to be in a voice channel to play music.")
        return
    
    voice_client = interaction.guild.voice_client

    if not voice_client:
        voice_client = await voice_channel.connect()
    elif voice_client.channel != voice_channel:
        await voice_client.move_to(voice_channel)

    # Options for YT-DLP (best audio setting according to documentation)
    ytdlp_opts = {
        "format": "bestaudio[abr<=96]/bestaudio",
        "noplaylist": True,
        "youtube_include_dash_manifest": False,
        "youtube_include_hls_manifest": False,
    }

    # Search for the song (1st result, indicated by 'ytsearch1:')
    query = "ytsearch1: " + song_query
    results = await search_ytdlp_async(query, ytdlp_opts)
    tracks = results.get("entries", [])

    # Return if no tracks are found
    if not tracks:
        await interaction.followup.send("No results found.")
        return
    
    # Play the first track, extract URL and title
    first_track = tracks[0]
    stream_url = first_track.get("url")
    title = first_track.get("title", "Untitled")

    # Debugging information
    #print("Track info:", first_track)
    #print("Stream URL:", stream_url)

    # Options for FFMPEG
    ffmpeg_opts = {
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        "options": "-vn",
        "executable": "C:\\Users\\Kevin\\Python Projects\\Discord Bot Project\\bin\\ffmpeg.exe",
    }

    # Create audio source with added volume control (Default volume is 50%)
    ffmpeg_source = discord.FFmpegPCMAudio(stream_url, **ffmpeg_opts)
    source = discord.PCMVolumeTransformer(ffmpeg_source, volume=0.5)

    # Play the audio through the voice client
    voice_client.play(source)

bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)