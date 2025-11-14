# Discord Music Bot - Quick Reference

## Ambiente
- **Language**: Python 3.10+
- **Framework**: discord.py 2.0+
- **Database**: MongoDB
- **Package Manager**: pip
- **Prefix**: ! (para comandos de texto)

## Estructura del Proyecto
```
.
├── main.py                    # Punto de entrada
├── config.py                  # Configuración
├── db.py                      # Funciones de base de datos
├── utils.py                   # Utilidades y decoradores
├── logger.py                  # Sistema de logging
├── i18n.py                    # Traducciones (español, inglés, árabe, portugués)
├── cogs/                      # Comandos organizados por módulos
│   ├── owner.py              # Comandos de propietario (NUEVO)
│   ├── premium.py            # Sistema de premium (NUEVO)
│   ├── music.py              # Reproducción
│   ├── playlists.py          # Playlists
│   ├── search.py             # Búsqueda
│   └── ... (14 más)
├── .env                       # Variables de entorno
└── requirements.txt           # Dependencias
```

## Variables Importantes
- `OWNER_IDS`: IDs de propietarios (int list)
- `COMMAND_PREFIX`: "!" para prefix commands
- `MONGODB_URI`: Conexión a MongoDB
- `DISCORD_TOKEN`: Token del bot

## Comandos Útiles de Owner

```bash
# Generar 10 claves premium por 30 días
/generate_keys 10 30

# Ver todas las claves
/view_keys

# Extender premium a usuario
/extend_premium @usuario 60

# Verificar estado premium
/check_premium @usuario

# Ver estadísticas del bot
/bot_stats

# Recargar un cog
/reload_cog nombre_cog

# Ver ayuda de owner
/owner_help
```

## Crear Nuevo Comando

### Básico (Hybrid Command):
```python
@commands.hybrid_command(name="comando", description="Descripción")
async def comando(self, ctx):
    embed = create_success_embed("Título", "Mensaje")
    await ctx.send(embed=embed)
```

### Con permisos de Owner:
```python
@commands.hybrid_command()
@owner_only()
async def comando(self, ctx):
    pass
```

### Con permisos Premium:
```python
@commands.hybrid_command()
@premium_only()
async def comando(self, ctx):
    pass
```

### Con permisos de Admin:
```python
@commands.hybrid_command()
@admin_only()
async def comando(self, ctx):
    pass
```

## Funciones de Base de Datos - Premium

```python
# Generar clave
key = await db.generate_premium_key(duration_days=30)

# Redimir clave
success, message = await db.redeem_premium_key(user_id, key)

# Verificar si es premium
is_premium = await db.is_premium(user_id)

# Obtener info premium
info = await db.get_premium_info(user_id)

# Extender premium
success, expires_at = await db.extend_premium(user_id, days=30)

# Ver todas las claves
keys = await db.get_premium_keys_info()

# Desactivar clave
await db.deactivate_premium_key(key)
```

## Funciones Comunes de Base de Datos

```python
# Playlists
await db.create_playlist(user_id, name, description)
await db.get_user_playlists(user_id)
await db.add_song_to_playlist(playlist_id, title, url, source)

# Favoritos
await db.add_favorite(user_id, title, url, source)
await db.get_user_favorites(user_id)

# Estadísticas
await db.get_user_stats(user_id)

# Configuración
await db.get_user_settings(user_id)
await db.update_user_settings(user_id, **settings)
await db.get_user_language(user_id)
```

## Utilidades de Embeds

```python
# Embed de éxito
embed = create_success_embed("Título", "Descripción")

# Embed de error
embed = create_error_embed("Título", "Descripción")

# Embed de info
embed = create_info_embed("Título", "Descripción")

# Embed personalizado
embed = discord.Embed(
    title="Título",
    description="Descripción",
    color=COLORS["primary"]
)
```

## Logging

```python
from logger import log_command, log_error, log_music_event

# Registrar comando
log_command(user_id, "comando", {"param": value})

# Registrar error
log_error(user_id, "función", "mensaje de error")

# Registrar evento musical
log_music_event(user_id, "evento", {"datos": "valor"})
```

## Decoradores Disponibles

```python
@owner_only()        # Solo propietarios
@premium_only()      # Solo usuarios premium
@admin_only()        # Solo administradores del servidor
@commands.guild_only()        # Solo en servidores
@commands.dm_only()           # Solo en DM
@commands.cooldown(1, 5)      # 1 uso cada 5 segundos
```

## Colecciones MongoDB

- `playlists` - Playlists de usuarios
- `playlist_songs` - Canciones en playlists
- `favorites` - Canciones favoritas
- `play_history` - Historial de reproducción
- `user_stats` - Estadísticas de usuarios
- `user_settings` - Configuración de usuarios
- `premium_keys` - Claves premium (NUEVO)
- `premium_users` - Usuarios con premium (NUEVO)

## Testing de Sintaxis
```bash
python verify_syntax.py
```

## Linting/Type Checking (si está disponible)
```bash
flake8 .
mypy .
```

## Información de Versión
- **Versión**: v1.4.0
- **Total Cogs**: 17
- **Total Comandos**: 80+
- **Idiomas**: 4 (Español, Inglés, Árabe, Portugués)
- **Base de datos**: MongoDB
- **Últimas Adiciones**: Owner commands, Premium system, Hybrid commands
