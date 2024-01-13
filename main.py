import discord
import tokenbot
import asyncio
import wavelink
from discord.ext import commands


from help_cog import help_cog
from music_cog import music_cog
from event_cog import event_cog
from comands_cog import comands_cog
from wave_cog import wave_cog

Token = tokenbot.token_key()
intents = discord.Intents.all()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='?', intents=intents)
bot.remove_command('help')

@bot.listen()
async def on_ready():
     bot.loop.create_task(node_connect())

async def main():
    async with bot:
        await bot.add_cog(event_cog(bot))
        await bot.add_cog(help_cog(bot))
        await bot.add_cog(wave_cog(bot))
        #await bot.add_cog(music_cog(bot))
        await bot.add_cog(comands_cog(bot))
        await bot.start(Token)
async def node_connect():
    await bot.wait_until_ready()
    # 2 nodes
    node = wavelink.Node(uri='85.88.163.80:3128', password="saher.inzeworld.com")
    node2 = wavelink.Node(uri='eu-lavalink.lexnet.cc:2333', password="lexn3tl@val!nk")
    await wavelink.NodePool.connect(client=bot, nodes=[node, node2])

asyncio.run(main())
