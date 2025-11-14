# 🎵 Bot de Música Discord - Profesional

Bot de música avanzado para Discord con soporte YouTube, Spotify y muchas funcionalidades profesionales.

## ⚙️ Requisitos

- **Python 3.10+** (https://www.python.org/)
- **Token de Discord Bot** (https://discord.com/developers/applications)
- **Spotify API** (Opcional) (https://developer.spotify.com/dashboard)
- **FFmpeg** (Para reproducción de audio)

## 📦 Instalación

### 1. Clonar/Descargar el proyecto
```bash
cd Discord-Bot-Music
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Edita `.env`:
```env
DISCORD_TOKEN=tu_token_del_bot_aqui
SPOTIFY_CLIENT_ID=tu_id_spotify (opcional)
SPOTIFY_CLIENT_SECRET=tu_secret_spotify (opcional)
```

## 🔑 Obtener credenciales

### Discord Token
1. Ve a https://discord.com/developers/applications
2. Crea una nueva aplicación
3. Ve a "Bot" y crea un bot
4. En "TOKEN" haz click en "Copy"
5. Pega el token en `.env`

### Spotify Credentials (Opcional)
1. Ve a https://developer.spotify.com/dashboard
2. Crea o abre una aplicación
3. Copia "Client ID" y "Client Secret"
4. Pégalos en `.env`

### Permisos del Bot
1. En Discord Developers, ve a OAuth2 > URL Generator
2. Selecciona scopes:
   - `bot`
   - `applications.commands`
3. Selecciona permisos:
   - **Text Channels**: Send Messages, Embed Links, Read Message History
   - **Voice**: Connect, Speak, Use Voice Activity
4. Copia el URL generado y abre en el navegador
5. Selecciona el servidor y confirma

## 🚀 Ejecución

```bash
python main.py
```

Verás en la consola:
```
✅ Bot conectado como YourBot#0000
📊 Guilds: 1
🔄 Cogs cargados: 4
✅ 15 comandos sincronizados
```

## 🎵 Comandos de Reproducción

### Música
| Comando | Descripción |
|---------|-------------|
| `/play <canción>` | Reproduce una canción (YouTube/Spotify) |
| `/queue [página]` | Muestra la cola de reproducción |
| `/skip` | Salta la canción actual |
| `/pause` | Pausa la música |
| `/resume` | Reanuda la música |
| `/stop` | Detiene y desconecta |
| `/nowplaying` | Muestra la canción actual |
| `/shuffle` | Activa/desactiva shuffle |
| `/loop` | Cambia el modo de repetición (off/one/all) |
| `/volume <0-100>` | Ajusta el volumen |

## ❤️ Favoritos

| Comando | Descripción |
|---------|-------------|
| `/favorite add <canción>` | Agrega a favoritos |
| `/favorite remove <canción>` | Elimina de favoritos |
| `/favorite list` | Muestra tus favoritos |

## 📋 Playlists

| Comando | Descripción |
|---------|-------------|
| `/playlist create <nombre> [descripción]` | Crea una playlist |
| `/playlist list` | Lista tus playlists |
| `/playlist delete <nombre>` | Elimina una playlist |

## 📊 Perfil

| Comando | Descripción |
|---------|-------------|
| `/stats` | Muestra tus estadísticas |
| `/profile` | Muestra tu perfil completo |
| `/settings theme <dark/light>` | Cambia tu tema |
| `/settings notifications <true/false>` | Activa/desactiva notificaciones |
| `/settings autoplay <true/false>` | Activa/desactiva reproducción automática |
| `/help` | Muestra todos los comandos |

## 🌟 Características

### Básicas
✅ **Reproducción multicanal** - Funciona en múltiples servidores simultáneamente
✅ **YouTube + Spotify** - Busca en ambas plataformas
✅ **Embeds profesionales** - Diseño moderno con Discord v2
✅ **Portadas dinámicas** - Muestra la carátula de la canción
✅ **Sistema de favoritos** - Guarda canciones favoritas
✅ **Playlists personalizadas** - Crea y gestiona playlists
✅ **Estadísticas** - Trackea tus reproducciones
✅ **Shuffle & Loop** - Modos de reproducción avanzados
✅ **Control de volumen** - Ajusta dinámicamente
✅ **Base de datos** - Persistencia de datos con SQLite
✅ **Logging completo** - Registra todas las acciones
✅ **Manejo de errores** - Sistema robusto de errores
✅ **Bajo consumo** - Optimizado para eficiencia
✅ **Minimalista** - Interfaz limpia y simple

### Avanzadas (v1.1.0+)
✨ **Búsqueda con previsualizaciones** - Ve resultados de múltiples fuentes lado a lado
✨ **Radiociones personalizadas** - 10+ estaciones de radio (Lo-Fi, EDM, Jazz, etc.)
✨ **Recomendaciones inteligentes** - Basadas en tu historial de reproducción
✨ **Notificaciones en tiempo real** - Alertas personalizadas de eventos
✨ **Hitos de reproducción** - Celebra tus logros musicales
✨ **Racha de escucha** - Seguimiento de actividad

## 🗂️ Estructura del proyecto

```
prototipo/
├── main.py              # Archivo principal del bot
├── config.py            # Configuración del bot
├── db.py                # Funciones de base de datos
├── utils.py             # Funciones auxiliares y embeds
├── logger.py            # Sistema de logging
├── requirements.txt     # Dependencias
├── LICENSE              # Licencia BSD 3-Clause
├── README.md            # Este archivo
├── SETUP.md             # Guía de instalación
├── CHANGELOG.md         # Historial de versiones
├── examples.md          # Ejemplos de uso
├── .env                 # Variables de entorno (crear)
├── .env.example         # Plantilla de variables
├── .gitignore           # Archivos a ignorar
├── music_bot.db         # Base de datos (auto-creada)
├── logs/                # Carpeta de logs (auto-creada)
└── cogs/                # Extensiones del bot
    ├── __init__.py
    ├── music.py         # Comandos de reproducción
    ├── favorites.py     # Comandos de favoritos
    ├── playlists.py     # Comandos de playlists
    ├── profile.py       # Comandos de perfil
    ├── search.py        # Búsqueda con previsualizaciones [NUEVO]
    ├── radio.py         # Radiociones personalizadas [NUEVO]
    ├── recommendations.py # Recomendaciones inteligentes [NUEVO]
    └── notifications.py # Notificaciones en tiempo real [NUEVO]
```

## 🔧 Configuración avanzada

### Cambiar el prefijo de comandos
En `config.py`:
```python
COMMAND_PREFIX = "!"  
```

### Ajustar colores de embeds
En `config.py`:
```python
COLORS = {
    "primary": 0x7B2CBF,    # Cambiar colores
    "success": 0x06A77D,
    "error": 0xFF0000,
}
```

## 📝 Logs

Los logs se guardan en `logs/music_bot_YYYYMMDD.log`

Ejemplo:
```
2024-01-15 14:23:45 - MusicBot - INFO - Bot conectado como MyBot#0000
2024-01-15 14:24:10 - MusicBot - INFO - Command: play hello | User: User#1234 | Guild: My Server
```

## 🐛 Troubleshooting

### "Token inválido"
- Verifica que copiaste bien el token en `.env`
- No incluyas caracteres extras

### "FFmpeg no encontrado"
- Instala FFmpeg: https://ffmpeg.org/download.html
- Añade al PATH del sistema

### "No se encuentra la canción"
- YouTube/Spotify podría estar bloqueado
- Intenta con un título diferente o más específico

### "El bot no se conecta a voz"
- Verifica los permisos del bot en el servidor
- El bot debe tener permisos "Connect" y "Speak"

## 📚 Recursos

- [discord.py Documentation](https://discordpy.readthedocs.io/)
- [Spotify Web API](https://developer.spotify.com/documentation/web-api)
- [yt-dlp Documentation](https://github.com/yt-dlp/yt-dlp)
