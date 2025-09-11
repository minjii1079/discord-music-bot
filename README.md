# 🎵 Discord Music Bot!
A short project where I made a simple music bot for my Discord server. It runs locally but can be hosted to run 24/7.
Once online and invited to your server, it will take the command `/play "song name/url here"`. The current build is limited
to playing only one song at a time, but I'd like to add a queue system to expand its functionality at a later date. **NOTE:** 
There is currently no token in the `DISCORD_TOKEN` environment variable, as leaving it would be a security vulnerability.

# ✏️ Creation Process
**Tech used:** Python, Discord API, discord.py API wrapper, FFMPEG, yt_dlp

I started by doing some research into Discord bots to find out about the tools I'd need. By using the discord.py API wrapper, I could implement the Discord API and do all the coding in Python.
I read some suggestions about yt_dlp, as it can search for and extract the URL for YouTube videos. FFMPEG was also going to be
important as I needed a way to take the URL and create an audio source that Discord can use. Now I had to decide what
*type* of bot I wanted to make. On Discord, I've primarily used music bots and used to think about making my own since
they used to break down quite frequently a few years ago (it was common for servers I was in to have multiple music
bots at once). With this in mind, I decided to create a music bot.

Despite conducting some research on what I'd need for this project, I still had relatively little knowledge on this topic.
Luckily, there is a lot of good documentation on discord.py's website that helps you get started pretty quickly,
and I was able to get something running within a few hours. The code itself isn't hard to understand;
Most of the effort lies in getting the different tech to interact together without bugs
(I talk about them in the next section). Discord API's website had lots of examples that taught me about intents, and which ones
I'd need for this project.

This project was also the first time I worked with FFMPEG and yt_dlp. yt_dlp is a command-line audio/video
downloader that I used to retrieve the requested music while making sure to disable downloading, as I would only
want the song to be played once. It has been set up to only take the first search result, as that is typically
the desired output. Once the URL is retrieved, a source is then created where the URL is passed through
`FfmpegOpusAudio` for processing, along with the specified options. This source is called by Discord and plays
through the voice client, which is how you hear the song coming out of the bot's "mic". The program reaches completion after
finally logging to the discord.log file. Once the song is finished, a new one can be requested with the same command
as mentioned above.

# ⚙️ Debugging and Optimizations
A major struggle for me was getting the bot to send the YouTube URL to FFMPEG. I was trying all sorts of things, like adding
debugging statements, changing variable and function names, re-reading documentation, searching on YouTube, and surfing
random forums and Reddit threads. The problem turned out to be pretty simple: a typo in the executable file path for FFMPEG.exe.
That was it.

# 📝 Lessons Learned
The obvious one is to check the basic stuff before worrying about anything else when something goes wrong. I obviously didn't
follow a process when trying to debug my code, which resulted in a lot of wasted time and unnecessary hassle. On a more positive note, however,
I was able to finally create a discord music bot that younger me was too lazy to do. I worked with several technologies for the first time and
gained more experience with version control (git) and project development. My next project is gonna be much more ambitious, so keep an eye out for that.



