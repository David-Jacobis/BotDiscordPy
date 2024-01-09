import discord
from discord.ext import commands


class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = ""
        self.text_channel_list = []
        self.set_message()

    def set_message(self):
        self.help_message = f"""
```
Comandos Gerais:
{self.bot.command_prefix}help - Exibe todos os comandos disponíveis
{self.bot.command_prefix}q - Exibe a fila de músicas atual
{self.bot.command_prefix}p <palavras-chave> - Encontra a música no YouTube e a reproduz no seu canal atual. Continuará a tocar a música atual se estiver pausada
{self.bot.command_prefix}skip - Pula a música atual em reprodução
{self.bot.command_prefix}clear - Interrompe a reprodução de música e limpa a fila
{self.bot.command_prefix}stop - Desconecta o bot do canal de voz
{self.bot.command_prefix}pause - Pausa a música atual em reprodução ou a retoma se já estiver pausada
{self.bot.command_prefix}resume - Retoma a reprodução da música atual
{self.bot.command_prefix}prefix - Altera o prefixo do comando
{self.bot.command_prefix}remove - Remove a última música da fila
```
"""

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game(f"digite {self.bot.command_prefix}help"))

    @commands.command(name="help", help="Exibe todos os comandos disponíveis")
    async def help(self, ctx):
        await ctx.send(self.help_message)

    @commands.command(name="send_to_all", help="Enviar uma mensagem para todos os membros")
    async def send_to_all(self, msg):
        for text_channel in self.text_channel_list:
            await text_channel.send(msg)
