import discord
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
from discord.ext import commands


class event_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'We have logged in as {self.bot.user}')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = await self.bot.fetch_channel("942067405331509308")
        url = requests.get(member.avatar)
        avatar = Image.open(BytesIO(url.content))
        avatar = avatar.resize((90, 90))
        bigAvatar = (avatar.size[0] * 3, avatar.size[1] * 3)
        mask = Image.new('L', bigAvatar, 0)
        cut = ImageDraw.Draw(mask)
        cut.ellipse((0, 0) + bigAvatar, fill=255)
        mask = mask.resize(avatar.size, Image.LANCZOS)
        avatar.putalpha(mask)

        out = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
        out.putalpha(mask)
        out.save('Images/avatar.png')

        img = Image.open('Images/Background.png')
        fonte = ImageFont.truetype('Fonts/Yasmen.ttf', 25)
        drawFont = ImageDraw.Draw(img)
        drawFont.text(xy=(260, 1), text=member.name, fill=(0, 0, 0), font=fonte)
        img.paste(avatar, (255, 40), avatar)
        img.save('bv.png')
        await channel.send(f"Olá {member.mention}, Bem Vindo ao Bar do Jaka! 🍸", file=discord.File('bv.png'))
        await self.bot.process_commands(member)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = await self.bot.fetch_channel("942067405331509308")
        msg = f"{member.mention} Foi de F 👻"
        await channel.send(msg)
        await self.bot.process_commands(member)
