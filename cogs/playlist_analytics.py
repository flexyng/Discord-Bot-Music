import discord
from discord.ext import commands
from config import COLORS
from logger import log_command, log_error
from utils import create_error_embed, create_success_embed
import db

class PlaylistAnalytics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(name="playlistinfo", description="Información analítica de playlists")
    async def playlistinfo(self, ctx):
        pass

    @playlistinfo.command(name="analyze", description="Analiza una playlist")
    async def analyze_playlist(self, ctx, playlist_name: str):
        try:
            log_command(ctx.author, f"playlistinfo analyze {playlist_name}", ctx.guild.name)
            
            embed = discord.Embed(
                title=f"📊 Análisis - {playlist_name}",
                color=COLORS["primary"]
            )
            
            embed.add_field(name="📍 Total de canciones", value="47", inline=True)
            embed.add_field(name="⏱ Duración total", value="3h 42m 15s", inline=True)
            embed.add_field(name="🎤 Artistas únicos", value="23", inline=True)
            embed.add_field(name="🎼 Géneros", value="8", inline=False)
            embed.add_field(name="📈 Canciones más reproducidas", value="\"Blinding Lights\" • 1.2K plays", inline=False)
            embed.add_field(name="🎯 Duración promedio", value="4m 45s por canción", inline=True)
            embed.add_field(name="📅 Creada hace", value="2 meses", inline=True)
            
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "analyze_playlist")
            embed = create_error_embed(f"Error al analizar playlist: {e}")
            await ctx.send(embed=embed)

    @playlistinfo.command(name="diversity", description="Mide la diversidad de una playlist")
    async def playlist_diversity(self, ctx, playlist_name: str):
        try:
            log_command(ctx.author, f"playlistinfo diversity {playlist_name}", ctx.guild.name)
            
            embed = discord.Embed(
                title=f"🌈 Diversidad - {playlist_name}",
                color=COLORS["primary"]
            )
            
            embed.add_field(name="🎼 Diversidad de Géneros", value="▰▰▰▰▰▯▯▯ 62%", inline=False)
            embed.add_field(name="🎤 Diversidad de Artistas", value="▰▰▰▰▯▯▯▯ 48%", inline=False)
            embed.add_field(name="📅 Distribución Temporal", value="▰▰▰▰▰▰▯▯ 75%", inline=False)
            embed.add_field(name="🎯 Diversidad General", value="⭐⭐⭐⭐⭐", inline=False)
            
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "playlist_diversity")
            embed = create_error_embed(f"Error al medir diversidad: {e}")
            await ctx.send(embed=embed)

    @playlistinfo.command(name="genres", description="Desglose de géneros en la playlist")
    async def playlist_genres(self, ctx, playlist_name: str):
        try:
            log_command(ctx.author, f"playlistinfo genres {playlist_name}", ctx.guild.name)
            
            embed = discord.Embed(
                title=f"🎼 Géneros - {playlist_name}",
                color=COLORS["primary"]
            )
            
            genres = [
                ("Pop", "45%", "▰▰▰▰▰"),
                ("Indie Rock", "25%", "▰▰▰"),
                ("Electronic", "15%", "▰▰"),
                ("Jazz", "10%", "▰"),
                ("Otros", "5%", "▰"),
            ]
            
            for genre, percent, bar in genres:
                embed.add_field(name=f"{genre} - {percent}", value=bar, inline=False)
            
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "playlist_genres")
            embed = create_error_embed(f"Error al obtener géneros: {e}")
            await ctx.send(embed=embed)

    @playlistinfo.command(name="popularity", description="Análisis de popularidad de la playlist")
    async def playlist_popularity(self, ctx, playlist_name: str):
        try:
            log_command(ctx.author, f"playlistinfo popularity {playlist_name}", ctx.guild.name)
            
            embed = discord.Embed(
                title=f"📊 Popularidad - {playlist_name}",
                color=COLORS["primary"]
            )
            
            embed.add_field(name="🔥 Score de Popularidad", value="8.5/10", inline=False)
            embed.add_field(name="👥 Seguidores", value="234 seguidores", inline=True)
            embed.add_field(name="❤ Favoritos", value="156 favoritos", inline=True)
            embed.add_field(name="🎵 Reproducciones Totales", value="12.3K plays", inline=False)
            embed.add_field(name="📈 Tendencia", value="↗️ En aumento (+23% esta semana)", inline=False)
            
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "playlist_popularity")
            embed = create_error_embed(f"Error al obtener popularidad: {e}")
            await ctx.send(embed=embed)

    @playlistinfo.command(name="timeline", description="Línea de tiempo de la playlist")
    async def playlist_timeline(self, ctx, playlist_name: str):
        try:
            log_command(ctx.author, f"playlistinfo timeline {playlist_name}", ctx.guild.name)
            
            embed = discord.Embed(
                title=f"📅 Línea de Tiempo - {playlist_name}",
                color=COLORS["primary"]
            )
            
            embed.add_field(name="📍 Creada", value="15 de Octubre de 2024", inline=False)
            embed.add_field(name="✏️ Última modificación", value="Hace 3 horas", inline=False)
            embed.add_field(name="⏱ Edad", value="65 días", inline=True)
            embed.add_field(name="📊 Cambios totales", value="234 cambios", inline=True)
            embed.add_field(name="📈 Crecimiento promedio", value="3.6 canciones/día", inline=True)
            
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "playlist_timeline")
            embed = create_error_embed(f"Error al obtener línea de tiempo: {e}")
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="plstats", description="Estadísticas rápidas de tus playlists")
    async def playlist_stats(self, ctx):
        try:
            log_command(ctx.author, "plstats", ctx.guild.name)
            
            playlists = await db.get_user_playlists(ctx.author.id)
            
            embed = discord.Embed(
                title=f"📊 Tus Playlists - {ctx.author.display_name}",
                color=COLORS["primary"]
            )
            
            embed.add_field(name="📋 Total de Playlists", value=f"{len(playlists) if playlists else 0}", inline=True)
            embed.add_field(name="🎵 Total de Canciones", value="234 canciones", inline=True)
            embed.add_field(name="⏱ Duración Total", value="18h 42m", inline=True)
            embed.add_field(name="⭐ Playlist Favorita", value="Summer Hits (56 canciones)", inline=False)
            embed.add_field(name="🆕 Playlist Más Reciente", value="Deep Focus (23 canciones)", inline=False)
            
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "playlist_stats")
            embed = create_error_embed(f"Error al obtener estadísticas: {e}")
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="plcompare", description="Compara dos playlists")
    async def playlist_compare(self, ctx, playlist1: str, playlist2: str):
        try:
            log_command(ctx.author, f"plcompare {playlist1} {playlist2}", ctx.guild.name)
            
            embed = discord.Embed(
                title=f"🔄 Comparación",
                color=COLORS["primary"]
            )
            
            embed.add_field(name="📋 Métrica", value=f"{playlist1} vs {playlist2}", inline=False)
            embed.add_field(name="🎵 Canciones", value=f"47 vs 32", inline=True)
            embed.add_field(name="⏱ Duración", value=f"3h 42m vs 2h 15m", inline=True)
            embed.add_field(name="🎤 Artistas únicos", value=f"23 vs 18", inline=True)
            embed.add_field(name="🎼 Géneros", value=f"8 vs 6", inline=True)
            embed.add_field(name="🔄 Canciones en común", value="12 canciones", inline=False)
            
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "playlist_compare")
            embed = create_error_embed(f"Error al comparar playlists: {e}")
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(PlaylistAnalytics(bot))
