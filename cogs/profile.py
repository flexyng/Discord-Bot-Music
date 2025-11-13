import discord
from discord.ext import commands
from utils import *
import db
from logger import log_command, log_error
from config import COLORS

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="stats", description="Muestra tus estadísticas de música")
    async def stats(self, ctx):
        try:
            log_command(ctx.author, "stats", ctx.guild.name)
            
            stats = await db.get_user_stats(ctx.author.id)
            embed = create_stats_embed(ctx.author, stats)
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "stats")
            embed = create_error_embed(f"Error al obtener estadísticas: {e}")
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="profile", description="Muestra tu perfil")
    async def profile(self, ctx):
        try:
            log_command(ctx.author, "profile", ctx.guild.name)
            
            stats = await db.get_user_stats(ctx.author.id)
            settings = await db.get_user_settings(ctx.author.id)
            
            total_plays, total_time, _, _ = stats
            theme, notifications, autoplay, language = settings
            
            hours = total_time // 3600 if total_time else 0
            
            embed = discord.Embed(
                title=f"🎵 Perfil de {ctx.author.display_name}",
                color=COLORS["primary"],
                description="Tu información como usuario del bot de música"
            )
            
            embed.add_field(name="👤 Usuario", value=f"{ctx.author.mention}", inline=True)
            embed.add_field(name="🆔 ID", value=f"`{ctx.author.id}`", inline=True)
            embed.add_field(name="▶ Total de reproduciones", value=f"{total_plays:,}", inline=True)
            embed.add_field(name="⏱ Horas de música", value=f"{hours}h", inline=True)
            embed.add_field(name="🎨 Tema", value=f"`{theme}`", inline=True)
            embed.add_field(name="🔔 Notificaciones", value=f"{'✅ Activadas' if notifications else '❌ Desactivadas'}", inline=True)
            embed.add_field(name="▶ Reproducción automática", value=f"{'✅ Activada' if autoplay else '❌ Desactivada'}", inline=True)
            embed.add_field(name="🌐 Idioma", value=f"`{language}`", inline=True)
            
            embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else None)
            embed.set_footer(text=f"Miembro desde {ctx.author.created_at.strftime('%d/%m/%Y')} • Hecho por flexyng")
            
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "profile")
            embed = create_error_embed(f"Error al obtener perfil: {e}")
            await ctx.send(embed=embed)

    @commands.hybrid_group(name="settings", description="Gestiona tu configuración")
    async def settings(self, ctx):
        pass

    @settings.command(name="theme", description="Cambia tu tema")
    async def set_theme(self, ctx, theme: str):
        try:
            if theme not in ["dark", "light"]:
                embed = create_error_embed("Tema inválido. Usa: `dark` o `light`")
                return await ctx.send(embed=embed)
            
            await db.update_user_settings(ctx.author.id, theme=theme)
            embed = create_success_embed("🎨 Tema actualizado", f"Tu tema ha sido cambiado a **{theme}**")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "set_theme")
            embed = create_error_embed(f"Error al actualizar tema: {e}")
            await ctx.send(embed=embed)

    @settings.command(name="notifications", description="Activa/desactiva notificaciones")
    async def set_notifications(self, ctx, enabled: bool):
        try:
            await db.update_user_settings(ctx.author.id, notifications=enabled)
            status = "✅ Activadas" if enabled else "❌ Desactivadas"
            embed = create_success_embed("🔔 Notificaciones", f"Tus notificaciones han sido {status}")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "set_notifications")
            embed = create_error_embed(f"Error al actualizar notificaciones: {e}")
            await ctx.send(embed=embed)

    @settings.command(name="autoplay", description="Activa/desactiva reproducción automática")
    async def set_autoplay(self, ctx, enabled: bool):
        try:
            await db.update_user_settings(ctx.author.id, autoplay=enabled)
            status = "✅ Activada" if enabled else "❌ Desactivada"
            embed = create_success_embed("▶ Reproducción automática", f"La reproducción automática ha sido {status}")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "set_autoplay")
            embed = create_error_embed(f"Error al actualizar autoplay: {e}")
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Profile(bot))
