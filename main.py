# import libraries
import os
import discord
from keep_alive import keep_alive
from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound, MissingPermissions, MissingRequiredArgument
from datetime import datetime

# Declaration on bot's client

client = commands.Bot(command_prefix='$')
client.remove_command('help')

# Event listening for when bot is active

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  print('Bot is ready.')
  f = open("log.txt", "a")
  now = datetime.now()
  current_time = now.strftime("%m/%d/%Y, %H:%M:%S")
  f.write(f"{current_time} : Bot is now active \n")
  f.close()

# Event listening for member leaving

@client.event
async def on_member_join(member):
  print(f'{member} has joined a server.')

# Event listening for member leaving

@client.event
async def on_member_remove(member):
  print(f'{member} has left a server.')

# For handling unknown commands

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.channel.send("Sorry, this command was not found!")

# The following is for commands

# Help command
  # Format: $help

@client.command()
async def help(ctx):
  await ctx.message.channel.send('''
  List of commands:
  - $help (this one) - Shows help menu
  - $hello - Says Hello! (for lonely people)
  - $ban [user] - Ban user
  - $kick [user] - kick user
  - $clear [amount] - Clears specified amount of messages
  If you want more function, please contact us at 765-922-0651''')

# Hello command
# Format: $hello

@client.command()
async def hello(ctx):
  await ctx.message.channel.send('Hello!')

# Ban command
# Format: $ban [user]

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
  await member.ban(reason="")
  f = open("log.txt", "a")
  now = datetime.now()

  current_time = now.strftime("%m/%d/%Y, %H:%M:%S")
  f.write(f"{current_time} : {ctx.author} banned {member} \n")
  f.close()

@ban.error
async def ban_error(ctx, error):
  if isinstance(error, MissingRequiredArgument):
    await ctx.channel.send("Format: $ban [user]")
  elif isinstance(error, MissingPermissions):
    await ctx.channel.send("I'm sorry, you do not have sufficient permission!")

# Kick command
# Format: $kick [user]

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
  await member.kick(reason="")
  f = open("log.txt", "a")
  now = datetime.now()

  current_time = now.strftime("%m/%d/%Y, %H:%M:%S")
  f.write(f"{current_time} : {ctx.author} kicked {member} \n")
  f.close()

@kick.error
async def kick_error(ctx, error):
  if isinstance(error, MissingRequiredArgument):
    await ctx.channel.send("Format: $kick [user]")
  elif isinstance(error, MissingPermissions):
    await ctx.channel.send("I'm sorry, you do not have sufficient permission!")

# Purge command
# Format: $purge [amount]

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, arg):
  print(arg)
  await ctx.message.channel.purge(limit=int(arg)+1)
  f = open("log.txt", "a")
  now = datetime.now()

  current_time = now.strftime("%m/%d/%Y, %H:%M:%S")
  f.write(f"{current_time} : {ctx.author} cleared {int(arg)} message(s) \n")
  f.close()

@clear.error
async def clear_error(ctx, error):
  if isinstance(error, MissingRequiredArgument):
    await ctx.channel.send("Format: $clear [amount]")
  elif isinstance(error, MissingPermissions):
    await ctx.channel.send("I'm sorry, you do not have sufficient permission!")

keep_alive()
client.run(os.environ['TOKEN'])
