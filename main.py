import discord
from discord.ext import commands
import os
import openai
import requests
from requests.structures import CaseInsensitiveDict
import wikipedia
import youtube_dl
import asyncio
import urllib.parse
from bs4 import BeautifulSoup
import json

openai.api_key = "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"
BOT_TOKEN = "MTA3MzY0NjkxODkwOTA0Mjc0OA.GYsEVb.7KjNfPUFytTLl7312f-Xb8iA1zDr2B0tO54CQ0"
CHANNEL_ID = 1030510177503420547


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
client = discord.Client(intents=discord.Intents.all())


async def send(text):
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(text)


@bot.event
async def on_ready():
    print("Hello everyone")
    botchanell = bot.get_channel(CHANNEL_ID)


@bot.command()
async def ping(ctx):
    await ctx.send("status = active")


@bot.command()
async def add(ctx, num1, num2):
    result = int(num1) + int(num2)
    await ctx.send(result)


@bot.command()
@commands.has_permissions(kick_members=True, ban_members=True,
                          manage_roles=True)  # Setting permissions that a user should have to execute this command.
async def ban(ctx, member: discord.Member, *, reason=None):
    if member.guild_permissions.administrator:  # To check if the member we are trying to mute is an admin or not.
        await ctx.channel.send(
            f'Hi {ctx.author.name}! The member you aer trying to mute is a server Administrator.'
            f' Please don\'t try this on them else they can get angry! :person_shrugging:')

    else:
        if reason is None:  # If the moderator did not enter any reason.
            # This command sends DM to the user about the BAN!
            await member.send(
                f'Hi {member.name}! You have been banned from {ctx.channel.guild.name}'
                f'. You must have done something wrong. VERY BAD! :angry: :triumph: \n \nReason: Not Specified')
            # This command sends message in the channel for confirming BAN!
            await ctx.channel.send(
                f'Hi {ctx.author.name}! {member.name}'
                f' has been banner succesfully from this server! \n \nReason: Not Specified')
            await member.ban()  # Bans the member.

        else:  # If the moderator entered a reason.
            # This command sends DM to the user about the BAN!
            await member.send(
                f'Hi {member.name}! You have been banned from {ctx.channel.guild.name}'
                f'. You must have done something wrong. VERY BAD! :angry: :triumph: \n \nReason: {reason}')
            # This command sends message in the channel for confirming BAN!
            await ctx.channel.send(
                f'Hi '
                f'{ctx.author.name}! {member.name} has been banner succesfully from this server! \n \nReason: {reason}')
            await member.ban()  # Bans the member.


@bot.command()
async def lock_channel(ctx):
    target_channel = client.get_channel()
    overwrite = discord.PermissionOverwrite()
    await target_channel.set_permissions(target_channel.guild.default_role, overwrite=overwrite)


@bot.command()
async def unlock_channel(ctx):
    target_channel = client.get_channel()
    overwrite = discord.PermissionOverwrite()
    await target_channel.set_permissions(target_channel.guild.default_role, overwrite=overwrite)


@bot.command()
async def server(ctx):
    user_id = ctx.author.id
    user = client.get_user(int(user_id))

    dm_channel = await ctx.author.create_dm()
    await dm_channel.send('This server is about an ark server named Still Chill '
                          'whose owners are Hyplayer(epro) and iXone(germ)')


@bot.command()
async def daily(ctx):
        user_id = ctx.author.id
        coins = 0

        # Construct the filename for the user's coins file
        filename = f"{ctx.author.name.lower()}_coins.txt"

        # Read the current coins value from the file, if it exists
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                coins = int(f.read())

        # Add 100 coins to the current value
        coins += 100

        # Save the updated value back to the file
        with open(filename, 'w') as f:
            f.write(str(coins))

        # Send a message back to the user confirming the addition of coins
        await ctx.channel.send(f"Added 100 coins to your account, {ctx.author.mention}! You now have {coins} coins.")


