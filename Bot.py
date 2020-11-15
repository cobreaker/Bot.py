import discord
import  math, time
from discord.ext import commands
from discord.ext.commands import Bot
import typing
from discord.utils import get
import asyncio
import shutil
import os
import json
import random
from discord import Game
from os import  system
import  youtube_dl
from better_profanity import profanity
profanity.load_censor_words_from_file("./profanity.txt")
client = discord.Client()
Clientdiscord = discord.Client()
bot = commands.Bot(command_prefix='#')
bot = Bot(command_prefix='#')
messages= joined = 0



async def update_stats():
    await bot.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {int(time.time())}, Message: {messages} , Members joined: {joined} , message ctx:{str()} \n")
            messages = 0
            joined = 0
            await asyncio.sleep(100)
        except Exception as e:
            print(e)
            await asyncio.sleep(100)

@bot.command()
async def kick(ctx, user : discord.Member):
    mbed = discord.Embed(
        title='❗ Member Kick',
        description=f"{user} has been Kicked"
    )
    if ctx.author.guild_permissions.kick_members:
        await ctx.send(embed = mbed)
        await user.kick()
@bot.command()
async  def ban(ctx, user : discord.Member):
    guild = ctx.guild
    mbed = discord.Embed(
        title = '❗ Member Ban',
        description= f"{user} has been banned"
    )
    if ctx.author.guild_permissions.ban_members:
        await ctx.send(embed = mbed)
        await guild.ban(user=user)

@bot.command()
async  def unban(ctx, user : discord.Member):
    guild = ctx.guild
    mbed = discord.Embed(
        title = 'Members',
        description= f"{user} has been unbanned"
    )
    if ctx.author.guild_permissions.ban_members:
        await ctx.send(embed = mbed)
        await guild.unban(user=user)


@bot.command(invoke_without_command=True, aliases=['Help'])
async def helpp(ctx):
    mbed = discord.Embed(
        title= "Help" ,
        description= "This command show the description of other commands"
    )
    mbed.add_field(name="Clear messages", value="#clear")
    mbed.add_field(name="Upper case converter", value="#up")
    mbed.add_field(name="Bot(join channel)", value="#join")
    mbed.add_field(name="Bot(leave channel)", value="#leave")
    mbed.add_field(name="Bot(play music)", value="#play")
    mbed.add_field(name="Bot(queue music)", value="#queue")
    mbed.add_field(name="Bot(stop music)", value="#stop")
    mbed.add_field(name="Bot(skip music)", value="#next")
    await ctx.send(embed = mbed)




@bot.command(pass_context=True, aliases=['info', 'in32'])
async def server_info(ctx):
    mbed = discord.Embed(
        color = discord.Color(0xffff),
        title = f"{ctx.guild.name}"
    )
    mbed.set_thumbnail(url=f"{ctx.guild.icon_url}")
    mbed.add_field(name='Region', value = f"{ctx.guild.region}")
    mbed.add_field(name='Member Count', value=f"{ctx.guild.member_count}")
    mbed.set_footer(icon_url=f"{ctx.guild.icon_url}", text=f"Guild ID: {ctx.guild.id}")
    await ctx.send(embed=mbed)
@bot.command()
async def avatar(ctx, user : discord.Member):
    mbed = discord.Embed(
        color=discord.Color(0xffff),
        title=f"{user}"
    )
    mbed.set_image(url=f"{user.avatar_url}")
    await ctx.send(embed=mbed)


@bot.command()
async def addrole(ctx, role : discord.Role, user : discord.Member):
    if ctx.author.guild_permissions.administrator:
        await user.add_roles(role)
        await ctx.send(f"Successfully Given {role.mention} to {user.mention}")

@bot.command()
async def remove(ctx, role : discord.Role, user : discord.Member):
    if ctx.author.guild_permissions.administrator:
        await user.remove_roles(role)
        await ctx.send(f"Successfully Removed {role.mention} From {user.mention}")

