import discord
from discord.ext import commands
import yt_dlp
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, COLORS
from utils import create_info_embed
from logger import log_command, log_error
import asyncio

class SearchPreviews(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'ytsearch',
        }
        
        if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET:
            auth = SpotifyClientCredentials(
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET
            )
            self.sp = spotipy.Spotify(auth_manager=auth)
        else:
            self.sp = None

    async def search_youtube_preview(self, query: str, limit: int = 5):
        try:
            loop = asyncio.get_event_loop()
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = await loop.run_in_executor(None, lambda: ydl.extract_info(f"ytsearch{limit}:{query}", download=False))
                results = []
                if info:
                    for item in info.get('entries', []):
                        results.append({
                            'title': item.get('title', 'Unknown'),
                            'url': item.get('webpage_url', ''),
                            'duration': item.get('duration', 0),
                            'thumbnail': item.get('thumbnail', ''),
                            'artist': item.get('uploader', 'Unknown'),
                            'source': 'youtube'
                        })
                return results
        except Exception as e:
            log_error(str(e), "search_youtube_preview")
            return []

    async def search_spotify_preview(self, query: str, limit: int = 5):
        if not self.sp:
            return []
        
        try:
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                None,
                lambda: self.sp.search(q=query, type='track', limit=limit)
            )
            
            preview_results = []
            if results['tracks']['items']:
                for track in results['tracks']['items']:
                    artists = ', '.join([artist['name'] for artist in track['artists']])
                    preview_results.append({
                        'title': track['name'],
                        'artist': artists,
                        'duration': track['duration_ms'] // 1000,
                        'thumbnail': track['album']['images'][0]['url'] if track['album']['images'] else None,
                        'url': track['external_urls'].get('spotify', ''),
                        'source': 'spotify'
                    })
            return preview_results
        except Exception as e:
            log_error(str(e), "search_spotify_preview")
            return []

    @commands.hybrid_command(name="search", description="Busca canciones con previsualizaciones")
    async def search(self, ctx, source: str = "all", *, query: str):
        log_command(ctx.author, f"search {source} {query}", ctx.guild.name)
        
        async with ctx.typing():
            youtube_results = []
            spotify_results = []
            
            if source in ["youtube", "all"]:
                youtube_results = await self.search_youtube_preview(query, 5)
            
            if source in ["spotify", "all"] and self.sp:
                spotify_results = await self.search_spotify_preview(query, 5)
        
        if not youtube_results and not spotify_results:
            embed = discord.Embed(
                title="❌ No se encontraron resultados",
                description=f"No hay resultados para: **{query}**",
                color=COLORS["error"]
            )
            return await ctx.send(embed=embed)
        
        embed = discord.Embed(
            title=f"🔍 Resultados de búsqueda para: {query}",
            color=COLORS["primary"]
        )
        
        if youtube_results:
            yt_text = ""
            for i, result in enumerate(youtube_results[:5], 1):
                yt_text += f"`{i}.` **{result['title'][:50]}** | {result['artist'][:30]}\n"
            embed.add_field(name="🎬 YouTube", value=yt_text, inline=False)
        
        if spotify_results:
            sp_text = ""
            for i, result in enumerate(spotify_results[:5], 1):
                sp_text += f"`{i}.` **{result['title'][:50]}** - {result['artist'][:30]}\n"
            embed.add_field(name="🎵 Spotify", value=sp_text, inline=False)
        
        embed.set_footer(text="Usa /play <canción> para reproducir")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(SearchPreviews(bot))
