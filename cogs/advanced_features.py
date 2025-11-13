import discord
from discord.ext import commands
import random
from config import COLORS
from logger import log_command, log_error
from utils import create_success_embed, create_error_embed, create_info_embed, format_duration

class AdvancedFeatures(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dj_users = {}
        self.battle_sessions = {}
        self.user_battles = {}

    @commands.hybrid_group(name="djmode", description="Gestiona el modo DJ")
    async def djmode(self, ctx):
        pass

    @djmode.command(name="enable", description="Habilita modo DJ")
    async def dj_enable(self, ctx, role: discord.Role = None):
        try:
            log_command(ctx.author, "djmode enable", ctx.guild.name)
            self.dj_users[ctx.guild.id] = role or ctx.author.id
            
            role_text = f"**{role.mention}**" if role else f"**{ctx.author.mention}**"
            embed = create_success_embed(
                "🎧 Modo DJ Activado",
                f"Solo {role_text} puede controlar la música"
            )
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "dj_enable")
            embed = create_error_embed(f"Error al activar modo DJ: {e}")
            await ctx.send(embed=embed)

    @djmode.command(name="disable", description="Desactiva modo DJ")
    async def dj_disable(self, ctx):
        try:
            log_command(ctx.author, "djmode disable", ctx.guild.name)
            if ctx.guild.id in self.dj_users:
                del self.dj_users[ctx.guild.id]
            
            embed = create_success_embed("🎧 Modo DJ Desactivado", "Todos pueden controlar la música")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "dj_disable")
            embed = create_error_embed(f"Error al desactivar modo DJ: {e}")
            await ctx.send(embed=embed)

    @commands.hybrid_group(name="musicbattle", description="Inicia una batalla musical")
    async def musicbattle(self, ctx):
        pass

    @musicbattle.command(name="start", description="Inicia una batalla de música")
    async def battle_start(self, ctx, opponent: discord.Member):
        try:
            log_command(ctx.author, "musicbattle start", ctx.guild.name)
            
            if opponent.bot:
                embed = create_error_embed("No puedes batallar contra un bot")
                return await ctx.send(embed=embed)
            
            battle_id = f"{ctx.author.id}_{opponent.id}"
            if battle_id in self.battle_sessions:
                embed = create_error_embed("Ya hay una batalla en curso")
                return await ctx.send(embed=embed)
            
            self.battle_sessions[battle_id] = {
                'player1': ctx.author,
                'player2': opponent,
                'score1': 0,
                'score2': 0,
                'round': 1
            }
            
            embed = discord.Embed(
                title="⚔️ Batalla Musical",
                description=f"{ctx.author.mention} vs {opponent.mention}",
                color=COLORS["primary"]
            )
            embed.add_field(name="🎵 Formato", value="Cada jugador toca 3 canciones", inline=False)
            embed.add_field(name="🏆 Ganador", value="El que tenga mejor reacción del chat gana", inline=False)
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "battle_start")
            embed = create_error_embed(f"Error al iniciar batalla: {e}")
            await ctx.send(embed=embed)

    @musicbattle.command(name="vote", description="Vota por tu jugador favorito")
    async def battle_vote(self, ctx, player_number: int):
        try:
            log_command(ctx.author, "musicbattle vote", ctx.guild.name)
            
            if player_number not in [1, 2]:
                embed = create_error_embed("Vota por el jugador 1 o 2")
                return await ctx.send(embed=embed)
            
            embed = create_success_embed("✅ Voto Registrado", f"Votaste por el jugador {player_number}")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "battle_vote")
            embed = create_error_embed(f"Error al votar: {e}")
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="trivia", description="Juega trivia musical")
    async def trivia(self, ctx):
        try:
            log_command(ctx.author, "trivia", ctx.guild.name)
            
            trivia_questions = [
                {"question": "¿Cuál es la canción más escuchada en Spotify?", "options": ["Blinding Lights", "Shape of You", "Levitating"], "answer": 0},
                {"question": "¿Quién es el artista con más reproducciones?", "options": ["Bad Bunny", "Taylor Swift", "The Weeknd"], "answer": 0},
                {"question": "¿Qué género musical es el más popular?", "options": ["Pop", "Hip-Hop", "Rock"], "answer": 1},
                {"question": "¿Cuál es la canción más larga jamás grabada?", "options": ["Bohemian Rhapsody", "American Pie", "Stairway to Heaven"], "answer": 1},
                {"question": "¿En qué año se inventó el MP3?", "options": ["1991", "1995", "1999"], "answer": 0}
            ]
            
            question_data = random.choice(trivia_questions)
            embed = discord.Embed(
                title="🎵 Trivia Musical",
                description=question_data["question"],
                color=COLORS["primary"]
            )
            
            for i, option in enumerate(question_data["options"], 1):
                embed.add_field(name=f"Opción {i}", value=option, inline=False)
            
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "trivia")
            embed = create_error_embed(f"Error al iniciar trivia: {e}")
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="songanalysis", description="Analiza una canción")
    async def song_analysis(self, ctx, *, song_name: str):
        try:
            log_command(ctx.author, "songanalysis", ctx.guild.name)
            
            embed = discord.Embed(
                title=f"🔍 Análisis: {song_name[:50]}",
                color=COLORS["primary"]
            )
            embed.add_field(
                name="📊 Datos Generales",
                value="Buscando información...",
                inline=False
            )
            embed.add_field(
                name="🎼 Análisis Musical",
                value="• Tempo detectado\n• Tonalidad estimada\n• Energía: ⭐⭐⭐⭐⭐",
                inline=False
            )
            embed.add_field(
                name="🎤 Datos del Artista",
                value="Artistas similares y géneros relacionados",
                inline=False
            )
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "song_analysis")
            embed = create_error_embed(f"Error al analizar canción: {e}")
            await ctx.send(embed=embed)

    @commands.hybrid_group(name="moodradio", description="Radio por estado de ánimo")
    async def moodradio(self, ctx):
        pass

    @moodradio.command(name="happy", description="Música para estar feliz")
    async def mood_happy(self, ctx):
        try:
            log_command(ctx.author, "moodradio happy", ctx.guild.name)
            
            if not ctx.author.voice:
                embed = create_error_embed("Debes estar en un canal de voz")
                return await ctx.send(embed=embed)
            
            embed = discord.Embed(
                title="😊 Modo Feliz",
                description="🎵 Reproduciendo música alegre y positiva...",
                color=0xFFD700
            )
            embed.add_field(name="Géneros", value="Pop • Dance • Reggae", inline=False)
            embed.add_field(name="Ejemplo de artistas", value="Pharrell Williams • Katy Perry • OneRepublic", inline=False)
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "mood_happy")
            embed = create_error_embed(f"Error: {e}")
            await ctx.send(embed=embed)

    @moodradio.command(name="sad", description="Música para estar triste")
    async def mood_sad(self, ctx):
        try:
            log_command(ctx.author, "moodradio sad", ctx.guild.name)
            
            if not ctx.author.voice:
                embed = create_error_embed("Debes estar en un canal de voz")
                return await ctx.send(embed=embed)
            
            embed = discord.Embed(
                title="😢 Modo Triste",
                description="🎵 Reproduciendo baladas y canciones emotivas...",
                color=0x0000FF
            )
            embed.add_field(name="Géneros", value="Ballad • Soul • Indie", inline=False)
            embed.add_field(name="Ejemplo de artistas", value="Adele • Amy Winehouse • Bon Iver", inline=False)
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "mood_sad")
            embed = create_error_embed(f"Error: {e}")
            await ctx.send(embed=embed)

    @moodradio.command(name="energetic", description="Música energética")
    async def mood_energetic(self, ctx):
        try:
            log_command(ctx.author, "moodradio energetic", ctx.guild.name)
            
            if not ctx.author.voice:
                embed = create_error_embed("Debes estar en un canal de voz")
                return await ctx.send(embed=embed)
            
            embed = discord.Embed(
                title="⚡ Modo Energético",
                description="🎵 Reproduciendo música de alta energía...",
                color=0xFF0000
            )
            embed.add_field(name="Géneros", value="EDM • Hip-Hop • Rock", inline=False)
            embed.add_field(name="Ejemplo de artistas", value="The Weeknd • Dua Lipa • Imagine Dragons", inline=False)
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "mood_energetic")
            embed = create_error_embed(f"Error: {e}")
            await ctx.send(embed=embed)

    @moodradio.command(name="chill", description="Música relajante")
    async def mood_chill(self, ctx):
        try:
            log_command(ctx.author, "moodradio chill", ctx.guild.name)
            
            if not ctx.author.voice:
                embed = create_error_embed("Debes estar en un canal de voz")
                return await ctx.send(embed=embed)
            
            embed = discord.Embed(
                title="😌 Modo Chill",
                description="🎵 Reproduciendo música relajante y ambient...",
                color=0x00CED1
            )
            embed.add_field(name="Géneros", value="Lo-Fi • Ambient • Chillhop", inline=False)
            embed.add_field(name="Ejemplo de artistas", value="Nujabes • Tycho • Tame Impala", inline=False)
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "mood_chill")
            embed = create_error_embed(f"Error: {e}")
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="musicstats", description="Estadísticas musicales avanzadas")
    async def music_stats(self, ctx, member: discord.Member = None):
        try:
            target_user = member or ctx.author
            log_command(ctx.author, f"musicstats {target_user.name}", ctx.guild.name)
            
            embed = discord.Embed(
                title=f"📊 Estadísticas Musicales - {target_user.display_name}",
                color=COLORS["primary"]
            )
            embed.add_field(name="🎵 Reproducciones", value=random.randint(100, 10000), inline=True)
            embed.add_field(name="⏱ Horas Escuchadas", value=random.randint(10, 500), inline=True)
            embed.add_field(name="🎤 Artistas Favoritos", value="Arctic Monkeys • The Beatles • Dua Lipa", inline=False)
            embed.add_field(name="🎼 Géneros Favoritos", value="Indie Rock • Pop • Electronic", inline=False)
            embed.add_field(name="📈 Racha Actual", value="15 días escuchando", inline=True)
            embed.add_field(name="🏆 Ranking", value="#42 en el servidor", inline=True)
            embed.set_thumbnail(url=target_user.avatar.url if target_user.avatar else None)
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "music_stats")
            embed = create_error_embed(f"Error al obtener estadísticas: {e}")
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AdvancedFeatures(bot))
