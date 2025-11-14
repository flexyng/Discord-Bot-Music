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
        client = motor.motor_asyncio.AsyncIOMotorClient(
            MONGODB_URI,
            maxPoolSize=10,
            minPoolSize=5,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000
        )
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
    await db.premium_keys.create_index([("key", ASCENDING)], unique=True)
    await db.premium_users.create_index([("user_id", ASCENDING)], unique=True)

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

async def generate_premium_key(duration_days: int = 30):
    import secrets
    try:
        key = f"KEY-{secrets.token_hex(8).upper()}"
        premium_key = {
            "key": key,
            "duration_days": duration_days,
            "created_at": datetime.utcnow(),
            "expires_at": None,
            "redeemed_by": None,
            "is_active": True,
            "uses": 0
        }
        result = await db.premium_keys.insert_one(premium_key)
        return key
    except Exception as e:
        logger.error(f"Error generando premium key: {e}")
        raise

async def redeem_premium_key(user_id: int, key: str):
    try:
        premium_key = await db.premium_keys.find_one({"key": key})
        
        if not premium_key:
            return False, "Clave no válida"
        
        if not premium_key.get("is_active"):
            return False, "Clave no activa"
        
        if premium_key.get("redeemed_by"):
            return False, "Clave ya ha sido utilizada"
        
        expires_at = datetime.utcnow()
        from datetime import timedelta
        expires_at += timedelta(days=premium_key["duration_days"])
        
        await db.premium_keys.update_one(
            {"key": key},
            {
                "$set": {
                    "redeemed_by": user_id,
                    "expires_at": expires_at,
                    "uses": premium_key.get("uses", 0) + 1
                }
            }
        )
        
        await db.premium_users.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "user_id": user_id,
                    "is_premium": True,
                    "premium_expires_at": expires_at,
                    "activated_keys": premium_key.get("uses", 0) + 1
                }
            },
            upsert=True
        )
        
        return True, f"✅ Premium activado hasta {expires_at.strftime('%d/%m/%Y')}"
    except Exception as e:
        logger.error(f"Error redenimiendo key: {e}")
        return False, str(e)

async def is_premium(user_id: int):
    try:
        user = await db.premium_users.find_one({"user_id": user_id})
        if not user:
            return False
        
        expires_at = user.get("premium_expires_at")
        if not expires_at:
            return False
        
        if datetime.utcnow() > expires_at:
            await db.premium_users.update_one(
                {"user_id": user_id},
                {"$set": {"is_premium": False}}
            )
            return False
        
        return True
    except Exception as e:
        logger.error(f"Error verificando premium: {e}")
        return False

async def get_premium_info(user_id: int):
    try:
        user = await db.premium_users.find_one({"user_id": user_id})
        if not user:
            return None
        return user
    except Exception as e:
        logger.error(f"Error obteniendo info premium: {e}")
        return None

async def get_premium_keys_info():
    try:
        keys = await db.premium_keys.find({}).to_list(length=None)
        return keys
    except Exception as e:
        logger.error(f"Error obteniendo keys: {e}")
        return []

async def deactivate_premium_key(key: str):
    try:
        await db.premium_keys.update_one(
            {"key": key},
            {"$set": {"is_active": False}}
        )
        return True
    except Exception as e:
        logger.error(f"Error desactivando key: {e}")
        return False

async def extend_premium(user_id: int, duration_days: int):
    try:
        from datetime import timedelta
        user = await db.premium_users.find_one({"user_id": user_id})
        
        if not user:
            expires_at = datetime.utcnow() + timedelta(days=duration_days)
        else:
            current_expires = user.get("premium_expires_at", datetime.utcnow())
            expires_at = current_expires + timedelta(days=duration_days)
        
        await db.premium_users.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "user_id": user_id,
                    "is_premium": True,
                    "premium_expires_at": expires_at
                }
            },
            upsert=True
        )
        
        return True, expires_at
    except Exception as e:
        logger.error(f"Error extendiendo premium: {e}")
        return False, None
