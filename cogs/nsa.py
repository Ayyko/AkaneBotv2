import aiohttp
from discord.ext import commands


class NSA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_chan = self.bot.get_channel(291681699043999754)
        self.blacklist = bot.shit["blacklist"]

    async def on_message_delete(self, message):
        if self.bot.shit["testing"]:
            return
        if not message.content:
            return
        if message.channel.id in self.blacklist:
            return
        if len(message.clean_content) > 1900:
            async with aiohttp.ClientSession() as session:
                async with session.post("https://hastebin.com/documents", data=message.clean_content) as r:
                    resp = await r.json()
                    try:
                        hb_url = "https://hastebin.com/{}".format(resp["key"])
                    except KeyError:
                        hb_url = "There was an error uploading to hb: {}".format(resp)
            await self.log_chan.send("{} in #{} ({}) deleted {}".format(str(message.author), message.channel.name, message.guild.name, hb_url))
            return
        await self.log_chan.send("{} in #{} ({}) deleted:\n```{}```".format(str(message.author), message.channel.name, message.guild.name, message.clean_content))

    async def on_message_edit(self, before, after):
        if self.bot.shit["testing"]:
            return
        if not after.content:
            return
        if after.content == before.content:
            return
        if after.channel.id in self.blacklist:
            return
        ret = "before:\n{}\nafter:\n{}".format(before.clean_content, after.clean_content)
        if len(ret) > 1900:
            async with aiohttp.ClientSession() as session:
                async with session.post("https://hastebin.com/documents", data=ret) as r:
                    resp = await r.json()
                    try:
                        hb_url = "https://hastebin.com/{}".format(resp["key"])
                    except KeyError:
                        hb_url = "There was an error uploading to hb: {}".format(resp)
            await self.log_chan.send("{} in #{} ({}) edited {}".format(str(after.author), after.channel.name, after.guild.name, hb_url))
            return
        await self.log_chan.send("{} in #{} ({}) edited:\n```{}```".format(str(after.author), after.channel.name, after.guild.name, ret))


def setup(bot):
    bot.add_cog(NSA(bot))
