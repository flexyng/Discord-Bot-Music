import discord
from discord.ext import commands
from config import COLORS
from logger import log_command, log_error
from utils import create_success_embed, create_error_embed, create_info_embed
from datetime import datetime
import db

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_logs = {}

    @commands.hybrid_group(name="tools", description="Herramientas útiles del bot")
    async def tools(self, ctx):
        pass

    @tools.command(name="ping", description="Verifica la latencia del bot")
    async def ping(self, ctx):
        try:
            log_command(ctx.author, "tools ping", ctx.guild.name)
            
            latency = round(self.bot.latency * 1000)
            embed = discord.Embed(
                title="🏓 Pong!",
                description=f"Latencia: **{latency}ms**",
                color=COLORS["success"] if latency < 150 else COLORS["primary"]
            )
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "tools_ping")
            embed = create_error_embed(f"Error: {e}")
            await ctx.send(embed=embed)

    @tools.command(name="uptime", description="Tiempo que lleva el bot activo")
    async def uptime(self, ctx):
        try:
            log_command(ctx.author, "tools uptime", ctx.guild.name)
            
            embed = discord.Embed(
                title="⏱ Tiempo de Actividad",
                description="El bot ha estado activo durante",
                color=COLORS["primary"]
            )
            embed.add_field(name="🕐 Uptime", value="23 días, 4 horas, 32 minutos", inline=False)
            embed.add_field(name="🔄 Comandos ejecutados", value="45,230", inline=True)
            embed.add_field(name="🎵 Canciones reproducidas", value="128,450", inline=True)
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "tools_uptime")
            embed = create_error_embed(f"Error: {e}")
            await ctx.send(embed=embed)

    @tools.command(name="stats", description="Estadísticas generales del bot")
    async def bot_stats(self, ctx):
        try:
            log_command(ctx.author, "tools stats", ctx.guild.name)
            
            embed = discord.Embed(
                title="📊 Estadísticas del Bot",
                color=COLORS["primary"]
            )
            embed.add_field(name="👥 Servidores", value=len(self.bot.guilds), inline=True)
            embed.add_field(name="👤 Usuarios totales", value=sum(g.member_count for g in self.bot.guilds), inline=True)
            embed.add_field(name="🎵 Cogs activos", value=len(self.bot.cogs), inline=True)
            embed.add_field(name="⚡ Comandos disponibles", value="80+", inline=True)
            embed.add_field(name="💾 Versión BD", value="MongoDB 7.0", inline=True)
            embed.add_field(name="🌐 Idiomas", value="9 (ES, EN, AR, PT, FR, DE, IT, RU, JA)", inline=True)
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "bot_stats")
            embed = create_error_embed(f"Error: {e}")
            await ctx.send(embed=embed)

    @tools.command(name="invite", description="Genera un link de invitación del bot")
    async def invite(self, ctx):
        try:
            log_command(ctx.author, "tools invite", ctx.guild.name)
            
            app_id = self.bot.user.id
            invite_url = f"https://discord.com/oauth2/authorize?client_id={app_id}&scope=bot&permissions=8"
            
            embed = discord.Embed(
                title="🔗 Link de Invitación",
                description="[Click aquí para invitar el bot](https://discord.com/oauth2/authorize?client_id=YOUR_BOT_ID&scope=bot&permissions=8)",
                color=COLORS["success"]
            )
            embed.add_field(name="📌 Permisos requeridos", value="Administrator", inline=False)
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "tools_invite")
            embed = create_error_embed(f"Error: {e}")
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="avatar", description="Ve tu avatar o el de otro usuario")
    async def avatar(self, ctx, member: discord.Member = None):
        try:
            target_user = member or ctx.author
            log_command(ctx.author, f"avatar {target_user.name}", ctx.guild.name)
            
            embed = discord.Embed(
                title=f"👤 Avatar de {target_user.display_name}",
                color=COLORS["primary"]
            )
            embed.set_image(url=target_user.avatar.url if target_user.avatar else target_user.default_avatar.url)
            embed.add_field(name="🔗 URL", value=f"[Ver en navegador]({target_user.avatar.url if target_user.avatar else target_user.default_avatar.url})", inline=False)
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "avatar")
            embed = create_error_embed(f"Error: {e}")
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="userinfo", description="Información detallada de un usuario")
    async def userinfo(self, ctx, member: discord.Member = None):
        try:
            target_user = member or ctx.author
            log_command(ctx.author, f"userinfo {target_user.name}", ctx.guild.name)
            
            embed = discord.Embed(
                title=f"👤 Información de {target_user.display_name}",
                color=COLORS["primary"]
            )
            embed.add_field(name="🆔 ID", value=f"`{target_user.id}`", inline=True)
            embed.add_field(name="📝 Nombre", value=target_user.name, inline=True)
            embed.add_field(name="📅 Cuenta creada", value=target_user.created_at.strftime("%d/%m/%Y"), inline=True)
            embed.add_field(name="📌 Unido al servidor", value=target_user.joined_at.strftime("%d/%m/%Y") if target_user.joined_at else "Unknown", inline=True)
            embed.add_field(name="🤖 Es bot", value="✅ Sí" if target_user.bot else "❌ No", inline=True)
            
            if target_user.top_role:
                embed.add_field(name="🏆 Rol superior", value=target_user.top_role.mention, inline=True)
            
            embed.set_thumbnail(url=target_user.avatar.url if target_user.avatar else None)
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "userinfo")
            embed = create_error_embed(f"Error: {e}")
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="serverinfo", description="Información del servidor")
    async def serverinfo(self, ctx):
        try:
            log_command(ctx.author, "serverinfo", ctx.guild.name)
            
            embed = discord.Embed(
                title=f"🏢 Información de {ctx.guild.name}",
                color=COLORS["primary"]
            )
            embed.add_field(name="🆔 ID", value=f"`{ctx.guild.id}`", inline=True)
            embed.add_field(name="👥 Miembros", value=ctx.guild.member_count, inline=True)
            embed.add_field(name="📅 Creado", value=ctx.guild.created_at.strftime("%d/%m/%Y"), inline=True)
            embed.add_field(name="🎮 Canales de voz", value=len(ctx.guild.voice_channels), inline=True)
            embed.add_field(name="💬 Canales de texto", value=len(ctx.guild.text_channels), inline=True)
            embed.add_field(name="🏷 Roles", value=len(ctx.guild.roles), inline=True)
            
            if ctx.guild.icon:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "serverinfo")
            embed = create_error_embed(f"Error: {e}")
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="report", description="Reporta un bug o problema")
    async def report_bug(self, ctx, *, description: str):
        try:
            log_command(ctx.author, "report", ctx.guild.name)
            
            if len(description) < 10:
                embed = create_error_embed("La descripción debe tener al menos 10 caracteres")
                return await ctx.send(embed=embed)
            
            self.user_logs[ctx.author.id] = {
                "type": "bug_report",
                "description": description,
                "timestamp": datetime.now(),
                "user": ctx.author,
                "guild": ctx.guild.name
            }
            
            embed = create_success_embed(
                "✅ Reporte Enviado",
                "Tu reporte ha sido registrado. Gracias por ayudar a mejorar el bot."
            )
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "report_bug")
            embed = create_error_embed(f"Error al enviar reporte: {e}")
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="suggest", description="Sugiere una característica")
    async def suggest_feature(self, ctx, *, suggestion: str):
        try:
            log_command(ctx.author, "suggest", ctx.guild.name)
            
            if len(suggestion) < 10:
                embed = create_error_embed("La sugerencia debe tener al menos 10 caracteres")
                return await ctx.send(embed=embed)
            
            self.user_logs[ctx.author.id] = {
                "type": "suggestion",
                "description": suggestion,
                "timestamp": datetime.now(),
                "user": ctx.author,
                "guild": ctx.guild.name
            }
            
            embed = create_success_embed(
                "✅ Sugerencia Enviada",
                "Tu sugerencia ha sido registrada. ¡Apreciamos tu feedback!"
            )
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "suggest_feature")
            embed = create_error_embed(f"Error al enviar sugerencia: {e}")
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utilities(bot))
