import discord
from config import COLORS
from typing import Optional
from datetime import datetime

def create_now_playing_embed(title: str, artist: str, duration: int, thumbnail: Optional[str] = None, requester = None, progress: int = 0, total: int = 0) -> discord.Embed:
    embed = discord.Embed(
        title=f"▶ {title[:60]}",
        color=COLORS["primary"]
    )
    
    embed.add_field(name="🎤 Artista", value=artist or "Desconocido", inline=True)
    embed.add_field(name="⏱ Duración", value=format_duration(duration), inline=True)
    
    if progress and total:
        bar = create_progress_bar(progress, total)
        embed.add_field(name="Progreso", value=bar, inline=False)
    
    footer_text = "Hecho por flexyng | BSD-3-Clause License"
    if requester:
        footer_text = f"Solicitado por {requester} • {footer_text}"
        embed.set_footer(text=footer_text, icon_url=requester.avatar.url if requester.avatar else None)
    else:
        embed.set_footer(text=footer_text)
    
    if thumbnail:
        embed.set_image(url=thumbnail)
    
    return embed

def create_queue_embed(songs: list, page: int = 1) -> discord.Embed:
    embed = discord.Embed(
        title="🎵 Cola de reproducción",
        color=COLORS["primary"]
    )
    
    if not songs:
        embed.description = "La cola está vacía"
        embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
        return embed
    
    start = (page - 1) * 8
    end = start + 8
    
    description = ""
    for i, song in enumerate(songs[start:end], start=start+1):
        duration = format_duration(song.get('duration', 0)) if isinstance(song, dict) else format_duration(song[5] if len(song) > 5 else 0)
        title = song.get('title', song[0]) if isinstance(song, dict) else song[0]
        description += f"`{i:2d}.` **{title[:45]}** | {duration}\n"
    
    embed.description = description
    
    total_pages = (len(songs) - 1) // 8 + 1
    if total_pages > 1:
        embed.set_footer(text=f"Página {page}/{total_pages} • Total: {len(songs)} canciones • Hecho por flexyng")
    else:
        embed.set_footer(text=f"Total: {len(songs)} canción(es) • Hecho por flexyng")
    
    return embed

def create_error_embed(message: str, title: str = "Error") -> discord.Embed:
    embed = discord.Embed(
        title=f"❌ {title}",
        description=message,
        color=COLORS["error"]
    )
    embed.set_footer(text=f"Timestamp: {datetime.now().strftime('%H:%M:%S')} • Hecho por flexyng")
    return embed

def create_success_embed(title: str, message: str) -> discord.Embed:
    embed = discord.Embed(
        title=f"✅ {title}",
        description=message,
        color=COLORS["success"]
    )
    embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
    return embed

def create_info_embed(title: str, message: str) -> discord.Embed:
    embed = discord.Embed(
        title=f"ℹ {title}",
        description=message,
        color=0x2E86DE
    )
    embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
    return embed

def create_stats_embed(user, stats: tuple) -> discord.Embed:
    total_plays, total_time, favorite_genre, favorite_artist = stats
    
    hours = total_time // 3600 if total_time else 0
    minutes = (total_time % 3600) // 60 if total_time else 0
    
    embed = discord.Embed(
        title=f"📊 Estadísticas de {user.display_name}",
        color=COLORS["primary"]
    )
    
    embed.add_field(name="▶ Reproducciones totales", value=f"{total_plays:,}", inline=True)
    embed.add_field(name="⏱ Tiempo total", value=f"{hours}h {minutes}m", inline=True)
    embed.add_field(name="⭐ Género favorito", value=favorite_genre or "No disponible", inline=True)
    embed.add_field(name="🎤 Artista favorito", value=favorite_artist or "No disponible", inline=True)
    
    embed.set_thumbnail(url=user.avatar.url if user.avatar else None)
    embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
    return embed

def create_playlist_embed(playlist_name: str, songs: list, user) -> discord.Embed:
    embed = discord.Embed(
        title=f"📋 {playlist_name}",
        color=COLORS["primary"]
    )
    
    if not songs:
        embed.description = "Esta playlist está vacía"
        embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
        return embed
    
    description = ""
    for i, song in enumerate(songs[:10], 1):
        duration = format_duration(song[5]) if len(song) > 5 else ""
        description += f"`{i:2d}.` **{song[1][:40]}** | {duration}\n"
    
    if len(songs) > 10:
        description += f"\n*... y {len(songs) - 10} más*"
    
    embed.description = description
    embed.set_footer(text=f"Total: {len(songs)} canciones • Por {user.display_name} • Hecho por flexyng")
    
    return embed

def format_duration(seconds: int) -> str:
    if seconds < 0:
        return "🔴 Transmisión en vivo"
    
    mins, secs = divmod(int(seconds), 60)
    hours, mins = divmod(mins, 60)
    
    if hours > 0:
        return f"{hours}:{mins:02d}:{secs:02d}"
    return f"{mins}:{secs:02d}"

def create_progress_bar(current: int, total: int, bar_length: int = 20) -> str:
    if total == 0:
        return "▯" * bar_length
    
    filled = int(bar_length * current / total)
    bar = "▰" * filled + "▯" * (bar_length - filled)
    percentage = int(100 * current / total)
    
    return f"{bar} {percentage}%"

