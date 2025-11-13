import aiosqlite
import os
from datetime import datetime

DB_PATH = "music_bot.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS playlists (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                is_public BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, name)
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS playlist_songs (
                id INTEGER PRIMARY KEY,
                playlist_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                artist TEXT,
                url TEXT NOT NULL,
                source TEXT NOT NULL,
                duration INTEGER,
                thumbnail TEXT,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (playlist_id) REFERENCES playlists(id)
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                artist TEXT,
                url TEXT NOT NULL,
                source TEXT NOT NULL,
                thumbnail TEXT,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                plays INTEGER DEFAULT 0,
                UNIQUE(user_id, url)
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_stats (
                user_id INTEGER PRIMARY KEY,
                total_plays INTEGER DEFAULT 0,
                total_time_played INTEGER DEFAULT 0,
                favorite_genre TEXT,
                favorite_artist TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS play_history (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                artist TEXT,
                source TEXT NOT NULL,
                played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                duration INTEGER
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_settings (
                user_id INTEGER PRIMARY KEY,
                theme TEXT DEFAULT 'dark',
                notifications BOOLEAN DEFAULT 1,
                autoplay BOOLEAN DEFAULT 1,
                language TEXT DEFAULT 'es'
            )
        """)
        
        await db.commit()

async def create_playlist(user_id: int, name: str, description: str = None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO playlists (user_id, name, description) VALUES (?, ?, ?)",
            (user_id, name, description)
        )
        await db.commit()

async def add_song_to_playlist(playlist_id: int, title: str, url: str, source: str, artist: str = None, duration: int = None, thumbnail: str = None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO playlist_songs (playlist_id, title, artist, url, source, duration, thumbnail) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (playlist_id, title, artist, url, source, duration, thumbnail)
        )
        await db.commit()

async def add_favorite(user_id: int, title: str, url: str, source: str, artist: str = None, thumbnail: str = None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO favorites (user_id, title, artist, url, source, thumbnail) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, title, artist, url, source, thumbnail)
        )
        await db.commit()

async def get_user_favorites(user_id: int, limit: int = 20):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT title, artist, url, source, thumbnail, plays FROM favorites WHERE user_id = ? ORDER BY plays DESC LIMIT ?",
            (user_id, limit)
        ) as cursor:
            return await cursor.fetchall()

async def get_user_playlists(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT id, name, description FROM playlists WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        ) as cursor:
            return await cursor.fetchall()

async def get_playlist_songs(playlist_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT id, title, artist, url, source, duration, thumbnail FROM playlist_songs WHERE playlist_id = ?",
            (playlist_id,)
        ) as cursor:
            return await cursor.fetchall()

async def remove_from_playlist(playlist_id: int, song_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM playlist_songs WHERE id = ? AND playlist_id = ?",
            (song_id, playlist_id)
        )
        await db.commit()

async def delete_playlist(playlist_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM playlist_songs WHERE playlist_id = ?", (playlist_id,))
        await db.execute("DELETE FROM playlists WHERE id = ?", (playlist_id,))
        await db.commit()

async def add_play_history(user_id: int, title: str, artist: str, source: str, duration: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO play_history (user_id, title, artist, source, duration) VALUES (?, ?, ?, ?, ?)",
            (user_id, title, artist, source, duration)
        )
        await db.execute(
            "UPDATE user_stats SET total_plays = total_plays + 1, total_time_played = total_time_played + ? WHERE user_id = ?",
            (duration, user_id)
        )
        await db.commit()

async def get_user_stats(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT total_plays, total_time_played, favorite_genre, favorite_artist FROM user_stats WHERE user_id = ?",
            (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
            if not result:
                await db.execute(
                    "INSERT INTO user_stats (user_id) VALUES (?)",
                    (user_id,)
                )
                await db.commit()
                return (0, 0, None, None)
            return result

async def get_user_settings(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT theme, notifications, autoplay, language FROM user_settings WHERE user_id = ?",
            (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
            if not result:
                await db.execute(
                    "INSERT INTO user_settings (user_id) VALUES (?)",
                    (user_id,)
                )
                await db.commit()
                return ('dark', True, True, 'es')
            return result

async def update_user_settings(user_id: int, **settings):
    async with aiosqlite.connect(DB_PATH) as db:
        for key, value in settings.items():
            await db.execute(
                f"UPDATE user_settings SET {key} = ? WHERE user_id = ?",
                (value, user_id)
            )
        await db.commit()
