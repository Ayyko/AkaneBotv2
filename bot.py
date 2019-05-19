import discord
from discord.ext import commands
import json
import logging
import sys
import cogs
import traceback

# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.StreamHandler(stream=sys.stdout)
# logger.addHandler(handler)

description = '''Ako#0408 | <@132694825454665728>'s mostly personal bot.
I can do things, and maybe stuff.
I'm open source: https://github.com/Ayyko/AkaneBot
I'm made using discord.py v.''' + discord.__version__


async def get_pre(self, message):
    ret = commands.when_mentioned(self, message) + ["Akane ", "akane "]
    if message.guild and message.guild.id == 169056767219597312:        # ML server
        ret += ["!", "?"]
    return ret

bot = commands.Bot(command_prefix=get_pre, description=description, dm_help=True)

with open("bot_shit.json", "r") as b:
    bot.shit = json.load(b)

startup_extensions = ["cogs.MuvLuv", "cogs.owner", "cogs.nsa"]


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
            traceback.print_exc()


@bot.command()
@commands.cooldown(1, 60, commands.cooldowns.BucketType.channel)
async def about(ctx):
    """Information about the bot (same as shown at the top of help)"""
    await ctx.send(description)

bot.run(bot.shit['token'])

with open("bot_shit.json", "w") as b:
    a = json.dumps(bot.shit)
    b.write(a)
