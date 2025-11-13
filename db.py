import motor.motor_asyncio
from datetime import datetime
from pymongo import ASCENDING, DESCENDING
from config import MONGODB_URI, MONGODB_DB_NAME
from logger import logger

client = None
db = None

async def init_db():
    global client, db
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
        db = client[MONGODB_DB_NAME]
        
        await db.command('ping')
        logger.info("✅ Conectado a MongoDB correctamente")
        
        await create_indexes()
        logger.info("✅ Índices de la base de datos creados")
    except Exception as e:
        logger.error(f"❌ Error conectando a MongoDB: {e}")
        raise

async def create_indexes():
    await db.playlists.create_index([("user_id", ASCENDING), ("name", ASCENDING)], unique=True)
    await db.favorites.create_index([("user_id", ASCENDING), ("url", ASCENDING)], unique=True)
    await db.play_history.create_index([("user_id", ASCENDING), ("played_at", DESCENDING)])
    await db.user_stats.create_index([("user_id", ASCENDING)], unique=True)
    await db.user_settings.create_index([("user_id", ASCENDING)], unique=True)

async def create_playlist(user_id: int, name: str, description: str = None):
    try:
        playlist = {
            "user_id": user_id,
            "name": name,
            "description": description,
            "is_public": False,
            "created_at": datetime.utcnow()
        }
        result = await db.playlists.insert_one(playlist)
        return result.inserted_id
    except Exception as e:
        logger.error(f"Error creando playlist: {e}")
        raise

async def add_song_to_playlist(playlist_id: int, title: str, url: str, source: str, artist: str = None, duration: int = None, thumbnail: str = None):
    try:
        song = {
            "playlist_id": playlist_id,
            "title": title,
            "artist": artist,
            "url": url,
            "source": source,
            "duration": duration,
            "thumbnail": thumbnail,
            "added_at": datetime.utcnow()
        }
        result = await db.playlist_songs.insert_one(song)
        return result.inserted_id
    except Exception as e:
        logger.error(f"Error agregando canción a playlist: {e}")
        raise

async def add_favorite(user_id: int, title: str, url: str, source: str, artist: str = None, thumbnail: str = None):
    try:
        favorite = {
            "user_id": user_id,
            "title": title,
            "artist": artist,
            "url": url,
            "source": source,
            "thumbnail": thumbnail,
            "added_at": datetime.utcnow(),
            "plays": 0
        }
        await db.favorites.update_one(
            {"user_id": user_id, "url": url},
            {"$set": favorite},
            upsert=True
        )
    except Exception as e:
        logger.error(f"Error agregando favorito: {e}")
        raise

async def get_user_favorites(user_id: int, limit: int = 20):
    try:
        favorites = await db.favorites.find(
            {"user_id": user_id}
        ).sort("plays", DESCENDING).limit(limit).to_list(length=limit)
        return favorites
    except Exception as e:
        logger.error(f"Error obteniendo favoritos: {e}")
        return []

async def get_user_playlists(user_id: int):
    try:
        playlists = await db.playlists.find(
            {"user_id": user_id}
        ).sort("created_at", DESCENDING).to_list(length=None)
        return playlists
    except Exception as e:
        logger.error(f"Error obteniendo playlists: {e}")
        return []

async def get_playlist_songs(playlist_id: int):
    try:
        songs = await db.playlist_songs.find(
            {"playlist_id": playlist_id}
        ).to_list(length=None)
        return songs
    except Exception as e:
        logger.error(f"Error obteniendo canciones de playlist: {e}")
        return []

async def remove_from_playlist(playlist_id: int, song_id: int):
    try:
        await db.playlist_songs.delete_one({"_id": song_id, "playlist_id": playlist_id})
    except Exception as e:
        logger.error(f"Error removiendo canción de playlist: {e}")
        raise

async def delete_playlist(playlist_id: int):
    try:
        await db.playlist_songs.delete_many({"playlist_id": playlist_id})
        await db.playlists.delete_one({"_id": playlist_id})
    except Exception as e:
        logger.error(f"Error eliminando playlist: {e}")
        raise

async def add_play_history(user_id: int, title: str, artist: str, source: str, duration: int):
    try:
        history = {
            "user_id": user_id,
            "title": title,
            "artist": artist,
            "source": source,
            "duration": duration,
            "played_at": datetime.utcnow()
        }
        await db.play_history.insert_one(history)
        
        await db.user_stats.update_one(
            {"user_id": user_id},
            {
                "$inc": {
                    "total_plays": 1,
                    "total_time_played": duration
                }
            },
            upsert=True
        )
    except Exception as e:
        logger.error(f"Error agregando historial de reproducción: {e}")
        raise

async def get_user_stats(user_id: int):
    try:
        stats = await db.user_stats.find_one({"user_id": user_id})
        if not stats:
            await db.user_stats.insert_one({
                "user_id": user_id,
                "total_plays": 0,
                "total_time_played": 0,
                "favorite_genre": None,
                "favorite_artist": None,
                "updated_at": datetime.utcnow()
            })
            return (0, 0, None, None)
        return (
            stats.get("total_plays", 0),
            stats.get("total_time_played", 0),
            stats.get("favorite_genre"),
            stats.get("favorite_artist")
        )
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        return (0, 0, None, None)

async def get_user_settings(user_id: int):
    try:
        settings = await db.user_settings.find_one({"user_id": user_id})
        if not settings:
            await db.user_settings.insert_one({
                "user_id": user_id,
                "theme": "dark",
                "notifications": True,
                "autoplay": True,
                "language": "es"
            })
            return ("dark", True, True, "es")
        return (
            settings.get("theme", "dark"),
            settings.get("notifications", True),
            settings.get("autoplay", True),
            settings.get("language", "es")
        )
    except Exception as e:
        logger.error(f"Error obteniendo configuración: {e}")
        return ("dark", True, True, "es")

async def update_user_settings(user_id: int, **settings):
    try:
        await db.user_settings.update_one(
            {"user_id": user_id},
            {"$set": settings},
            upsert=True
        )
    except Exception as e:
        logger.error(f"Error actualizando configuración: {e}")
        raise

async def get_user_language(user_id: int):
    try:
        settings = await db.user_settings.find_one({"user_id": user_id})
        if settings:
            return settings.get("language", "es")
        return "es"
    except Exception as e:
        logger.error(f"Error obteniendo idioma: {e}")
        return "es"

async def set_user_language(user_id: int, language: str):
    try:
        await db.user_settings.update_one(
            {"user_id": user_id},
            {"$set": {"language": language}},
            upsert=True
        )
    except Exception as e:
        logger.error(f"Error estableciendo idioma: {e}")
        raise

async def close_db():
    global client
    if client:
        client.close()
        logger.info("✅ Conexión a MongoDB cerrada")
