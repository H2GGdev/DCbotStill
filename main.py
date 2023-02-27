import discord
from discord.ext import commands
import os

BOT_TOKEN = "MTA3MzY0NjkxODkwOTA0Mjc0OA.GYsEVb.7KjNfPUFytTLl7312f-Xb8iA1zDr2B0tO54CQ0"
CHANNEL_ID = 1030510177503420547


bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())
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
async def add(ctx, num1,num2):
    result = int(num1) + int(num2)
    await ctx.send(result)
@bot.command()
@commands.has_permissions(kick_members=True, ban_members=True,
                          manage_roles=True)  # Setting permissions that a user should have to execute this command.
async def ban(ctx, member: discord.Member, *, reason=None):
    if member.guild_permissions.administrator:  # To check if the member we are trying to mute is an admin or not.
        await ctx.channel.send(
            f'Hi {ctx.author.name}! The member you aer trying to mute is a server Administrator. Please don\'t try this on them else they can get angry! :person_shrugging:')

    else:
        if reason is None:  # If the moderator did not enter any reason.
            # This command sends DM to the user about the BAN!
            await member.send(
                f'Hi {member.name}! You have been banned from {ctx.channel.guild.name}. You must have done something wrong. VERY BAD! :angry: :triumph: \n \nReason: Not Specified')
            # This command sends message in the channel for confirming BAN!
            await ctx.channel.send(
                f'Hi {ctx.author.name}! {member.name} has been banner succesfully from this server! \n \nReason: Not Specified')
            await member.ban()  # Bans the member.

        else:  # If the moderator entered a reason.
            # This command sends DM to the user about the BAN!
            await member.send(
                f'Hi {member.name}! You have been banned from {ctx.channel.guild.name}. You must have done something wrong. VERY BAD! :angry: :triumph: \n \nReason: {reason}')
            # This command sends message in the channel for confirming BAN!
            await ctx.channel.send(
                f'Hi {ctx.author.name}! {member.name} has been banner succesfully from this server! \n \nReason: {reason}')
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
    await dm_channel.send('This server is about an ark server named Still Chill whose owners are Hyplayer(epro) and iXone(germ)')
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


bot.run(BOT_TOKEN)