@bot.command(name='coins', category='economy')
async def coins(ctx):
    # Construct the filename for the user's coins file
    filename = f"{ctx.author.name.lower()}_coins.txt"
    user_id = ctx.author.id
    coins = 0

    # Read the current coins value from the file, if it exists
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            coins = int(f.read())

        # Send a message back to the user with their current coin balance
        await ctx.channel.send(f"You currently have {coins} coins, {ctx.author.mention}!")
    else:
        # If the user doesn't have a coins file yet, send an error message
        await ctx.channel.send(f"You don't have any coins yet, {ctx.author.mention}!")


@bot.command(name='buy', category='economy')
async def buy(ctx, item: str):
    # Get the user's current coin balance
    filename = f"{ctx.author.name.lower()}_coins.txt"
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            coins = int(f.read())
    else:
        coins = 0

    # Handle the purchase of VIP
    if item.lower() == 'vip':
        if coins >= 1000:
            # Subtract the cost of VIP from the user's balance
            coins -= 1000

            # Save the updated balance to the file
            with open(filename, 'w') as f:
                f.write(str(coins))

            # Add the VIP role to the user
            role = discord.utils.get(ctx.guild.roles, name='VIP')
            await ctx.author.add_roles(role)

            await ctx.send(f"Congratulations, {ctx.author.mention}! You are now a VIP member and have been charged 1000 coins. You have {coins} coins left.")
        else:
            await ctx.send(f"Sorry, {ctx.author.mention}! You don't have enough coins to purchase VIP. You need 1000 coins, but you only have {coins} coins.")
    else:
        await ctx.send(f"Invalid purchase request, {ctx.author.mention}! The only item available for purchase is VIP.")


@bot.command(name='TakeRole', category='Administration')
@commands.has_permissions(administrator=True)
async def takeRole(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    await ctx.send(f"{role.mention} has been removed from {user.mention}")


@bot.command(name='Clear', category='Administration')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    """
    Clears a specified amount of messages from the current channel.
    Only users with the 'Manage Messages' permission can use this command.
    Usage: !clear <amount>
    """
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f"Cleared {amount} messages.")

@bot.command()
async def killmyself(ctx):
    await ctx.send("ok you lost all your coins")
    coins = 0

    # Construct the filename for the user's coins file
    filename = f"{ctx.author.name.lower()}_coins.txt"

    # Read the current coins value from the file, if it exists
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            coins = int(f.read())
    coins = 0

    # Save the updated value back to the file
    with open(filename, 'w') as f:
        f.write(str(coins))
@bot.command()
async def helpme(ctx):
    # Define the list of commands and their explanations
    commands = [
        {
            "name": "ping",
            "description": "Check if the bot is active."
        },
        {
            "name": "add",
            "description": "Add two numbers. Example usage: !add 5 7"
        },
        {
            "name": "ban",
            "description": "Ban a member from the server. Example usage: !ban @user 'reason'"
        },
        {
            "name": "lock_channel",
            "description": "Lock a channel to prevent members from sending messages. Example usage: !lock_channel"
        },
        {
            "name": "unlock_channel",
            "description": "Unlock a previously locked channel to allow members to send messages again. Example usage: !unlock_channel"
        },
        {
            "name": "server",
            "description": "Get information about the server. Example usage: !server"
        },
        {
            "name": "daily",
            "description": "Get 100 coins daily. Example usage: !daily"
        },
        {
            "name": "coins",
            "description": "Check your coin balance. Example usage: !coins"
        },
        {
            "name": "buy",
            "description": "Buy an item with your coins. Example usage: !buy vip"
        },
        {
            "name": "Dall",
            "description": "Ask Dall-e to make a picture"
        }
    ]

    # Create the help message by iterating through the list of commands
    help_message = "**Available commands:**\n"
    for cmd in commands:
        help_message += f"\n**!{cmd['name']}**: {cmd['description']}"

    # Send the help message to the user's DMs
    await ctx.author.send(help_message)

    # Send a confirmation message in the server channel
    await ctx.send(f"{ctx.author.mention}, check your DMs for a list of available commands!")
