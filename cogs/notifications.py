import discord
from discord.ext import commands, tasks
import db
from utils import create_info_embed, create_success_embed
from logger import log_command, log_error
from config import COLORS
from datetime import datetime
from collections import defaultdict

class Notifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_subscriptions = defaultdict(dict)
        self.notification_queue = []
        self.process_notifications.start()

    def cog_unload(self):
        self.process_notifications.cancel()

    @tasks.loop(seconds=30)
    async def process_notifications(self):
        """Procesa la cola de notificaciones periódicamente"""
        if self.notification_queue:
            for notification in self.notification_queue[:]:
                try:
                    user = self.bot.get_user(notification['user_id'])
                    if user:
                        embed = discord.Embed(
                            title=notification['title'],
                            description=notification['message'],
                            color=notification.get('color', COLORS["primary"])
                        )
                        embed.set_footer(text=f"Notificación • {datetime.now().strftime('%H:%M:%S')}")
                        
                        try:
                            await user.send(embed=embed)
                        except discord.Forbidden:
                            pass
                    
                    self.notification_queue.remove(notification)
                except Exception as e:
                    log_error(str(e), "process_notifications")

    @process_notifications.before_loop
    async def before_process_notifications(self):
        await self.bot.wait_until_ready()

    @commands.hybrid_group(name="notifications", description="Gestiona notificaciones")
    async def notifications(self, ctx):
        pass

    @notifications.command(name="settings", description="Configura tus notificaciones")
    async def notification_settings(self, ctx):
        log_command(ctx.author, "notifications settings", ctx.guild.name)
        
        settings = await db.get_user_settings(ctx.author.id)
        theme, notifications_enabled, autoplay, language = settings
        
        embed = discord.Embed(
            title="🔔 Configuración de Notificaciones",
            color=COLORS["primary"]
        )
        
        embed.add_field(
            name="Estado",
            value=f"{'✅ Activadas' if notifications_enabled else '❌ Desactivadas'}",
            inline=True
        )
        
        embed.add_field(
            name="Tipos disponibles",
            value="""
`now_playing` - Cuando empieza una canción
`queue_update` - Cuando la cola cambia
`favorite_added` - Cuando agregas un favorito
`milestone` - Cuando alcanzas un hito
`recommendation` - Cuando hay recomendaciones
""",
            inline=False
        )
        
        await ctx.send(embed=embed)

    @notifications.command(name="enable", description="Activa las notificaciones")
    async def enable_notifications(self, ctx):
        log_command(ctx.author, "notifications enable", ctx.guild.name)
        
        await db.update_user_settings(ctx.author.id, notifications=True)
        
        embed = create_success_embed(
            "🔔 Notificaciones Activadas",
            "Recibirás notificaciones en tu bandeja de entrada de Discord"
        )
        await ctx.send(embed=embed)
        
        self.send_notification(
            ctx.author.id,
            "🔔 ¡Notificaciones Activadas!",
            "Ahora recibirás notificaciones en tiempo real",
            COLORS["success"]
        )

    @notifications.command(name="disable", description="Desactiva las notificaciones")
    async def disable_notifications(self, ctx):
        log_command(ctx.author, "notifications disable", ctx.guild.name)
        
        await db.update_user_settings(ctx.author.id, notifications=False)
        
        embed = create_success_embed(
            "🔔 Notificaciones Desactivadas",
            "Ya no recibirás notificaciones"
        )
        await ctx.send(embed=embed)

    @notifications.command(name="test", description="Envía una notificación de prueba")
    async def test_notification(self, ctx):
        log_command(ctx.author, "notifications test", ctx.guild.name)
        
        settings = await db.get_user_settings(ctx.author.id)
        _, notifications_enabled, _, _ = settings
        
        if not notifications_enabled:
            embed = discord.Embed(
                title="❌ Notificaciones Desactivadas",
                description="Activa las notificaciones con `/notifications enable`",
                color=COLORS["error"]
            )
            return await ctx.send(embed=embed)
        
        embed = create_success_embed(
            "✅ Notificación de Prueba Enviada",
            "Revisa tus mensajes directos"
        )
        await ctx.send(embed=embed)
        
        self.send_notification(
            ctx.author.id,
            "🎵 Notificación de Prueba",
            "¡Las notificaciones están funcionando correctamente!",
            COLORS["success"]
        )

    def send_notification(self, user_id: int, title: str, message: str, color: int = COLORS["primary"]):
        """Agrega una notificación a la cola"""
        self.notification_queue.append({
            'user_id': user_id,
            'title': title,
            'message': message,
            'color': color,
            'timestamp': datetime.now()
        })

    @commands.hybrid_command(name="milestones", description="Ver tus hitos de reproducción")
    async def milestones(self, ctx):
        log_command(ctx.author, "milestones", ctx.guild.name)
        
        stats = await db.get_user_stats(ctx.author.id)
        total_plays, total_time, _, _ = stats
        
        embed = discord.Embed(
            title="🏆 Tus Hitos de Reproducción",
            color=COLORS["primary"]
        )
        
        milestones_data = [
            (10, "🎵 Primeras 10 Reproducciones", "Empezaste tu viaje musical"),
            (50, "🎶 50 Reproducciones", "¡Buen ritmo!"),
            (100, "🎼 Centenario", "100 canciones reproducidas"),
            (250, "🎤 250 Reproducciones", "¡Eres un verdadero melómano!"),
            (500, "🏅 500 Reproducciones", "¡Increíble dedicación!"),
            (1000, "👑 1000 Reproducciones", "¡Eres una leyenda!"),
        ]
        
        for milestone, title, description in milestones_data:
            if total_plays >= milestone:
                status = "✅"
            else:
                progress = int((total_plays / milestone) * 100)
                status = f"⏳ {progress}%"
            
            embed.add_field(
                name=f"{status} {title}",
                value=description,
                inline=False
            )
        
        embed.set_footer(text=f"Total de reproducciones: {total_plays}")
        
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="streak", description="Ver tu racha de escucha")
    async def listening_streak(self, ctx):
        log_command(ctx.author, "streak", ctx.guild.name)
        
        stats = await db.get_user_stats(ctx.author.id)
        total_plays, total_time, _, _ = stats
        
        hours = total_time // 3600
        minutes = (total_time % 3600) // 60
        
        embed = discord.Embed(
            title="🔥 Tu Racha de Escucha",
            color=COLORS["primary"]
        )
        
        embed.add_field(
            name="🎵 Reproducciones",
            value=f"{total_plays:,} canciones",
            inline=True
        )
        
        embed.add_field(
            name="⏱ Tiempo Total",
            value=f"{hours}h {minutes}m",
            inline=True
        )
        
        if total_plays > 0:
            avg_per_day = total_plays / 30
            embed.add_field(
                name="📊 Promedio Diario",
                value=f"{avg_per_day:.1f} canciones/día",
                inline=True
            )
        
        embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else None)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Notifications(bot))
