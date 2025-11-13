import discord
from discord.ext import commands
import asyncio
from config import DISCORD_TOKEN, COMMAND_PREFIX, COLORS
from db import init_db
from logger import logger
import os
import sys

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(
    command_prefix=COMMAND_PREFIX,
    intents=intents,
    help_command=None,
    sync_commands_debug=False
)

@bot.event
async def on_ready():
    logger.info(f"✅ Bot conectado como {bot.user}")
    logger.info(f"📊 Guilds: {len(bot.guilds)}")
    logger.info(f"🔄 Cogs cargados: {len(bot.cogs)}")
    
    try:
        synced = await bot.tree.sync()
        logger.info(f"✅ {len(synced)} comandos sincronizados")
    except Exception as e:
        logger.error(f"Error al sincronizar comandos: {e}")
    
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name="🎵 /play | /language"
        )
    )

@bot.event
async def on_error(event, *args, **kwargs):
    logger.error(f"Error en evento {event}", exc_info=True)

@bot.event
async def on_voice_state_update(member, before, after):
    if member == bot.user and not after.channel:
        guild = member.guild
        vc = guild.voice_client
        if vc:
            await vc.disconnect()

@bot.event
async def on_command_error(ctx, error):
    logger.error(f"Error en comando: {error}", exc_info=True)
    embed = discord.Embed(
        title="❌ Error",
        description=str(error)[:200],
        color=COLORS["error"]
    )
    try:
        await ctx.send(embed=embed)
    except:
        pass

async def load_cogs():
    cogs_dir = './cogs'
    
    if not os.path.exists(cogs_dir):
        os.makedirs(cogs_dir)
        logger.warning("Carpeta cogs no encontrada, creada")
        return
    
    for filename in os.listdir(cogs_dir):
        if filename.endswith('.py') and not filename.startswith('_'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f"✅ Cog cargado: {filename[:-3]}")
            except Exception as e:
                logger.error(f"❌ Error al cargar {filename}: {e}")

async def main():
    try:
        async with bot:
            await init_db()
            logger.info("✅ Base de datos inicializada")
            
            await load_cogs()
            logger.info("✅ Cogs cargados")
            
            await bot.start(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Error fatal: {e}", exc_info=True)
        sys.exit(1)
    finally:
        from db import close_db
        await close_db()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot detenido por el usuario")
    except Exception as e:
        logger.error(f"Error no manejado: {e}", exc_info=True)