@bot.command()
async def Dall(ctx,*, query):
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {openai.api_key}"

    data = """
    {
        """
    data += f'"model": "image-alpha-001",'
    data += f'"prompt": "{query}",'
    data += """
        "num_images":1,
        "size":"512x512",
        "response_format":"url"
    }
    """

    resp = requests.post("https://api.openai.com/v1/images/generations", headers=headers, data=data)

    if resp.status_code != 200:
        raise ValueError("Failed to generate image: %s" % resp.text)

    response_text = resp.json()
    image_url = response_text['data'][0]['url']
    await ctx.send(image_url)
    print(image_url)
@bot.command()
async def wiki(message):
        query = message.content[6:]
        try:
            result = wikipedia.summary(query, sentences=2)
            await message.channel.send(result)
        except wikipedia.exceptions.PageError:
            await message.channel.send(f"Sorry, I couldn't find any Wikipedia pages for {query}.")
        except wikipedia.exceptions.DisambiguationError as e:
            options = '\n'.join(e.options[:5])
            await message.channel.send(f"Sorry, I found multiple options for {query}. Please try one of the following:\n{options}")


@bot.command()
async def play(message):
    try:
        voice_channel = message.author.voice.channel
    except AttributeError:
        await message.channel.send('You must be in a voice channel to use this command')
        return
    try:
        url = message.content.split()[1]
    except IndexError:
        await message.channel.send('You must provide a YouTube URL to play')
        return
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'song.mp3',
        'noplaylist': True,
        'quiet': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_name = ydl.prepare_filename(info_dict)
    voice_client = await voice_channel.connect()
    source = discord.FFmpegPCMAudio(file_name)
    player = voice_client.play(source)
    while not player.is_done():
        await asyncio.sleep(1)
    player.stop()
    voice_client.stop()
    await voice_client.disconnect()


@bot.command()
async def image(ctx, *, search_query):
    query = urllib.parse.quote(search_query)
    url = f"https://www.google.com/search?q={query}&tbm=isch"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    images = soup.find_all("img")
    await ctx.send(images[1].get("src"))


@bot.command()
async def joke(ctx):
    response = requests.get("https://v2.jokeapi.dev/joke/Any")
    joke_json = json.loads(response.text)
    if joke_json['type'] == 'single':
        await ctx.send(joke_json['joke'])
    else:
        await ctx.send(f"{joke_json['setup']}\n{joke_json['delivery']}")
# Replace YOUR_CHANNEL_ID with the ID of the channel you want to send messages to
YOUR_CHANNEL_ID = 1030508028140736543
LOCKDOWN_CHANNEL_ID = YOUR_CHANNEL_ID

EXCLUDE_CHANNELS = [1030073510581784586, 1037031777400795136, 1039868287263191061]


@bot.command()
@commands.has_permissions(administrator=True)
async def lock(ctx):
    lockdown_channel = bot.get_channel(LOCKDOWN_CHANNEL_ID)
    for channel in ctx.guild.channels:
        if channel.id not in EXCLUDE_CHANNELS:
            await ctx.send(f"{channel} has been locked")
            await channel.set_permissions(ctx.guild.default_role, read_messages=False)
    await lockdown_channel.send('Server locked down.')


@bot.command()
@commands.has_permissions(administrator=True)
async def unlock(ctx):
    lockdown_channel = bot.get_channel(LOCKDOWN_CHANNEL_ID)
    for channel in ctx.guild.channels:
        if channel.id not in EXCLUDE_CHANNELS:
            await ctx.send(f"{channel} has been unlocked")
            await channel.set_permissions(ctx.guild.default_role, read_messages=True)
    await lockdown_channel.send('Server unlocked. All channels are now visible.')


bot.run(BOT_TOKEN)
