import discord, traceback, json
from discord.ext import commands

from src import env, bridge, test, webhooks
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

def Embed(description):
  return discord.Embed(
    # color = 0xffffff,
    description = description,
  )

@bot.command()
async def status(context):
  if bridge.status():
    await context.send(embed = Embed(':green_circle: Active'))
  else:
    await context.send(embed = Embed(':red_circle: Inactive'))

@bot.command()
async def version(context):
  await context.send(embed = Embed(bridge.version()))

@bot.command()
@commands.has_any_role('admin', 'dev')
async def start(context):
  await context.send(embed = Embed(bridge.start()))
  await bot.change_presence(activity = active)

@bot.command()
@commands.has_any_role('admin', 'dev')
async def stop(context):
  await context.send(embed = Embed(bridge.stop()))
  await bot.change_presence(activity = inactive)

@bot.command()
@commands.has_any_role('admin', 'dev')
async def restart(context):
  await context.send(embed = Embed(bridge.restart()))
  await bot.change_presence(activity = active)

msg = 'Error: No matches found.\nPossible values: issue, reddit or release.'

@bot.command()
@commands.has_any_role('admin', 'dev')
async def payload(context, name):
  webhook = {
    'issue': webhooks.issues,
    'reddit': webhooks.reddit,
    'release': webhooks.releases,
  }.get(name, False)

  if webhook:
    try:
      await context.send(
        f'```json\n{json.dumps(webhook.payload, indent = 2)}```'
      )
    except:
      await context.send(embed = Embed(webhook.payload))
  else:
    await context.send(embed = Embed(msg))

@bot.command()
@commands.has_any_role('admin', 'dev')
async def resend(context, name):
  webhook = {
    'issue': webhooks.issues,
    'reddit': webhooks.reddit,
    'release': webhooks.releases,
  }.get(name, False)

  if webhook:
    webhook.send()
  else:
    await context.send(embed = Embed(msg))

@bot.command()
@commands.has_any_role('admin', 'dev')
async def send(context, name):
  webhook = {
    'issue': test.issues,
    'reddit': test.reddit,
    'release': test.releases,
  }.get(name, False)

  if webhook:
    webhook.send()
  else:
    await context.send(embed = Embed(msg))

@bot.event
async def on_command_error(context, error):
  if isinstance(error, commands.CommandNotFound):
    pass
  elif isinstance(error, commands.MissingAnyRole):
    await context.send(
      embed = Embed("You don't have permission to use this command.")
    )
  else:
    logger(''.join(
      traceback.format_exception(type(error), error, error.__traceback__)
    ))

@bot.event
async def on_ready():
  logger('Matterbot has been started.')

def init() -> None:
  bot.run(env.token['discord'])
