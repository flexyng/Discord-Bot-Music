import discord
from discord.ext import commands
from utils import create_success_embed, create_error_embed, create_info_embed, owner_only
from logger import log_command, log_error
from config import COLORS
import db

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="generate_keys", description="[OWNER] Generar claves premium")
    @owner_only()
    async def generate_keys(self, ctx, amount: int = 1, duration: int = 30):
        try:
            log_command(ctx.author.id, "generate_keys", {"amount": amount, "duration": duration})
            
            if amount < 1 or amount > 100:
                embed = create_error_embed("❌ Error", "La cantidad debe estar entre 1 y 100")
                await ctx.send(embed=embed)
                return
            
            keys = []
            for i in range(amount):
                key = await db.generate_premium_key(duration)
                keys.append(key)
            
            embed = create_success_embed(
                "✅ Claves Generadas",
                f"Se han generado {amount} claves de {duration} días de duración."
            )
            
            keys_text = "\n".join(keys)
            embed.add_field(name="🔑 Claves", value=f"```\n{keys_text}\n```", inline=False)
            
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(ctx.author.id, "generate_keys", str(e))
            embed = create_error_embed("❌ Error", str(e))
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="view_keys", description="[OWNER] Ver todas las claves premium")
    @owner_only()
    async def view_keys(self, ctx):
        try:
            log_command(ctx.author.id, "view_keys", {})
            
            keys = await db.get_premium_keys_info()
            
            if not keys:
                embed = create_error_embed("❌ Sin claves", "No hay claves generadas")
                await ctx.send(embed=embed)
                return
            
            embed = discord.Embed(
                title="🔑 Gestión de Claves Premium",
                color=COLORS["primary"]
            )
            
            active_keys = [k for k in keys if k.get("is_active")]
            used_keys = [k for k in keys if k.get("redeemed_by")]
            
            embed.add_field(
                name="📊 Estadísticas",
                value=f"**Total**: {len(keys)}\n**Activas**: {len(active_keys)}\n**Utilizadas**: {len(used_keys)}",
                inline=False
            )
            
            if active_keys:
                available = [k for k in active_keys if not k.get("redeemed_by")]
                if available:
                    keys_list = "\n".join([f"`{k['key']}` - {k['duration_days']}d" for k in available[:10]])
                    embed.add_field(
                        name="🟢 Claves Disponibles",
                        value=keys_list if available else "Ninguna",
                        inline=False
                    )
            
            if used_keys:
                used_list = "\n".join([f"`{k['key']}` - Usuario: {k['redeemed_by']}" for k in used_keys[:5]])
                embed.add_field(
                    name="🔴 Claves Utilizadas",
                    value=used_list,
                    inline=False
                )
            
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(ctx.author.id, "view_keys", str(e))
            embed = create_error_embed("❌ Error", str(e))
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="deactivate_key", description="[OWNER] Desactivar una clave premium")
    @owner_only()
    async def deactivate_key(self, ctx, key: str):
        try:
            log_command(ctx.author.id, "deactivate_key", {"key": key})
            
            result = await db.deactivate_premium_key(key)
            
            if result:
                embed = create_success_embed(
                    "✅ Clave Desactivada",
                    f"La clave `{key}` ha sido desactivada exitosamente"
                )
            else:
                embed = create_error_embed(
                    "❌ Error",
                    f"No se pudo desactivar la clave `{key}`"
                )
            
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(ctx.author.id, "deactivate_key", str(e))
            embed = create_error_embed("❌ Error", str(e))
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="extend_premium", description="[OWNER] Extender premium a un usuario")
    @owner_only()
    async def extend_premium(self, ctx, user: discord.User, days: int = 30):
        try:
            log_command(ctx.author.id, "extend_premium", {"user": user.id, "days": days})
            
            if days < 1 or days > 365:
                embed = create_error_embed("❌ Error", "Los días deben estar entre 1 y 365")
                await ctx.send(embed=embed)
                return
            
            success, expires_at = await db.extend_premium(user.id, days)
            
            if success:
                embed = create_success_embed(
                    "✅ Premium Extendido",
                    f"Premium extendido a {user.mention} por {days} días"
                )
                embed.add_field(
                    name="📅 Vence",
                    value=expires_at.strftime("%d/%m/%Y %H:%M:%S"),
                    inline=False
                )
            else:
                embed = create_error_embed("❌ Error", "No se pudo extender premium")
            
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(ctx.author.id, "extend_premium", str(e))
            embed = create_error_embed("❌ Error", str(e))
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="check_premium", description="[OWNER] Verificar estado premium de un usuario")
    @owner_only()
    async def check_premium(self, ctx, user: discord.User):
        try:
            log_command(ctx.author.id, "check_premium", {"user": user.id})
            
            is_premium = await db.is_premium(user.id)
            info = await db.get_premium_info(user.id)
            
            embed = discord.Embed(
                title=f"📊 Estado Premium - {user}",
                color=COLORS["premium"] if is_premium else COLORS["error"]
            )
            
            embed.add_field(
                name="Estado",
                value="✅ Premium" if is_premium else "❌ Free",
                inline=False
            )
            
            if info and info.get("premium_expires_at"):
                embed.add_field(
                    name="📅 Vence",
                    value=info["premium_expires_at"].strftime("%d/%m/%Y %H:%M:%S"),
                    inline=False
                )
                embed.add_field(
                    name="🔑 Claves Activadas",
                    value=str(info.get("activated_keys", 0)),
                    inline=False
                )
            
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(ctx.author.id, "check_premium", str(e))
            embed = create_error_embed("❌ Error", str(e))
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="bot_stats", description="[OWNER] Ver estadísticas del bot")
    @owner_only()
    async def bot_stats(self, ctx):
        try:
            log_command(ctx.author.id, "bot_stats", {})
            
            embed = discord.Embed(
                title="📊 Estadísticas del Bot",
                color=COLORS["primary"]
            )
            
            embed.add_field(
                name="🔗 Conexiones",
                value=f"Servidores: {len(self.bot.guilds)}\nMiembros: {sum(g.member_count for g in self.bot.guilds if g.member_count)}",
                inline=False
            )
            
            embed.add_field(
                name="⚙️ Sistema",
                value=f"Cogs: {len(self.bot.cogs)}\nComandos: {len(self.bot.commands)}\nLATENCY: {round(self.bot.latency * 1000)}ms",
                inline=False
            )
            
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(ctx.author.id, "bot_stats", str(e))
            embed = create_error_embed("❌ Error", str(e))
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="reload_cog", description="[OWNER] Recargar un cog")
    @owner_only()
    async def reload_cog(self, ctx, cog_name: str):
        try:
            log_command(ctx.author.id, "reload_cog", {"cog": cog_name})
            
            try:
                await self.bot.reload_extension(f"cogs.{cog_name}")
                embed = create_success_embed(
                    "✅ Cog Recargado",
                    f"El cog `{cog_name}` ha sido recargado exitosamente"
                )
            except commands.ExtensionNotLoaded:
                embed = create_error_embed("❌ Error", f"El cog `{cog_name}` no estaba cargado")
            except commands.ExtensionNotFound:
                embed = create_error_embed("❌ Error", f"El cog `{cog_name}` no existe")
            except Exception as e:
                embed = create_error_embed("❌ Error", f"Error recargando cog: {str(e)}")
            
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(ctx.author.id, "reload_cog", str(e))
            embed = create_error_embed("❌ Error", str(e))
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="owner_help", description="[OWNER] Ver ayuda de comandos de owner")
    @owner_only()
    async def owner_help(self, ctx):
        try:
            embed = discord.Embed(
                title="👑 Comandos de Owner",
                color=COLORS["primary"],
                description="Comandos exclusivos para propietarios del bot"
            )
            
            embed.add_field(
                name="🔑 Gestión de Premium",
                value="""
`/generate_keys [cantidad] [días]` - Generar claves premium
`/view_keys` - Ver todas las claves
`/deactivate_key <key>` - Desactivar una clave
`/extend_premium <usuario> [días]` - Extender premium a usuario
`/check_premium <usuario>` - Ver estado premium
""",
                inline=False
            )
            
            embed.add_field(
                name="⚙️ Sistema",
                value="""
`/bot_stats` - Estadísticas del bot
`/reload_cog <nombre>` - Recargar un cog
`/owner_help` - Este mensaje
""",
                inline=False
            )
            
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(ctx.author.id, "owner_help", str(e))
            embed = create_error_embed("❌ Error", str(e))
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Owner(bot))
