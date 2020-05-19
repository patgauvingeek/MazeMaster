'''The maze master both'''
import json
from discord.ext import commands

if __name__ == '__main__':
  with open('auth.json') as json_auth:
    AUTH = json.load(json_auth)
    TOKEN = AUTH['token']

  BOT = commands.Bot(command_prefix='!')

  @BOT.event
  async def on_ready():
    '''LOGGED'''
    print('Logged in as %s (%s)' % (BOT.user.name, BOT.user.id))

  @BOT.command()
  async def ping(ctx):
    '''Response to !ping'''
    await ctx.send('!pong')

  @BOT.command()
  async def go(ctx, direction: str):
    await ctx.send("you are going %s" % direction)

  BOT.run(TOKEN)
