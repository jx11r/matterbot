import discord, traceback, time
from discord.ext import commands

from src import env, bridge
from src.utils import logger

active = discord.Activity(
  type = discord.ActivityType.listening,
  name = 'Telegram/IRC'
)

inactive = discord.Activity(
  type = discord.ActivityType.listening,
  name = '!start',
)

bot = commands.Bot(
  command_prefix = '!',
  help_command = None,
  activity = active,
  status = discord.Status.online,
)

@bot.command()
async def status(context):
  if bridge.status():
    await context.send('Bridge: active.')
  else:
    await context.send('Bridge: inactive.')

@bot.command()
async def version(context):
  await context.send(bridge.version())

@bot.command()
@commands.has_any_role('admin', 'dev')
async def start(context):
  await context.send(bridge.start())
  await bot.change_presence(activity = active)

@bot.command()
@commands.has_any_role('admin', 'dev')
async def stop(context):
  await context.send(bridge.stop())
  await bot.change_presence(activity = inactive)

@bot.command()
@commands.has_any_role('admin', 'dev')
async def restart(context):
  await context.send(bridge.restart())
  await bot.change_presence(activity = active)

@bot.event
async def on_command_error(context, error):
  if isinstance(error, commands.CommandNotFound):
    pass
  elif isinstance(error, commands.MissingAnyRole):
    await context.send("You don't have permission to use this command.")
  else:
    print(''.join(
      traceback.format_exception(type(error), error, error.__traceback__)
    ))

@bot.event
async def on_ready():
  logger('Matterbot has been started.')

def init() -> None:
  time.sleep(15)
  bot.run(env.token['discord'])
