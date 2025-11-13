# 📚 Ejemplos de Uso

Esta guía muestra cómo usar los comandos del bot de música con ejemplos prácticos.

## 🎵 Reproducción de Música

### Reproducir una canción
```
/play Bohemian Rhapsody
/play Taylor Swift Anti-Hero
/play Lo-fi beats for studying
```
El bot buscará automáticamente la canción en YouTube y Spotify.

### Ver la cola de reproducción
```
/queue
/queue 2
```
Muestra las próximas 10 canciones. Usa números para cambiar de página.

### Controlar la reproducción
```
/pause              # Pausa la canción actual
/resume             # Reanuda desde donde se pausó
/skip               # Salta a la siguiente canción
/stop               # Detiene todo y desconecta
/nowplaying         # Muestra la canción actual
```

### Modos especiales
```
/shuffle            # Activa modo shuffle (aleatoria)
/loop               # Cicla entre: off → one song → all songs → off
/volume 75          # Ajusta volumen al 75%
```

## ❤️ Gestionar Favoritos

### Guardar canciones
```
/favorite add
```
Mientras se reproduye una canción, usa este comando para guardarla como favorita.

### Ver favoritos
```
/favorite list
```
Muestra tus canciones favoritas ordenadas por cantidad de reproducciones.

### Eliminar de favoritos
```
/favorite remove Bohemian Rhapsody
```

### Ejemplo completo
```
Usuario: /play Levitating
Bot: ✅ Agregado a la cola - "Levitating" por Dua Lipa

Usuario: /favorite add
Bot: ✅ Agregado a favoritos - "Levitating"

Usuario: /favorite list
Bot: [Muestra lista de favoritos con estadísticas]
```

## 📋 Crear y Gestionar Playlists

### Crear una playlist
```
/playlist create Gym Session
/playlist create Relax Vibes with description "Música para relajarse"
```

### Agregar canciones a una playlist
```
/playlist add Gym Session
```
Agrega la canción que se está reproduciendo a la playlist.

### Listar tus playlists
```
/playlist list
```

### Eliminar una playlist
```
/playlist delete Gym Session
```

### Ejemplo: Crear una playlist completa
```
Usuario: /playlist create Workout Mix
Bot: ✅ Playlist creada - "Workout Mix"

Usuario: /play Eye of the Tiger
Usuario: /playlist add Workout Mix
Bot: ✅ Agregado a "Workout Mix"

Usuario: /play Pump It Up
Usuario: /playlist add Workout Mix
Bot: ✅ Agregado a "Workout Mix"

Usuario: /play Don't Stop Me Now
Usuario: /playlist add Workout Mix
Bot: ✅ Agregado a "Workout Mix"

Usuario: /playlist list
Bot: [Muestra "Workout Mix" con 3 canciones]
```

## 📊 Ver Estadísticas

### Mis estadísticas
```
/stats
```
Muestra:
- Total de reproducciones
- Tiempo total escuchado
- Género favorito
- Artista favorito

### Mi perfil completo
```
/profile
```
Muestra:
- Información del usuario
- Estadísticas de reproducción
- Configuración actual
- Historial general

### Ejemplo
```
Usuario: /stats
Bot:
📊 Estadísticas de Juan
▶ Reproducciones totales: 1,234
⏱ Tiempo total: 128h 45m
⭐ Género favorito: Indie Rock
🎤 Artista favorito: Arctic Monkeys
```

## ⚙️ Configurar Preferencias

### Cambiar tema
```
/settings theme dark
/settings theme light
```

### Activar/desactivar notificaciones
```
/settings notifications true
/settings notifications false
```

### Activar/desactivar autoplay
```
/settings autoplay true     # Reproducción automática al agregar canciones
/settings autoplay false
```

### Ejemplo de configuración
```
Usuario: /settings theme dark
Bot: ✅ Tema actualizado - Tu tema es ahora "dark"

Usuario: /settings notifications false
Bot: 🔔 Notificaciones - Tus notificaciones han sido desactivadas

Usuario: /profile
Bot: [Muestra perfil con nueva configuración]
```

## 🎯 Casos de Uso Comunes

### Crear una lista de fiesta
```
/playlist create Party Time
/play Levitating
/playlist add Party Time
/play Blinding Lights
/playlist add Party Time
/play Shut Up and Dance
/playlist add Party Time
/shuffle          # Opcional: activar shuffle
/loop             # Opcional: repetir playlist
```

### Sesión de estudio relajado
```
/play Lo-fi Hip Hop Beats
/volume 30        # Volumen bajo
/loop             # Repetir indefinidamente
```

### Descubrir nueva música
```
/play Artist Name Mix
/pause
/nowplaying
/favorite add
# Repetir con otros artistas
```

### Sesión de gym
```
/playlist create Gym Workout
/play High energy trap
/play EDM fitness mix
/play Rock Anthems
/shuffle           # Mezclar el orden
/volume 80         # Volumen alto
```

## 💡 Tips y Trucos

### Búsqueda específica
```
/play The Beatles - Hey Jude
/play Dua Lipa 2024
/play Lo-fi beats to study to
```

### Aprovechar los favoritos
```
/favorite list          # Ver qué canciones te gustan más
/play <canción favorita>
```

### Gestionar múltiples playlists
```
/playlist create Commute
/playlist create Sleep
/playlist create Workout
```

### Monitorear tu consumo de música
```
/stats              # Ver cuántas canciones has escuchado
/profile            # Ver información completa
```

## 🚨 Códigos de Error Comunes

| Error | Solución |
|-------|----------|
| "No se encontró la canción" | Intenta con un nombre más específico |
| "Debes estar en un canal de voz" | Únete a un canal de voz primero |
| "No hay música reproduciéndose" | Reproduce una canción con `/play` |
| "La cola está vacía" | Agrega canciones con `/play` |

## 📞 Ayuda

```
/help               # Muestra todos los comandos disponibles
```

---

**¡Disfruta usando el bot de música!** 🎵
