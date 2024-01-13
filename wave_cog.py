import discord
from discord.ext import commands
import wavelink

class wave_cog(commands.Cog):
    def __int__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node {node.id} is ready!")

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.YouTubeTrack):
        ctx = player.ctx
        vc: player = ctx.voice_client

        if vc.loop:
            return await vc.play(track)

        next_song = vc.queue.get()
        await vc.play(next_song)
        await ctx.send(f"Tocando Agora: {next_song.title}")

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.YouTubeTrack):
        ctx = player.ctx
        vc: player = ctx.voice_client

        if vc.loop:
            return await vc.play(track)

        next_song = vc.queue.get()
        await vc.play(next_song)
        await ctx.send(f"Tocando Agora: {next_song.title}")

    async def node_connect(self):
        await self.bot.wait_until_ready()
        # 2 nodes
        node = wavelink.Node(uri='158.101.190.108:27531', password='enour-dev')
        node2 = wavelink.Node(uri='85.88.163.80:3128', password="saher.inzeworld.com")
        node3 = wavelink.Node(uri='eu-lavalink.lexnet.cc:2333', password="lexn3tl@val!nk")
        await wavelink.NodePool.connect(client=self.bot, nodes=[node, node2])

    @commands.command(name="play", aliases=["p", "playing"], help="Reproduz uma música selecionada do YouTube.")
    async def play(self, ctx, *, search: wavelink.YouTubeTrack):
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Entra no canal de música antes mané")
        else:
            vc: wavelink.Player = ctx.voice_client

        if vc.queue.is_empty and not vc.is_playing:
            await vc.play(search)
            await ctx.send(f"Tocando Agora: {search.title}.")
        else:
            await vc.queue.put_wait(search)
            await ctx.send(f"Adicionado `{search.title}` na fila.")
        vc.ctx = ctx
        setattr(vc, "loop", False)

        await vc.play(search)
        embed = discord.Embed(title="Música Tocando", description=f"Agora Tocando: `{search.title}`", color=0xFF5733)
        embed.set_footer(text="música pedida por: {}".format(ctx.author.display_name))
        embed.add_field(name='Duração', value=f"{search.duration}")
        embed.add_field(name='Autor', value=f"{search.author}")
        embed.add_field(name='Link da música', value=f"{search.uri}")
        await ctx.send(embed=embed)

    @commands.command(name="pause", help="Pausa a música atual em reprodução.")
    async def pause(self, ctx):
        if not ctx.voice_client:
            return await ctx.send("Você não está tocando nenhuma música, então como vou pausar alguma coisa?")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Entre em um canal de voz antes de executar este comando seu burro")
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.pause()
        await ctx.send("Música tocando pausada")

    @commands.command(name="resume", aliases=["r"], help="Continua a reprodução com o bot do Discord.")
    async def resume(self, ctx):
        if not ctx.voice_client:
            return await ctx.send("Como que eu vou tirar a pausa de uma música que não ta tocando??")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Entre em um canal de voz antes de executar este comando seu burro")
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.resume()
        await ctx.send("Música voltou a tocar rapaziada")

    @commands.command(name="stop", help= "Parar de Tocar a Música")
    async def stop(self, ctx):
        if not ctx.voice_client:
            return await ctx.send("Como que eu vou parar uma música que não está tocando??")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Entre em um canal de voz antes de executar este comando seu burro")
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.stop()
        await ctx.send("Parei essa música aí")

    @commands.command(name="quit", aliases=["disconnect", "l", "d"], help="Expulsar o bot do canal de voz.")
    async def disconnect(self, ctx):
        if not ctx.voice_client:
            return await ctx.send("Você ainda não usou o comando play para me inserir, então como vou sair de um canal??")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Entre em um canal de voz antes de executar este comando seu burro")
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.disconnect()
        await ctx.send("Saindo")

    @commands.command(name="queue", aliases=["q"], help="Exibe as músicas atuais na fila.")
    async def queue(self, ctx):
        if not ctx.voice_client:
            return await ctx.send("Você não está tocando nenhuma música, então como vou ver a fila??")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Entre em um canal de voz antes de executar este comando seu burro")
        else:
            vc: wavelink.Player = ctx.voice_client

        if vc.queue.is_empty:
            return await ctx.send("A fila ta vazia")
        embed = discord.Embed(title="Fila", description=f"", color=0xFF5733)
        embed.set_footer(text="Fila solicitada por: {}".format(ctx.author.display_name))
        song_count = 0
        for song in vc.queue:
            song_count += 1
            embed.add_field(name=f'Número da música {song_count}', value=f"`{song.title}`")
        await ctx.send(embed=embed)

