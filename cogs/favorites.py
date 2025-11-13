import discord
from discord.ext import commands
from utils import *
import db
from logger import log_command, log_error

class Favorites(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(name="favorite", description="Gestiona tus canciones favoritas")
    async def favorite(self, ctx):
        pass

    @favorite.command(name="add", description="Agrega una canción a favoritos")
    async def add_favorite(self, ctx, *, song_name: str):
        try:
            log_command(ctx.author, "favorite add", ctx.guild.name)
            
            # Aquí iría lógica para buscar la canción
            embed = create_success_embed("❤ Agregado a favoritos", f"Canción guardada: **{song_name}**")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "add_favorite")
            embed = create_error_embed(f"Error al agregar a favoritos: {e}")
            await ctx.send(embed=embed)

    @favorite.command(name="list", description="Muestra tus canciones favoritas")
    async def list_favorites(self, ctx):
        try:
            log_command(ctx.author, "favorite list", ctx.guild.name)
            
            favorites = await db.get_user_favorites(ctx.author.id)
            embed = create_favorites_embed(favorites, ctx.author)
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "list_favorites")
            embed = create_error_embed(f"Error al obtener favoritos: {e}")
            await ctx.send(embed=embed)

    @favorite.command(name="remove", description="Elimina una canción de favoritos")
    async def remove_favorite(self, ctx, *, song_name: str):
        try:
            log_command(ctx.author, "favorite remove", ctx.guild.name)
            
            embed = create_success_embed("❌ Eliminado de favoritos", f"Canción removida: **{song_name}**")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "remove_favorite")
            embed = create_error_embed(f"Error al eliminar de favoritos: {e}")
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Favorites(bot))