def create_favorites_embed(favorites: list, user) -> discord.Embed:
    embed = discord.Embed(
        title=f"❤ Canciones favoritas de {user.display_name}",
        color=COLORS["primary"]
    )
    
    if not favorites:
        embed.description = "No tienes canciones favoritas"
        embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
        return embed
    
    description = ""
    for i, fav in enumerate(favorites[:15], 1):
        title = fav[0][:40]
        artist = fav[1] or "Desconocido"
        plays = fav[5] if len(fav) > 5 else 0
        description += f"`{i:2d}.` **{title}** - {artist} ({plays} plays)\n"
    
    embed.description = description
    if len(favorites) > 15:
        embed.set_footer(text=f"Mostrando 15 de {len(favorites)} favoritos • Hecho por flexyng")
    else:
        embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
    
    return embed

def create_help_embed() -> discord.Embed:
    embed = discord.Embed(
        title="🎵 Ayuda - Comandos disponibles",
        color=COLORS["primary"],
        description="Lista completa de comandos del bot de música v1.3.0"
    )
    
    embed.add_field(
        name="🎶 Reproducción",
        value="""
`/play <canción>` - Reproduce una canción
`/pause` - Pausa la música
`/resume` - Reanuda la música
`/skip` - Salta la canción actual
`/stop` - Detiene la música
`/queue` - Muestra la cola
`/shuffle` - Activa/desactiva shuffle
`/loop` - Cambia modo de repetición
`/volume <0-100>` - Ajusta volumen
`/nowplaying` - Canción actual
""",
        inline=False
    )
    
    embed.add_field(
        name="❤ Favoritos",
        value="""
`/favorite add <canción>` - Agrega a favoritos
`/favorite remove <canción>` - Elimina de favoritos
`/favorite list` - Muestra tus favoritos
""",
        inline=False
    )
    
    embed.add_field(
        name="📋 Playlists",
        value="""
`/playlist create <nombre>` - Crea playlist
`/playlist list` - Lista tus playlists
`/playlist delete <nombre>` - Elimina playlist
""",
        inline=False
    )
    
    embed.add_field(
        name="🎛 Gestor de Cola",
        value="""
`/queuemgr insert <pos> <canción>` - Inserta en posición
`/queuemgr move <from> <to>` - Mueve canción
`/queuemgr remove <posición>` - Elimina de posición
`/queuemgr clear` - Limpia la cola
`/queuemgr duplicate <pos>` - Duplica canción
`/queuemgr random <cantidad>` - Agrega aleatorias
`/queueinfo` - Info de la cola
""",
        inline=False
    )
    
    embed.add_field(
        name="🏆 Leaderboards",
        value="""
`/leaderboard plays` - Top reproducciones
`/leaderboard time` - Top horas
`/leaderboard songs` - Canciones populares
`/leaderboard artists` - Artistas populares
`/leaderboard genres` - Géneros populares
`/myrank` - Tu ranking personal
""",
        inline=False
    )
    
    embed.add_field(
        name="📊 Analítica de Playlists",
        value="""
`/playlistinfo analyze <playlist>` - Analiza playlist
`/playlistinfo diversity <playlist>` - Diversidad
`/playlistinfo genres <playlist>` - Desglose géneros
`/playlistinfo popularity <playlist>` - Popularidad
`/playlistinfo timeline <playlist>` - Línea temporal
`/plstats` - Tus estadísticas
`/plcompare <pl1> <pl2>` - Compara playlists
""",
        inline=False
    )
    
    embed.add_field(
        name="🔧 Herramientas",
        value="""
`/tools ping` - Latencia del bot
`/tools uptime` - Tiempo de actividad
`/tools stats` - Estadísticas bot
`/tools invite` - Link de invitación
`/avatar [@user]` - Ver avatar
`/userinfo [@user]` - Info de usuario
`/serverinfo` - Info del servidor
`/report <descripción>` - Reportar bug
`/suggest <descripción>` - Sugerir feature
""",
        inline=False
    )
    
    embed.add_field(
        name="🎪 Características Avanzadas",
        value="""
`/djmode enable [rol]` - Modo DJ
`/musicbattle start [@usuario]` - Batalla musical
`/trivia` - Trivia musical
`/songanalysis <canción>` - Análisis de canción
`/moodradio [happy|sad|energetic|chill]` - Radio por mood
`/musicstats [@user]` - Estadísticas musicales
""",
        inline=False
    )
    
    embed.add_field(
        name="🤝 Colaboración",
        value="""
`/collab start <nombre>` - Sesión colaborativa
`/collab join <id>` - Unirse a sesión
`/collab add <id> <canción>` - Agregar canción
`/request add <canción>` - Solicitar canción
`/request list` - Ver solicitudes
`/suggest artist <artista>` - Sugerir artista
`/suggest genre <género>` - Sugerir género
""",
        inline=False
    )
    
    embed.add_field(
        name="🔍 Búsqueda y Recomendaciones",
        value="""
`/search [youtube|spotify|all] <query>` - Buscar canciones
`/recommend [limite]` - Recomendaciones
`/similar` - Canciones similares
`/topgenres` - Géneros favoritos
`/radio list` - Ver estaciones
`/radio play <estación>` - Reproducer estación
""",
        inline=False
    )
    
    embed.add_field(
        name="🌐 Idioma y Configuración",
        value="""
`/language [código]` - Cambiar idioma
`/mylanguage` - Tu idioma actual
`/languages` - Ver idiomas disponibles
`/settings theme [dark|light]` - Cambiar tema
`/notifications settings` - Configurar notificaciones
`/profile` - Ver tu perfil
`/milestones` - Ver tus hitos
`/streak` - Tu racha de escucha
""",
        inline=False
    )
    
    embed.set_footer(text="Hecho por flexyng | BSD-3-Clause License")
    return embed
