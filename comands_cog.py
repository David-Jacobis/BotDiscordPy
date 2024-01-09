import discord
from discord.ext import commands
import os
import random

class comands_cog(commands.Cog):
    def __int__(self,bot):
        self.bot = bot

    @commands.command(name="braço")
    async def braco(self,ctx):
        pasta_imagens = 'Images/braco'  # Substitua pelo caminho real da sua pasta
        lista_de_imagens = [f for f in os.listdir(pasta_imagens) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

        if lista_de_imagens:
            imagem_escolhida = random.choice(lista_de_imagens)
            caminho_completo = os.path.join(pasta_imagens, imagem_escolhida)

            with open(caminho_completo, 'rb') as imagem:
                arquivo = discord.File(imagem)
                descricoes = ["Cheirin de bussa", "Já Pode?", "Botou no Cool", "Amassa Velhas", "Vou fazer o AP do time", "Aqui tem Setup de Gank"]

                descricao_aleatoria = random.choice(descricoes)
                await ctx.send(descricao_aleatoria, file=arquivo)
        else:
            await ctx.send("Nenhuma imagem encontrada na pasta.")

    @commands.command(name="goza")
    async def goza(self,ctx):
        await ctx.send('Já pode?', file=discord.File('Images/deixa.jpeg'))
