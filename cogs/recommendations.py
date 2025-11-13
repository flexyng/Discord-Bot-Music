import discord
from discord.ext import commands
import db
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, COLORS
from utils import create_info_embed, create_error_embed, format_duration
from logger import log_command, log_error
import asyncio
from collections import Counter

class Recommendations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET:
            auth = SpotifyClientCredentials(
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET
            )
            self.sp = spotipy.Spotify(auth_manager=auth)
        else:
            self.sp = None

    @commands.hybrid_command(name="recommend", description="Obtiene recomendaciones basadas en tus gustos")
    async def recommend(self, ctx, limit: int = 5):
        log_command(ctx.author, f"recommend {limit}", ctx.guild.name)
        
        if not self.sp:
            embed = create_error_embed(
                "Las recomendaciones requieren credenciales de Spotify. Por favor configura tu bot con tokens de Spotify.",
                "Recomendaciones"
            )
            return await ctx.send(embed=embed)
        
        if limit > 10:
            limit = 10
        
        async with ctx.typing():
            try:
                stats = await db.get_user_stats(ctx.author.id)
                _, _, favorite_genre, favorite_artist = stats
                
                if not favorite_artist:
                    embed = create_error_embed(
                        "Necesitas escuchar más canciones para obtener recomendaciones personalizadas.\n\nUsa `/play` para agregar canciones a tu historial.",
                        "Sin datos"
                    )
                    return await ctx.send(embed=embed)
                
                loop = asyncio.get_event_loop()
                
                artist_results = await loop.run_in_executor(
                    None,
                    lambda: self.sp.search(q=favorite_artist, type='artist', limit=1)
                )
                
                if not artist_results['artists']['items']:
                    embed = create_error_embed("No se encontró el artista favorito", "Recomendaciones")
                    return await ctx.send(embed=embed)
                
                artist_id = artist_results['artists']['items'][0]['id']
                
                recommendations = await loop.run_in_executor(
                    None,
                    lambda: self.sp.recommendations(seed_artists=[artist_id], limit=limit)
                )
                
            except Exception as e:
                log_error(str(e), "recommend")
                embed = create_error_embed(
                    f"Error al obtener recomendaciones: {str(e)[:100]}",
                    "Error"
                )
                return await ctx.send(embed=embed)
        
        if not recommendations.get('tracks'):
            embed = create_error_embed("No se pudieron generar recomendaciones", "Recomendaciones")
            return await ctx.send(embed=embed)
        
        embed = discord.Embed(
            title="🎵 Recomendaciones Personalizadas",
            description=f"Basadas en tu artista favorito: **{favorite_artist}**",
            color=COLORS["primary"]
        )
        
        embed.add_field(
            name="Tu género favorito",
            value=f"`{favorite_genre or 'No determinado'}`",
            inline=True
        )
        
        recommendations_text = ""
        for i, track in enumerate(recommendations['tracks'], 1):
            artists = ', '.join([artist['name'] for artist in track['artists']])
            duration = format_duration(track['duration_ms'] // 1000)
            recommendations_text += f"`{i}.` **{track['name'][:40]}** - {artists[:30]}\n"
        
        embed.add_field(name="🎶 Canciones recomendadas", value=recommendations_text, inline=False)
        embed.set_footer(text="Usa /play para reproducir cualquiera de estas canciones")
        
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="similar", description="Encuentra canciones similares a tu favorita")
    async def similar_songs(self, ctx):
        log_command(ctx.author, "similar", ctx.guild.name)
        
        if not self.sp:
            embed = create_error_embed(
                "Esta función requiere credenciales de Spotify",
                "Similar"
            )
            return await ctx.send(embed=embed)
        
        favorites = await db.get_user_favorites(ctx.author.id, limit=1)
        
        if not favorites:
            embed = create_error_embed(
                "Necesitas tener canciones favoritas para esta función.\n\nUsa `/favorite add` para guardar canciones.",
                "Sin favoritos"
            )
            return await ctx.send(embed=embed)
        
        favorite_title = favorites[0][0]
        
        async with ctx.typing():
            try:
                loop = asyncio.get_event_loop()
                
                search_results = await loop.run_in_executor(
                    None,
                    lambda: self.sp.search(q=favorite_title, type='track', limit=1)
                )
                
                if not search_results['tracks']['items']:
                    embed = create_error_embed("No se encontró la canción", "Similar")
                    return await ctx.send(embed=embed)
                
                track_id = search_results['tracks']['items'][0]['id']
                
                similar = await loop.run_in_executor(
                    None,
                    lambda: self.sp.recommendations(seed_tracks=[track_id], limit=5)
                )
                
            except Exception as e:
                log_error(str(e), "similar_songs")
                embed = create_error_embed(f"Error: {str(e)[:100]}", "Error")
                return await ctx.send(embed=embed)
        
        embed = discord.Embed(
            title="🎵 Canciones Similares",
            description=f"Basadas en: **{favorite_title}**",
            color=COLORS["primary"]
        )
        
        similar_text = ""
        for i, track in enumerate(similar['tracks'], 1):
            artists = ', '.join([artist['name'] for artist in track['artists']])
            similar_text += f"`{i}.` **{track['name'][:40]}** - {artists[:30]}\n"
        
        embed.description = f"Basadas en: **{favorite_title}**\n\n" + similar_text
        embed.set_footer(text="Usa /play para reproducir")
        
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="topgenres", description="Muestra tus géneros más escuchados")
    async def top_genres(self, ctx):
        log_command(ctx.author, "topgenres", ctx.guild.name)
        
        stats = await db.get_user_stats(ctx.author.id)
        _, _, favorite_genre, favorite_artist = stats
        
        embed = discord.Embed(
            title="📊 Tus Géneros Favoritos",
            color=COLORS["primary"]
        )
        
        embed.add_field(
            name="🏆 #1 Género",
            value=f"`{favorite_genre or 'No determinado'}`",
            inline=False
        )
        
        embed.add_field(
            name="🎤 Artista Favorito",
            value=f"`{favorite_artist or 'No determinado'}`",
            inline=False
        )
        
        embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else None)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Recommendations(bot))
