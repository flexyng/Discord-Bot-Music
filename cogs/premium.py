import discord
from discord.ext import commands
from utils import create_success_embed, create_error_embed, create_info_embed, premium_only
from logger import log_command, log_error
from config import COLORS, PREMIUM_FEATURES
import db

class Premium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="premium", description="Gestionar suscripción premium")
    async def premium(self, ctx):
        try:
            await ctx.send("Use `/premium redeem`, `/premium info` o `/premium status`")
        except Exception as e:
            log_error(ctx.author.id, "premium", str(e))

    @commands.hybrid_group(name="premium", invoke_without_command=True, description="Comandos de premium")
    async def premium_group(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Usa `/premium redeem <key>`, `/premium info` o `/premium status`")

    @premium_group.command(name="redeem", description="Redimir clave premium")
    async def redeem(self, ctx, key: str):
        try:
            log_command(ctx.author.id, "premium_redeem", {"key": key})
            
            success, message = await db.redeem_premium_key(ctx.author.id, key)
            
            if success:
                embed = create_success_embed(
                    "✅ Premium Activado",
                    message
                )
                embed.add_field(
                    name="🎁 Beneficios Premium",
                    value="""
• Playlists ilimitadas
• Cola ilimitada
• Análisis avanzado
• Prefijo personalizado
• Soporte prioritario
• Sin anuncios
""",
                    inline=False
                )
            else:
                embed = create_error_embed("❌ Error", message)
            
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(ctx.author.id, "premium_redeem", str(e))
            embed = create_error_embed("❌ Error", str(e))
            await ctx.send(embed=embed)

    @premium_group.command(name="info", description="Ver información de premium")
    async def info(self, ctx):
        try:
            log_command(ctx.author.id, "premium_info", {})
            
            embed = discord.Embed(
                title="💎 Sistema Premium",
                color=COLORS["premium"],
                description="Obtén acceso a funciones exclusivas"
            )
            
            embed.add_field(
                name="🎁 Beneficios Premium",
                value="""
✅ **Playlists Ilimitadas** (vs 5 en Free)
✅ **Cola Ilimitada** (vs 50 en Free)
✅ **Análisis Avanzado** (Estadísticas detalladas)
✅ **Prefijo Personalizado** (Crea tu propio prefix)
✅ **Soporte Prioritario** (Respuesta inmediata)
✅ **Sin Anuncios** (Experiencia limpia)
✅ **Comandos Exclusivos Premium**
✅ **Descarga de Playlists** (Para premium users)
""",
                inline=False
            )
            
            embed.add_field(
                name="📊 Comparación Free vs Premium",
                value=f"""
**Playlists**: {PREMIUM_FEATURES['unlimited_playlists']['free']} vs Ilimitadas
**Cola**: {PREMIUM_FEATURES['unlimited_queue']['free']} canciones vs Ilimitada
**Análisis**: {('No' if not PREMIUM_FEATURES['advanced_analytics']['free'] else 'Sí')} vs Sí
**Prefijo Custom**: {('No' if not PREMIUM_FEATURES['custom_prefix']['free'] else 'Sí')} vs Sí
**Soporte**: Estándar vs Prioritario
""",
                inline=False
            )
            
            embed.add_field(
                name="🔑 Cómo Obtener Premium",
                value="Usa `/premium redeem <key>` con una clave de activación",
                inline=False
            )
            
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(ctx.author.id, "premium_info", str(e))
            embed = create_error_embed("❌ Error", str(e))
            await ctx.send(embed=embed)

    @premium_group.command(name="status", description="Ver tu estado premium")
    async def status(self, ctx):
        try:
            log_command(ctx.author.id, "premium_status", {})
            
            is_premium = await db.is_premium(ctx.author.id)
            info = await db.get_premium_info(ctx.author.id)
            
            embed = discord.Embed(
                title=f"📊 Tu Estado Premium",
                color=COLORS["premium"] if is_premium else COLORS["error"]
            )
            
            embed.add_field(
                name="Estado",
                value="✅ Premium Activo" if is_premium else "❌ Usuario Free",
                inline=False
            )
            
            if is_premium and info and info.get("premium_expires_at"):
                from datetime import datetime
                expires_at = info["premium_expires_at"]
                days_left = (expires_at - datetime.utcnow()).days
                
                embed.add_field(
                    name="📅 Vence",
                    value=expires_at.strftime("%d/%m/%Y %H:%M:%S"),
                    inline=False
                )
                
                embed.add_field(
                    name="⏱ Días Restantes",
                    value=str(max(0, days_left)),
                    inline=False
                )
                
                embed.add_field(
                    name="🔑 Claves Activadas",
                    value=str(info.get("activated_keys", 0)),
                    inline=False
                )
            else:
                embed.add_field(
                    name="💡 Sugerencia",
                    value="Obtén premium para desbloquear funciones exclusivas\n`/premium info` - Ver beneficios",
                    inline=False
                )
            
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(ctx.author.id, "premium_status", str(e))
            embed = create_error_embed("❌ Error", str(e))
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="premium_command", description="Comando exclusivo premium")
    @premium_only()
    async def premium_command(self, ctx):
        try:
            log_command(ctx.author.id, "premium_command", {})
            
            embed = create_success_embed(
                "✨ Comando Premium Ejecutado",
                "Este es un comando exclusivo para usuarios premium"
            )
            
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(ctx.author.id, "premium_command", str(e))
            embed = create_error_embed("❌ Error", str(e))
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="features", description="Ver características por suscripción")
    async def features(self, ctx):
        try:
            log_command(ctx.author.id, "features", {})
            
            embed = discord.Embed(
                title="✨ Características del Bot",
                color=COLORS["primary"]
            )
            
            for feature, limits in PREMIUM_FEATURES.items():
                free_limit = limits["free"]
                premium_limit = limits["premium"]
                
                free_display = "Deshabilitado" if free_limit is False else f"{free_limit}" if isinstance(free_limit, int) else "Limitado"
                premium_display = "Habilitado" if premium_limit is True else f"Ilimitado" if premium_limit is None else f"{premium_limit}"
                
                feature_name = feature.replace("_", " ").title()
                embed.add_field(
                    name=f"{'🟢' if premium_limit is True or premium_limit is None else '🟡'} {feature_name}",
                    value=f"**Free**: {free_display}\n**Premium**: {premium_display}",
                    inline=False
                )
            
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(ctx.author.id, "features", str(e))
            embed = create_error_embed("❌ Error", str(e))
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Premium(bot))
