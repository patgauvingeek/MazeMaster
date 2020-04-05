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
  async def ping():
    '''Response to !ping'''
    await BOT.say('!pong')

  @BOT.command()
  async def go(direction: str):
    await BOT.say("you are going %s" % direction)

  BOT.run(TOKEN)
