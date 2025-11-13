import discord
from discord.ext import commands
import db
from utils import create_success_embed, create_error_embed, create_info_embed
from logger import log_command, log_error
from config import COLORS

RADIO_STATIONS = {
    "lofi": {"name": "Lo-Fi Hip Hop", "genre": "Lo-Fi", "description": "Música relajante para estudiar"},
    "edm": {"name": "Electronic Dance Music", "genre": "EDM", "description": "Música electrónica de alta energía"},
    "indie": {"name": "Indie Rock", "genre": "Indie", "description": "Bandas independientes de rock"},
    "jazz": {"name": "Jazz Classics", "genre": "Jazz", "description": "Clásicos del jazz"},
    "pop": {"name": "Pop Hits", "genre": "Pop", "description": "Los éxitos del pop actual"},
    "metal": {"name": "Heavy Metal", "genre": "Metal", "description": "Rock y metal pesado"},
    "country": {"name": "Country Roads", "genre": "Country", "description": "Música country clásica"},
    "hiphop": {"name": "Hip-Hop Beats", "genre": "Hip-Hop", "description": "Hip-hop y rap moderno"},
    "rnb": {"name": "R&B Smooth", "genre": "R&B", "description": "R&B suave y romántico"},
    "reggae": {"name": "Reggae Vibes", "genre": "Reggae", "description": "Reggae y ska relajante"},
}

class Radio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_stations = {}

    @commands.hybrid_group(name="radio", description="Gestiona radiociones")
    async def radio(self, ctx):
        pass

    @radio.command(name="list", description="Lista todas las radiociones disponibles")
    async def list_stations(self, ctx):
        log_command(ctx.author, "radio list", ctx.guild.name)
        
        embed = discord.Embed(
            title="📻 Radiociones Disponibles",
            color=COLORS["primary"],
            description="Estaciones de radio personalizadas"
        )
        
        for key, station in RADIO_STATIONS.items():
            embed.add_field(
                name=f"/radio play {key}",
                value=f"**{station['name']}** - {station['description']}",
                inline=False
            )
        
        embed.set_footer(text="Usa /radio play <estación> para empezar")
        await ctx.send(embed=embed)

    @radio.command(name="play", description="Reproduce una estación de radio")
    async def play_station(self, ctx, station: str):
        log_command(ctx.author, f"radio play {station}", ctx.guild.name)
        
        if station not in RADIO_STATIONS:
            embed = create_error_embed(
                f"Estación no encontrada. Usa `/radio list` para ver opciones",
                "Radio"
            )
            return await ctx.send(embed=embed)
        
        if not ctx.author.voice:
            embed = create_error_embed("Debes estar en un canal de voz", "Radio")
            return await ctx.send(embed=embed)
        
        station_info = RADIO_STATIONS[station]
        
        embed = create_success_embed(
            f"📻 Reproduciendo {station_info['name']}",
            f"🎵 Género: **{station_info['genre']}**\n{station_info['description']}"
        )
        
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/825/825532.png")
        await ctx.send(embed=embed)
        
        self.active_stations[ctx.guild.id] = {
            "station": station,
            "user": ctx.author.id,
            "info": station_info
        }

    @radio.command(name="current", description="Muestra la estación actual")
    async def current_station(self, ctx):
        log_command(ctx.author, "radio current", ctx.guild.name)
        
        current = self.active_stations.get(ctx.guild.id)
        
        if not current:
            embed = create_error_embed("No hay estación activa", "Radio")
            return await ctx.send(embed=embed)
        
        info = current["info"]
        embed = discord.Embed(
            title=f"📻 {info['name']}",
            description=info['description'],
            color=COLORS["primary"]
        )
        
        embed.add_field(name="Género", value=info['genre'], inline=True)
        embed.add_field(name="Estado", value="🔴 En vivo", inline=True)
        
        await ctx.send(embed=embed)

    @radio.command(name="stop", description="Detiene la estación de radio")
    async def stop_station(self, ctx):
        log_command(ctx.author, "radio stop", ctx.guild.name)
        
        if ctx.guild.id in self.active_stations:
            del self.active_stations[ctx.guild.id]
            embed = create_success_embed("📻 Estación detenida", "")
        else:
            embed = create_error_embed("No hay estación activa", "Radio")
        
        await ctx.send(embed=embed)

    @radio.command(name="info", description="Información sobre una estación")
    async def station_info(self, ctx, station: str):
        log_command(ctx.author, f"radio info {station}", ctx.guild.name)
        
        if station not in RADIO_STATIONS:
            embed = create_error_embed(f"Estación no encontrada: {station}", "Radio Info")
            return await ctx.send(embed=embed)
        
        info = RADIO_STATIONS[station]
        
        embed = discord.Embed(
            title=f"📻 {info['name']}",
            description=info['description'],
            color=COLORS["primary"]
        )
        
        embed.add_field(name="Código", value=f"`{station}`", inline=True)
        embed.add_field(name="Género", value=info['genre'], inline=True)
        embed.add_field(name="Comando", value=f"`/radio play {station}`", inline=False)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Radio(bot))
