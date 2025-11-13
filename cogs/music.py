import discord
from discord.ext import commands, tasks
import yt_dlp
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from collections import defaultdict, deque
from utils import *
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, COLORS
import asyncio
import random
import db
from logger import log_command, log_error, log_music_event

class MusicPlayer:
    def __init__(self):
        self.queues = defaultdict(deque)
        self.now_playing = {}
        self.is_playing = defaultdict(bool)
        self.is_paused = defaultdict(bool)
        self.current_source = defaultdict(lambda: None)
        self.loop_status = defaultdict(lambda: "off")
        self.shuffle_enabled = defaultdict(bool)
        self.volume = defaultdict(lambda: 50)
        
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'ytsearch',
            'socket_timeout': 30,
        }
        
        if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET:
            auth = SpotifyClientCredentials(
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET
            )
            self.sp = spotipy.Spotify(auth_manager=auth)
        else:
            self.sp = None

    async def search_youtube(self, query: str):
        try:
            loop = asyncio.get_event_loop()
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = await loop.run_in_executor(None, lambda: ydl.extract_info(query, download=False))
                if info:
                    return {
                        'title': info.get('title', 'Unknown'),
                        'url': info.get('webpage_url', ''),
                        'duration': info.get('duration', 0),
                        'thumbnail': info.get('thumbnail', ''),
                        'artist': info.get('uploader', 'Unknown'),
                        'source': 'youtube'
                    }
        except Exception as e:
            log_error(str(e), "search_youtube")
        return None

    async def search_spotify(self, query: str):
        if not self.sp:
            return None
        
        try:
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                None,
                lambda: self.sp.search(q=query, type='track', limit=1)
            )
            
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                artists = ', '.join([artist['name'] for artist in track['artists']])
                
                ydl_query = f"{track['name']} {artists}"
                youtube_result = await self.search_youtube(ydl_query)
                
                return {
                    'title': track['name'],
                    'artist': artists,
                    'duration': track['duration_ms'] // 1000,
                    'thumbnail': track['album']['images'][0]['url'] if track['album']['images'] else None,
                    'url': youtube_result['url'] if youtube_result else None,
                    'source': 'spotify'
                }
        except Exception as e:
            log_error(str(e), "search_spotify")
        return None

    async def search(self, query: str, source: str = 'youtube'):
        if source == 'youtube':
            return await self.search_youtube(query)
        elif source == 'spotify':
            return await self.search_spotify(query)
        else:
            result = await self.search_youtube(query)
            if not result:
                result = await self.search_spotify(query)
            return result

    def add_to_queue(self, guild_id: int, song: dict):
        self.queues[guild_id].append(song)

    def get_queue(self, guild_id: int):
        return list(self.queues[guild_id])

    def clear_queue(self, guild_id: int):
        self.queues[guild_id].clear()

    def skip(self, guild_id: int):
        if self.queues[guild_id]:
            self.queues[guild_id].popleft()
            return True
        return False

    def shuffle_queue(self, guild_id: int):
        queue = list(self.queues[guild_id])
        random.shuffle(queue)
        self.queues[guild_id] = deque(queue)

    def toggle_loop(self, guild_id: int):
        if self.loop_status[guild_id] == "off":
            self.loop_status[guild_id] = "one"
        elif self.loop_status[guild_id] == "one":
            self.loop_status[guild_id] = "all"
        else:
            self.loop_status[guild_id] = "off"
        return self.loop_status[guild_id]

    def set_volume(self, guild_id: int, volume: int):
        self.volume[guild_id] = max(0, min(100, volume))
        return self.volume[guild_id]


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.player = MusicPlayer()

    @commands.hybrid_command(name="play", description="Reproduce una canción")
    async def play(self, ctx, *, query: str):
        if not ctx.author.voice:
            embed = create_error_embed("Debes estar en un canal de voz", "Sin conexión")
            return await ctx.send(embed=embed)

        channel = ctx.author.voice.channel
        log_command(ctx.author, f"play {query}", ctx.guild.name)
        
        async with ctx.typing():
            song = await self.player.search(query)
        
        if not song:
            embed = create_error_embed(f"No se encontró: **{query}**", "Búsqueda fallida")
            return await ctx.send(embed=embed)

        if not ctx.voice_client:
            await channel.connect()
        
        self.player.add_to_queue(ctx.guild.id, song)
        queue_pos = len(self.player.get_queue(ctx.guild.id))
        
        embed = create_success_embed(
            "✅ Agregado a la cola",
            f"**{song['title'][:60]}**\n\n🎤 {song.get('artist', 'Desconocido')}\n⏱ {format_duration(song.get('duration', 0))}\n📍 Posición: #{queue_pos}"
        )
        
        if song.get('thumbnail'):
            embed.set_thumbnail(url=song['thumbnail'])
        
        await ctx.send(embed=embed)
        log_music_event("added_to_queue", ctx.author.name, song['title'])
        
        if not ctx.voice_client.is_playing():
            await self._play_next(ctx)

    async def _play_next(self, ctx):
        queue = self.player.get_queue(ctx.guild.id)
        
        if not queue:
            if ctx.voice_client:
                await ctx.voice_client.disconnect()
            return
        
        song = self.player.queues[ctx.guild.id].popleft()
        self.player.now_playing[ctx.guild.id] = song
        self.player.is_playing[ctx.guild.id] = True
        
        await db.add_play_history(ctx.author.id, song['title'], song.get('artist', 'Unknown'), song.get('source', 'unknown'), song.get('duration', 0))
        log_music_event("now_playing", ctx.author.name, song['title'])
        
        embed = create_now_playing_embed(
            song['title'],
            song.get('artist', 'Desconocido'),
            song.get('duration', 0),
            song.get('thumbnail'),
            ctx.author
        )
        
        message = await ctx.send(embed=embed, view=self._create_view(ctx))
        self.player.current_source[ctx.guild.id] = message

    def _create_view(self, ctx):
        view = discord.ui.View()
        
        async def pause_callback(interaction):
            if ctx.voice_client and ctx.voice_client.is_playing():
                ctx.voice_client.pause()
                self.player.is_paused[ctx.guild.id] = True
                await interaction.response.defer()
        
        async def resume_callback(interaction):
            if ctx.voice_client and ctx.voice_client.is_paused():
                ctx.voice_client.resume()
                self.player.is_paused[ctx.guild.id] = False
                await interaction.response.defer()
        
        async def skip_callback(interaction):
            if ctx.voice_client and ctx.voice_client.is_playing():
                self.player.skip(ctx.guild.id)
                ctx.voice_client.stop()
            await interaction.response.defer()
        
        async def stop_callback(interaction):
            self.player.clear_queue(ctx.guild.id)
            if ctx.voice_client:
                await ctx.voice_client.disconnect()
            await interaction.response.defer()
        
        pause_btn = discord.ui.Button(label="⏸", style=discord.ButtonStyle.primary)
        pause_btn.callback = pause_callback
        view.add_item(pause_btn)
        
        resume_btn = discord.ui.Button(label="▶", style=discord.ButtonStyle.success)
        resume_btn.callback = resume_callback
        view.add_item(resume_btn)
        
        skip_btn = discord.ui.Button(label="⏭", style=discord.ButtonStyle.primary)
        skip_btn.callback = skip_callback
        view.add_item(skip_btn)
        
        stop_btn = discord.ui.Button(label="⏹", style=discord.ButtonStyle.danger)
        stop_btn.callback = stop_callback
        view.add_item(stop_btn)
        
        return view

    @commands.hybrid_command(name="queue", description="Muestra la cola de reproducción")
    async def queue(self, ctx, page: int = 1):
        log_command(ctx.author, "queue", ctx.guild.name)
        queue = self.player.get_queue(ctx.guild.id)
        
        if not queue:
            embed = create_error_embed("La cola está vacía", "Queue")
            return await ctx.send(embed=embed)
        
        embed = create_queue_embed(queue, page)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="skip", description="Salta la canción actual")
    async def skip(self, ctx):
        log_command(ctx.author, "skip", ctx.guild.name)
        
        if self.player.get_queue(ctx.guild.id):
            self.player.skip(ctx.guild.id)
            if ctx.voice_client:
                ctx.voice_client.stop()
            embed = create_success_embed("⏭ Canción saltada", "")
        else:
            embed = create_error_embed("No hay canciones en la cola", "Queue vacía")
        
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="stop", description="Detiene la música y desconecta")
    async def stop(self, ctx):
        log_command(ctx.author, "stop", ctx.guild.name)
        
        self.player.clear_queue(ctx.guild.id)
        self.player.is_playing[ctx.guild.id] = False
        
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        
        embed = create_success_embed("⏹ Música detenida", "El bot ha sido desconectado")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="pause", description="Pausa la música")
    async def pause(self, ctx):
        log_command(ctx.author, "pause", ctx.guild.name)
        
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            self.player.is_paused[ctx.guild.id] = True
            embed = create_success_embed("⏸ Música pausada", "")
        else:
            embed = create_error_embed("No hay música reproduciéndose", "Pause")
        
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="resume", description="Reanuda la música")
    async def resume(self, ctx):
        log_command(ctx.author, "resume", ctx.guild.name)
        
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            self.player.is_paused[ctx.guild.id] = False
            embed = create_success_embed("▶ Música reanudada", "")
        else:
            embed = create_error_embed("No hay música pausada", "Resume")
        
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="shuffle", description="Activa/desactiva modo shuffle")
    async def shuffle(self, ctx):
        log_command(ctx.author, "shuffle", ctx.guild.name)
        
        if self.player.shuffle_enabled[ctx.guild.id]:
            self.player.shuffle_enabled[ctx.guild.id] = False
            status = "❌ Desactivado"
        else:
            self.player.shuffle_enabled[ctx.guild.id] = True
            self.player.shuffle_queue(ctx.guild.id)
            status = "✅ Activado"
        
        embed = create_success_embed("🔀 Shuffle", f"Shuffle ha sido {status}")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="loop", description="Cambia el modo de repetición")
    async def loop(self, ctx):
        log_command(ctx.author, "loop", ctx.guild.name)
        
        loop_status = self.player.toggle_loop(ctx.guild.id)
        status_map = {"off": "❌ Desactivado", "one": "🔂 Una canción", "all": "🔁 Todas las canciones"}
        
        embed = create_success_embed("🔁 Modo de repetición", f"Repetición: {status_map.get(loop_status, 'Desconocido')}")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="volume", description="Ajusta el volumen (0-100)")
    async def volume(self, ctx, vol: int):
        log_command(ctx.author, f"volume {vol}", ctx.guild.name)
        
        volume = self.player.set_volume(ctx.guild.id, vol)
        embed = create_success_embed("🔊 Volumen", f"Volumen ajustado a **{volume}%**")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="nowplaying", description="Muestra la canción actual")
    async def nowplaying(self, ctx):
        log_command(ctx.author, "nowplaying", ctx.guild.name)
        
        song = self.player.now_playing.get(ctx.guild.id)
        
        if not song:
            embed = create_error_embed("No hay canción reproduciéndose", "Now Playing")
            return await ctx.send(embed=embed)
        
        embed = create_now_playing_embed(
            song['title'],
            song.get('artist', 'Desconocido'),
            song.get('duration', 0),
            song.get('thumbnail'),
            ctx.author
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="help", description="Muestra los comandos disponibles")
    async def help_cmd(self, ctx):
        embed = create_help_embed()
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Music(bot))
