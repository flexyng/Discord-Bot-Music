# Discord Music Bot v1.4.0 - Setup Guide

## Nuevas Características en v1.4.0

### 1. Sistema Premium
El bot ahora incluye un sistema premium completo con:
- **Claves premium** con duración personalizable
- **Características exclusivas** para usuarios premium
- **Comparación free vs premium**

### 2. Comandos de Owner
Solo propietarios del bot pueden acceder:
- `/generate_keys [cantidad] [días]` - Generar claves premium
- `/view_keys` - Ver todas las claves
- `/deactivate_key <key>` - Desactivar una clave
- `/extend_premium <usuario> [días]` - Extender premium
- `/check_premium <usuario>` - Verificar estado premium
- `/bot_stats` - Estadísticas del bot
- `/reload_cog <nombre>` - Recargar un cog
- `/owner_help` - Ver ayuda de owner

### 3. Comandos de Premium (Para todos)
- `/premium redeem <key>` - Redimir clave premium
- `/premium info` - Ver información de premium
- `/premium status` - Ver tu estado premium
- `/features` - Ver características comparadas

### 4. Todos los comandos son Hybrid
Todos los comandos funcionan tanto como:
- **Slash commands**: `/comando`
- **Prefix commands**: `!comando`

## Instalación

### 1. Variables de entorno
Actualizar `.env` con:
```
DISCORD_TOKEN=your_token
OWNER_IDS=123456789,987654321
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=discord_music_bot
SPOTIFY_CLIENT_ID=optional
SPOTIFY_CLIENT_SECRET=optional
DEFAULT_LANGUAGE=es
```

### 2. Dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar el bot
```bash
python main.py
```

## Uso del Sistema Premium

### Para Propietarios:

1. **Generar claves**:
   ```
   /generate_keys 10 30
   ```
   Esto genera 10 claves válidas por 30 días

2. **Ver claves**:
   ```
   /view_keys
   ```
   Muestra todas las claves, cuáles están activas y usadas

3. **Extender premium**:
   ```
   /extend_premium @usuario 60
   ```
   Extiende premium a un usuario por 60 días

### Para Usuarios:

1. **Redimir clave**:
   ```
   /premium redeem KEY-ABC123XYZ
   ```

2. **Ver estado**:
   ```
   /premium status
   ```

3. **Ver beneficios**:
   ```
   /premium info
   ```

## Características Premium vs Free

| Característica | Free | Premium |
|---|---|---|
| Playlists | 5 | Ilimitadas |
| Cola | 50 canciones | Ilimitada |
| Análisis avanzado | No | Sí |
| Prefijo personalizado | No | Sí |
| Soporte prioritario | No | Sí |
| Sin anuncios | No | Sí |

## Estructura de Decoradores

### owner_only()
```python
@commands.hybrid_command()
@owner_only()
async def mi_comando(self, ctx):
    pass
```

### premium_only()
```python
@commands.hybrid_command()
@premium_only()
async def mi_comando(self, ctx):
    pass
```

### admin_only()
```python
@commands.hybrid_command()
@admin_only()
async def mi_comando(self, ctx):
    pass
```

## Estructura de Base de Datos

### Colecciones Nuevas:

**premium_keys**:
- `key`: String único
- `duration_days`: Número de días de validez
- `created_at`: Fecha de creación
- `redeemed_by`: ID del usuario que redimió (null si no usado)
- `expires_at`: Fecha de vencimiento
- `is_active`: Boolean
- `uses`: Número de usos

**premium_users**:
- `user_id`: ID del usuario (único)
- `is_premium`: Boolean
- `premium_expires_at`: Fecha de vencimiento
- `activated_keys`: Número de claves activadas

## Cambios en Configuración

### config.py
Nuevas variables:
- `OWNER_IDS`: Lista de IDs de propietarios
- `COMMAND_PREFIX`: Cambió de "/" a "!"
- `COLORS["premium"]`: Color dorado (#FFD700)
- `COLORS["warning"]`: Color naranja (#FFA500)
- `PREMIUM_FEATURES`: Dict con características

## Todos los Cogs y Comandos

### Cogs:
1. **owner.py** - Comandos de propietario
2. **premium.py** - Sistema de premium
3. **music.py** - Reproductor de música
4. **playlists.py** - Gestión de playlists
5. **search.py** - Búsqueda de canciones
6. **favorites.py** - Canciones favoritas
7. **radio.py** - Modo radio
8. **notifications.py** - Notificaciones
9. **profile.py** - Perfil de usuario
10. **collaboration.py** - Colaboración
11. **advanced_features.py** - Características avanzadas
12. **recommendations.py** - Recomendaciones
13. **language.py** - Gestión de idiomas
14. **queue_manager.py** - Gestión de cola
15. **leaderboard.py** - Tabla de posiciones
16. **playlist_analytics.py** - Análisis de playlists
17. **utilities.py** - Utilidades

## Testing

Todos los archivos han sido verificados para:
- ✅ Sintaxis Python correcta
- ✅ Decoradores hybrid_command/hybrid_group
- ✅ Funciones de base de datos
- ✅ Sistema de permisos

## Notas Importantes

1. **OWNER_IDS**: Debe estar configurado en .env para que funcionen los comandos de owner
2. **Prefijo**: El prefijo cambió de "/" a "!" para permitir slash commands
3. **Premium**: El sistema es completamente funcional pero requiere implementación de cobro en producción
4. **Database**: Requiere MongoDB activo

## Soporte

Para reportar errores o sugerencias:
```
/report <descripción>
/suggest <sugerencia>
```
