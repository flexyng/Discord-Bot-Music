import discord
from discord.ext import commands
from utils import *
import db
from logger import log_command, log_error

class Playlists(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(name="playlist", description="Gestiona tus playlists")
    async def playlist(self, ctx):
        pass

    @playlist.command(name="create", description="Crea una nueva playlist")
    async def create_playlist(self, ctx, name: str, *, description: str = None):
        try:
            log_command(ctx.author, "playlist create", ctx.guild.name)
            
            await db.create_playlist(ctx.author.id, name, description)
            embed = create_success_embed("📋 Playlist creada", f"**{name}** ha sido creada exitosamente")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "create_playlist")
            embed = create_error_embed(f"Error al crear playlist: {e}")
            await ctx.send(embed=embed)

    @playlist.command(name="list", description="Muestra tus playlists")
    async def list_playlists(self, ctx):
        try:
            log_command(ctx.author, "playlist list", ctx.guild.name)
            
            playlists = await db.get_user_playlists(ctx.author.id)
            
            if not playlists:
                embed = create_info_embed("📋 Tus Playlists", "No tienes playlists creadas. Usa `/playlist create` para crear una.")
                return await ctx.send(embed=embed)
            
            embed = discord.Embed(
                title="📋 Tus Playlists",
                color=COLORS["primary"]
            )
            
            for playlist_id, name, description in playlists:
                value = description or "Sin descripción"
                embed.add_field(name=name, value=value, inline=False)
            
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "list_playlists")
            embed = create_error_embed(f"Error al obtener playlists: {e}")
            await ctx.send(embed=embed)

    @playlist.command(name="delete", description="Elimina una playlist")
    async def delete_playlist(self, ctx, name: str):
        try:
            log_command(ctx.author, "playlist delete", ctx.guild.name)
            
            playlists = await db.get_user_playlists(ctx.author.id)
            playlist_id = next((p[0] for p in playlists if p[1] == name), None)
            
            if not playlist_id:
                embed = create_error_embed(f"No se encontró la playlist **{name}**")
                return await ctx.send(embed=embed)
            
            await db.delete_playlist(playlist_id)
            embed = create_success_embed("🗑 Playlist eliminada", f"**{name}** ha sido eliminada")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "delete_playlist")
            embed = create_error_embed(f"Error al eliminar playlist: {e}")
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Playlists(bot))
