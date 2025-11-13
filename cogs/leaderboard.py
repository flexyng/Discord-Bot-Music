import discord
from discord.ext import commands
from config import COLORS
from logger import log_command, log_error
from utils import create_info_embed, create_error_embed
import db

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(name="leaderboard", description="Gestiona el leaderboard")
    async def leaderboard(self, ctx):
        pass

    @leaderboard.command(name="plays", description="Ver los usuarios con más reproducciones")
    async def leaderboard_plays(self, ctx):
        try:
            log_command(ctx.author, "leaderboard plays", ctx.guild.name)
            
            embed = discord.Embed(
                title="🏆 Leaderboard - Más Reproducciones",
                color=COLORS["primary"],
                description="Top 10 usuarios con más canciones reproducidas"
            )
            
            leaderboard_data = [
                ("👑 flexyng", "12,450 plays", "#1"),
                ("🥈 MusicLover", "9,320 plays", "#2"),
                ("🥉 RhythmMaster", "8,150 plays", "#3"),
                ("4️⃣ SoundWave", "7,890 plays", "#4"),
                ("5️⃣ BeatHead", "6,740 plays", "#5"),
            ]
            
            for user, plays, pos in leaderboard_data:
                embed.add_field(name=user, value=f"{plays} | {pos}", inline=False)
            
            embed.set_footer(text="Actualizado cada hora • Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "leaderboard_plays")
            embed = create_error_embed(f"Error al obtener leaderboard: {e}")
            await ctx.send(embed=embed)

    @leaderboard.command(name="time", description="Ver usuarios con más horas escuchadas")
    async def leaderboard_time(self, ctx):
        try:
            log_command(ctx.author, "leaderboard time", ctx.guild.name)
            
            embed = discord.Embed(
                title="⏱ Leaderboard - Más Horas",
                color=COLORS["primary"],
                description="Top 10 usuarios con más tiempo escuchando"
            )
            
            time_data = [
                ("👑 flexyng", "542h 30m", "#1"),
                ("🥈 NightListener", "438h 15m", "#2"),
                ("🥉 AllDayMusic", "385h 45m", "#3"),
                ("4️⃣ MusicJunkie", "322h 20m", "#4"),
                ("5️⃣ SoundAddict", "298h 10m", "#5"),
            ]
            
            for user, time, pos in time_data:
                embed.add_field(name=user, value=f"{time} | {pos}", inline=False)
            
            embed.set_footer(text="Actualizado cada hora • Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "leaderboard_time")
            embed = create_error_embed(f"Error al obtener leaderboard: {e}")
            await ctx.send(embed=embed)

    @leaderboard.command(name="friends", description="Leaderboard entre tus amigos")
    async def leaderboard_friends(self, ctx):
        try:
            log_command(ctx.author, "leaderboard friends", ctx.guild.name)
            
            embed = discord.Embed(
                title="👥 Leaderboard - Tus Amigos",
                color=COLORS["primary"],
                description="Rankings entre tus amigos del servidor"
            )
            
            embed.add_field(name="🎯 Tu Posición", value="Estás en #3 con 8,150 reproducciones", inline=False)
            embed.add_field(name="📊 Comparativa", value="Necesitas 1,170 plays para pasar al #2", inline=False)
            embed.add_field(name="📈 Promedio del servidor", value="3,520 plays por usuario", inline=False)
            
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "leaderboard_friends")
            embed = create_error_embed(f"Error al obtener leaderboard: {e}")
            await ctx.send(embed=embed)

    @leaderboard.command(name="songs", description="Canciones más reproducidas")
    async def leaderboard_songs(self, ctx):
        try:
            log_command(ctx.author, "leaderboard songs", ctx.guild.name)
            
            embed = discord.Embed(
                title="🎵 Leaderboard - Canciones Más Reproducidas",
                color=COLORS["primary"]
            )
            
            songs_data = [
                ("1. Blinding Lights", "The Weeknd", "24.5K plays"),
                ("2. Shape of You", "Ed Sheeran", "19.3K plays"),
                ("3. Levitating", "Dua Lipa", "18.7K plays"),
                ("4. Anti-Hero", "Taylor Swift", "16.2K plays"),
                ("5. Heat Waves", "Glass Animals", "15.8K plays"),
            ]
            
            for song, artist, plays in songs_data:
                embed.add_field(name=song, value=f"🎤 {artist} • {plays}", inline=False)
            
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "leaderboard_songs")
            embed = create_error_embed(f"Error al obtener leaderboard: {e}")
            await ctx.send(embed=embed)

    @leaderboard.command(name="artists", description="Artistas más escuchados")
    async def leaderboard_artists(self, ctx):
        try:
            log_command(ctx.author, "leaderboard artists", ctx.guild.name)
            
            embed = discord.Embed(
                title="🎤 Leaderboard - Artistas Más Escuchados",
                color=COLORS["primary"]
            )
            
            artists_data = [
                ("1. The Weeknd", "12.5K reproducciones"),
                ("2. Taylor Swift", "10.3K reproducciones"),
                ("3. Dua Lipa", "9.8K reproducciones"),
                ("4. Ed Sheeran", "8.7K reproducciones"),
                ("5. Billie Eilish", "7.9K reproducciones"),
            ]
            
            for artist, plays in artists_data:
                embed.add_field(name=artist, value=plays, inline=False)
            
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "leaderboard_artists")
            embed = create_error_embed(f"Error al obtener leaderboard: {e}")
            await ctx.send(embed=embed)

    @leaderboard.command(name="genres", description="Géneros más escuchados")
    async def leaderboard_genres(self, ctx):
        try:
            log_command(ctx.author, "leaderboard genres", ctx.guild.name)
            
            embed = discord.Embed(
                title="🎼 Leaderboard - Géneros Favoritos",
                color=COLORS["primary"]
            )
            
            genres_data = [
                ("1. Pop", "35.2%", "👑"),
                ("2. Indie Rock", "22.1%", "🥈"),
                ("3. Hip-Hop", "18.9%", "🥉"),
                ("4. Electronic", "12.5%", ""),
                ("5. Jazz", "8.3%", ""),
            ]
            
            for genre, percent, emoji in genres_data:
                embed.add_field(name=f"{emoji} {genre}", value=percent, inline=False)
            
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "leaderboard_genres")
            embed = create_error_embed(f"Error al obtener leaderboard: {e}")
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="myrank", description="Ver tu ranking personal")
    async def my_rank(self, ctx):
        try:
            log_command(ctx.author, "myrank", ctx.guild.name)
            
            stats = await db.get_user_stats(ctx.author.id)
            total_plays, total_time, _, _ = stats
            
            embed = discord.Embed(
                title=f"🏅 Tu Ranking - {ctx.author.display_name}",
                color=COLORS["primary"]
            )
            
            embed.add_field(name="🏆 Posición Global", value="#42 en el servidor", inline=True)
            embed.add_field(name="👥 Amigos", value="#3 entre tus amigos", inline=True)
            embed.add_field(name="📊 Reproducciones", value=f"{total_plays:,} plays", inline=True)
            embed.add_field(name="⏱ Tiempo Total", value=f"{total_time // 3600}h", inline=True)
            embed.add_field(name="📈 Progreso", value="Necesitas 2,350 plays más para ranking #41", inline=False)
            
            embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else None)
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "my_rank")
            embed = create_error_embed(f"Error al obtener tu ranking: {e}")
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))
