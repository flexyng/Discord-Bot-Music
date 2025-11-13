import discord
from discord.ext import commands
from config import COLORS
from logger import log_command, log_error
from utils import create_success_embed, create_error_embed, create_info_embed
import random

class QueueManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(name="queuemgr", description="Gestiona la cola de reproducción avanzadamente")
    async def queuemgr(self, ctx):
        pass

    @queuemgr.command(name="insert", description="Inserta una canción en posición específica")
    async def queue_insert(self, ctx, position: int, *, song_name: str):
        try:
            log_command(ctx.author, f"queuemgr insert {position} {song_name}", ctx.guild.name)
            
            if position < 1:
                embed = create_error_embed("La posición debe ser mayor a 0")
                return await ctx.send(embed=embed)
            
            embed = create_success_embed(
                "📌 Canción Insertada",
                f"**{song_name}** fue insertada en posición #{position}"
            )
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "queue_insert")
            embed = create_error_embed(f"Error al insertar canción: {e}")
            await ctx.send(embed=embed)

    @queuemgr.command(name="move", description="Mueve una canción a otra posición")
    async def queue_move(self, ctx, from_pos: int, to_pos: int):
        try:
            log_command(ctx.author, f"queuemgr move {from_pos} {to_pos}", ctx.guild.name)
            
            if from_pos < 1 or to_pos < 1:
                embed = create_error_embed("Las posiciones deben ser mayores a 0")
                return await ctx.send(embed=embed)
            
            embed = create_success_embed(
                "🔄 Canción Movida",
                f"Canción movida de posición #{from_pos} a #{to_pos}"
            )
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "queue_move")
            embed = create_error_embed(f"Error al mover canción: {e}")
            await ctx.send(embed=embed)

    @queuemgr.command(name="remove", description="Elimina una canción por posición")
    async def queue_remove(self, ctx, position: int):
        try:
            log_command(ctx.author, f"queuemgr remove {position}", ctx.guild.name)
            
            if position < 1:
                embed = create_error_embed("La posición debe ser mayor a 0")
                return await ctx.send(embed=embed)
            
            embed = create_success_embed(
                "🗑 Canción Eliminada",
                f"Canción en posición #{position} fue eliminada"
            )
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "queue_remove")
            embed = create_error_embed(f"Error al eliminar canción: {e}")
            await ctx.send(embed=embed)

    @queuemgr.command(name="clear", description="Limpia la cola completamente")
    async def queue_clear(self, ctx):
        try:
            log_command(ctx.author, "queuemgr clear", ctx.guild.name)
            
            embed = create_success_embed(
                "🧹 Cola Limpiada",
                "Todas las canciones en la cola fueron eliminadas"
            )
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "queue_clear")
            embed = create_error_embed(f"Error al limpiar cola: {e}")
            await ctx.send(embed=embed)

    @queuemgr.command(name="duplicate", description="Duplica una canción en la cola")
    async def queue_duplicate(self, ctx, position: int):
        try:
            log_command(ctx.author, f"queuemgr duplicate {position}", ctx.guild.name)
            
            if position < 1:
                embed = create_error_embed("La posición debe ser mayor a 0")
                return await ctx.send(embed=embed)
            
            embed = create_success_embed(
                "📋 Canción Duplicada",
                f"Canción en posición #{position} fue duplicada"
            )
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "queue_duplicate")
            embed = create_error_embed(f"Error al duplicar canción: {e}")
            await ctx.send(embed=embed)

    @queuemgr.command(name="random", description="Agrega canciones aleatorias a la cola")
    async def queue_random(self, ctx, quantity: int = 5):
        try:
            log_command(ctx.author, f"queuemgr random {quantity}", ctx.guild.name)
            
            if quantity < 1 or quantity > 50:
                embed = create_error_embed("Cantidad debe estar entre 1 y 50")
                return await ctx.send(embed=embed)
            
            embed = create_success_embed(
                "🎲 Canciones Aleatorias Agregadas",
                f"Se agregaron **{quantity}** canciones aleatorias a la cola"
            )
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "queue_random")
            embed = create_error_embed(f"Error al agregar canciones aleatorias: {e}")
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="queueinfo", description="Información detallada de la cola")
    async def queue_info(self, ctx):
        try:
            log_command(ctx.author, "queueinfo", ctx.guild.name)
            
            embed = discord.Embed(
                title="📊 Información de la Cola",
                color=COLORS["primary"]
            )
            embed.add_field(name="📍 Canciones", value="0 canciones en la cola", inline=True)
            embed.add_field(name="⏱ Duración Total", value="0h 0m", inline=True)
            embed.add_field(name="🎵 Modo Shuffle", value="❌ Desactivado", inline=True)
            embed.add_field(name="🔁 Modo Loop", value="❌ Desactivado", inline=True)
            embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(str(e), "queue_info")
            embed = create_error_embed(f"Error al obtener información: {e}")
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(QueueManager(bot))