@bot.command()
async def repeat(ctx, * , arg):
    await ctx.send(arg)


@bot.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))


def to_upper(argument):
    return argument.upper()


@bot.command()
async def up(ctx, *, content: to_upper):
    await ctx.send(content)

@bot.command()
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)


@bot.command(pass_context=True)
async def join(ctx):
   global voice
   channel =ctx.message.author.voice.channel
   voice = get(bot.voice_clients, guild=ctx.guild)
   if voice and voice.is_connected():
       await voice.move_to(channel)
   else:
       voice = await channel.connect()




@bot.command(pass_context=True)
async def leave(ctx):
   global voice
   channel =ctx.message.author.voice.channel
   voice = get(bot.voice_clients, guild=ctx.guild)
   if voice and voice.is_connected():
       await voice.disconnect()
       print(f"Bot has left {channel}")
       await ctx.send(f"Bot has left  {channel}")
   else:
       print("Bot was told to leave voice channel")
       await ctx.send("Bot is not connected to a channel")

@bot.command()
async def play(ctx, url:str):
    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No More Queued songs")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, Playing next song")
                print(f"Songs still in queue : {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07
            else:
                queues.clear()
                return
        else:
            queues.clear()
            print("No songs were queued before the ending of the last song\n")











    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old file")
    except PermissionError:
        print("Trying to delete song file")
        await ctx.send("Error: Music playing")
        return


    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed old song file")
            shutil.rmtree(Queue_folder)
    except:
        print("No old Queue folder")


    await ctx.send("Getting evrey thing ready")

    voice = get(bot.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(id)s.%(ext)s',  # name the file the ID of the video
        'noplaylist': True,
        'nocheckcertificate': True,
        'proxy': "",
        'addmetadata': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed file {file}")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    await ctx.send(f"Playing Song")
    print("Playing")


@bot.command(pass_context=True)
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music Paused")
        voice.pause()
        await  ctx.send("Music Paused")
    else:
        print("Music Not Playing")
        await ctx.send("Music Not playing")
@bot.command(pass_context=True)
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Music Resumed")
        voice.resume()
        await ctx.send("Resumed Music")
    else:
        print("Music is not Paused")
        await ctx.send("Music is not Paused")

@bot.command(pass_context=True)
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    queues.clear()
    queue_infile = os.path.isdir("./Queue")
    if queue_infile is True:
        shutil.rmtree("./Queue")


    if voice and voice.is_playing():
        print("Music stoped")
        voice.stop()
        await ctx.send("Music stoped")
    else:
        print("No Music is playing")
        await ctx.send("No Music is playing ")
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

queues = {}
@bot.command()
async def queue(ctx, url:str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")

    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num +=1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num +=1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue")  + f"\song{q_num}.%(ext)s")
    ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl': queue_path,  # name the file the ID of the video
            'noplaylist': True,
            'nocheckcertificate': True,
            'proxy': "",
            'addmetadata': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now")
        ydl.download([url])

    await ctx.send("Adding song" + str(q_num) + "to the queue")
    print("song added to the queue")




@bot.command(pass_context=True)
async def next(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)




    if voice and voice.is_playing():
        print("playing next song")
        voice.stop()
        await ctx.send("Next song")
    else:
        print("No Music is playing")
        await ctx.send("No Music is playing ")







@bot.event
async def on_message(message):







    global messages
    messages += 1

    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if not message.author.bot:
        if profanity.contains_profanity(message.content):
            await message.delete()
            await message.channel.send("You can't use that word")

    guild = message.guild
    if guild:
        path = "chatlogs/{}.txt".format(guild.id)
        with open(path, 'a+') as f:
            print("{0.author.name} : {0.content}".format(message), file=f)














    await bot.process_commands(message)




@bot.event
async def on_member_join(member):

    global joined
    joined += 1

    for channel in member.server.channels:
        if str(channel) == "general":
            await bot.send_message(f"""Welcome to the server {member.mention}""")















bot.loop.create_task(update_stats())
bot.run(os.environ['token'])
