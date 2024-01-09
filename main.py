import discord
import tokenbot
import asyncio
from discord.ext import commands


from help_cog import help_cog
from music_cog import music_cog
from event_cog import event_cog
from comands_cog import comands_cog

Token = tokenbot.token_key()
intents = discord.Intents.all()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='?', intents=intents)
bot.remove_command('help')


async def main():
    async with bot:
        await bot.add_cog(event_cog(bot))
        await bot.add_cog(help_cog(bot))
        await bot.add_cog(music_cog(bot))
        await bot.add_cog(comands_cog(bot))
        await bot.start(Token)


asyncio.run(main())
