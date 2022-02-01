from discord import Intents
from discord.ext.commands import Bot, Cog, CommandNotFound, MissingPermissions
import config
import requests
import datetime

from commands import Commands


class DiscordBot(Bot):

    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            await ctx.reply('I do not know that command?!',mention_author=False)
    @Cog.listener()
    async def on_permissions_error(self, ctx, error):
        if isinstance(error,MissingPermissions):
            await ctx.reply('MissingPermission!', mention_author=False)




if __name__ == "__main__":
    intents = Intents.default()
    intents.members = True
    bot = DiscordBot(command_prefix="T9$", intents=intents, help_command=None)
    bot.add_cog(Commands(bot))
    bot.run(config.TOKEN)
