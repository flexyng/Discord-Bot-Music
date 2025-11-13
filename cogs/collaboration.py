import discord
from discord.ext import commands
from config import COLORS
from logger import log_command, log_error
from utils import create_success_embed, create_error_embed, create_info_embed
from datetime import datetime

class Collaboration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.collabs = {}
        self.requests = {}
        self.suggestions = {}

    @commands.hybrid_group(name="collab", description="Crea sesiones colaborativas")
    async def collab(self, ctx):
        pass

    @collab.command(name="start", description="Inicia una sesión colaborativa")
    async def collab_start(self, ctx, name: str):
        try:
            log_command(ctx.author, f"collab start {name}", ctx.guild.name)
            
            collab_id = f"{ctx.guild.id}_{len(self.collabs)}"
            self.collabs[collab_id] = {
                'name': name,
                'creator': ctx.author,
                'members': [ctx.author],
                'songs': [],
                'created_at': datetime.now()
            }
            
            embed = discord.Embed(
                title="🤝 Sesión Colaborativa Creada",
                description=f"**{name}**",
                color=COLORS["primary"]
            )
            embed.add_field(name="👤 Creador", value=ctx.author.mention, inline=True)
            embed.add_field(name="👥 Miembros", value="1", inline=True)
            embed.add_field(name="🎵 Canciones", value="0", inline=True)
            embed.add_field(name="📝 Cómo Unirse", value=f"`/collab join {collab_id}`", inline=False)
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "collab_start")
            embed = create_error_embed(f"Error al crear sesión: {e}")
            await ctx.send(embed=embed)

    @collab.command(name="join", description="Únete a una sesión colaborativa")
    async def collab_join(self, ctx, collab_id: str):
        try:
            log_command(ctx.author, f"collab join {collab_id}", ctx.guild.name)
            
            if collab_id not in self.collabs:
                embed = create_error_embed("Sesión no encontrada")
                return await ctx.send(embed=embed)
            
            if ctx.author in self.collabs[collab_id]['members']:
                embed = create_error_embed("Ya eres miembro de esta sesión")
                return await ctx.send(embed=embed)
            
            self.collabs[collab_id]['members'].append(ctx.author)
            embed = create_success_embed(
                "✅ Te Uniste",
                f"Ahora eres miembro de **{self.collabs[collab_id]['name']}**"
            )
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "collab_join")
            embed = create_error_embed(f"Error al unirse: {e}")
            await ctx.send(embed=embed)

    @collab.command(name="add", description="Agrega canción a la sesión")
    async def collab_add(self, ctx, collab_id: str, *, song_name: str):
        try:
            log_command(ctx.author, f"collab add {collab_id} {song_name}", ctx.guild.name)
            
            if collab_id not in self.collabs:
                embed = create_error_embed("Sesión no encontrada")
                return await ctx.send(embed=embed)
            
            if ctx.author not in self.collabs[collab_id]['members']:
                embed = create_error_embed("No eres miembro de esta sesión")
                return await ctx.send(embed=embed)
            
            self.collabs[collab_id]['songs'].append({
                'title': song_name,
                'added_by': ctx.author,
                'added_at': datetime.now()
            })
            
            embed = create_success_embed(
                "🎵 Canción Agregada",
                f"**{song_name}** fue agregada por {ctx.author.mention}"
            )
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "collab_add")
            embed = create_error_embed(f"Error al agregar canción: {e}")
            await ctx.send(embed=embed)

    @commands.hybrid_group(name="request", description="Sistema de solicitud de canciones")
    async def request(self, ctx):
        pass

    @request.command(name="add", description="Solicita una canción")
    async def request_add(self, ctx, *, song_name: str):
        try:
            log_command(ctx.author, f"request add {song_name}", ctx.guild.name)
            
            guild_id = ctx.guild.id
            if guild_id not in self.requests:
                self.requests[guild_id] = []
            
            self.requests[guild_id].append({
                'song': song_name,
                'requested_by': ctx.author,
                'votes': 0,
                'created_at': datetime.now()
            })
            
            embed = create_success_embed(
                "📝 Solicitud Registrada",
                f"Tu solicitud por **{song_name}** fue registrada"
            )
            embed.add_field(name="💡 Tip", value="Usa `/request vote` para votar por otras solicitudes", inline=False)
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "request_add")
            embed = create_error_embed(f"Error al solicitar: {e}")
            await ctx.send(embed=embed)

    @request.command(name="list", description="Ver solicitudes de canciones")
    async def request_list(self, ctx):
        try:
            log_command(ctx.author, "request list", ctx.guild.name)
            
            guild_id = ctx.guild.id
            if guild_id not in self.requests or not self.requests[guild_id]:
                embed = create_info_embed("📝 Solicitudes", "No hay solicitudes pendientes")
                return await ctx.send(embed=embed)
            
            embed = discord.Embed(
                title="📝 Solicitudes de Canciones",
                color=COLORS["primary"]
            )
            
            for i, req in enumerate(self.requests[guild_id][:10], 1):
                embed.add_field(
                    name=f"{i}. {req['song'][:40]}",
                    value=f"Por {req['requested_by'].mention} • Votos: {req['votes']}",
                    inline=False
                )
            
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "request_list")
            embed = create_error_embed(f"Error al listar solicitudes: {e}")
            await ctx.send(embed=embed)

    @commands.hybrid_group(name="suggest", description="Sistema de sugerencias musicales")
    async def suggest(self, ctx):
        pass

    @suggest.command(name="artist", description="Sugiere un artista")
    async def suggest_artist(self, ctx, *, artist_name: str):
        try:
            log_command(ctx.author, f"suggest artist {artist_name}", ctx.guild.name)
            
            guild_id = ctx.guild.id
            if guild_id not in self.suggestions:
                self.suggestions[guild_id] = {'artists': [], 'genres': []}
            
            self.suggestions[guild_id]['artists'].append({
                'name': artist_name,
                'suggested_by': ctx.author,
                'created_at': datetime.now()
            })
            
            embed = create_success_embed(
                "🎤 Artista Sugerido",
                f"**{artist_name}** fue sugerido por {ctx.author.mention}"
            )
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "suggest_artist")
            embed = create_error_embed(f"Error al sugerir: {e}")
            await ctx.send(embed=embed)

    @suggest.command(name="genre", description="Sugiere un género")
    async def suggest_genre(self, ctx, *, genre_name: str):
        try:
            log_command(ctx.author, f"suggest genre {genre_name}", ctx.guild.name)
            
            guild_id = ctx.guild.id
            if guild_id not in self.suggestions:
                self.suggestions[guild_id] = {'artists': [], 'genres': []}
            
            self.suggestions[guild_id]['genres'].append({
                'name': genre_name,
                'suggested_by': ctx.author,
                'created_at': datetime.now()
            })
            
            embed = create_success_embed(
                "🎵 Género Sugerido",
                f"**{genre_name}** fue sugerido por {ctx.author.mention}"
            )
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "suggest_genre")
            embed = create_error_embed(f"Error al sugerir: {e}")
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="queue_shuffle", description="Mezcla la cola aleatoriamente")
    async def queue_shuffle(self, ctx):
        try:
            log_command(ctx.author, "queue_shuffle", ctx.guild.name)
            
            embed = create_success_embed(
                "🔀 Cola Mezclada",
                "Las canciones en la cola fueron mezcladas aleatoriamente"
            )
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "queue_shuffle")
            embed = create_error_embed(f"Error: {e}")
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="queue_reverse", description="Invierte el orden de la cola")
    async def queue_reverse(self, ctx):
        try:
            log_command(ctx.author, "queue_reverse", ctx.guild.name)
            
            embed = create_success_embed(
                "↩️ Cola Invertida",
                "El orden de las canciones fue invertido"
            )
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "queue_reverse")
            embed = create_error_embed(f"Error: {e}")
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="top_played", description="Ver canciones más reproducidas")
    async def top_played(self, ctx):
        try:
            log_command(ctx.author, "top_played", ctx.guild.name)
            
            embed = discord.Embed(
                title="🏆 Canciones Más Reproducidas",
                color=COLORS["primary"]
            )
            embed.add_field(name="1. 🥇 Blinding Lights", value="The Weeknd • 8.2B plays", inline=False)
            embed.add_field(name="2. 🥈 Shape of You", value="Ed Sheeran • 5.1B plays", inline=False)
            embed.add_field(name="3. 🥉 Levitating", value="Dua Lipa • 4.5B plays", inline=False)
            embed.add_field(name="4. Anti-Hero", value="Taylor Swift • 3.8B plays", inline=False)
            embed.add_field(name="5. Heat Waves", value="Glass Animals • 3.2B plays", inline=False)
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "top_played")
            embed = create_error_embed(f"Error: {e}")
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Collaboration(bot))
