import sqlite3
import os
import sys

# Определяем точный путь к папке, где запущен скрипт или .exe
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_NAME = os.path.join(BASE_DIR, "library.db")

class DatabaseManager:
    """Класс для управления базой данных SQLite."""
    
    def __init__(self, db_path=DB_NAME):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        """Возвращает соединение с БД с увеличенным таймаутом."""
        # timeout=10 не дает базе зависать намертво при блокировках
        return sqlite3.connect(self.db_path, timeout=10)

    def _init_db(self):
        """Создает таблицы и заполняет жанры."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS genres (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    year INTEGER,
                    genre_id INTEGER,
                    cover_path TEXT,
                    FOREIGN KEY (genre_id) REFERENCES genres (id)
                )
            """)
            cursor.execute("SELECT COUNT(*) FROM genres")
            if cursor.fetchone()[0] == 0:
                default_genres = [("Фантастика",), ("Детектив",), ("Роман",), ("Научная литература",), ("Фэнтези",)]
                cursor.executemany("INSERT INTO genres (name) VALUES (?)", default_genres)
            conn.commit()
        finally:
            conn.close()

    def get_all_genres(self):
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM genres ORDER BY name")
            return cursor.fetchall()
        finally:
            conn.close()

    def get_all_books(self):
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            query = """
                SELECT b.id, b.title, b.author, b.year, g.name, b.cover_path 
                FROM books b 
                LEFT JOIN genres g ON b.genre_id = g.id
            """
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            conn.close()

    def add_book(self, title, author, year, genre_id, cover_path):
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO books (title, author, year, genre_id, cover_path)
                VALUES (?, ?, ?, ?, ?)
            """, (title, author, year, genre_id, cover_path))
            conn.commit()
        finally:
            conn.close()

    def update_book(self, book_id, title, author, year, genre_id, cover_path):
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE books 
                SET title = ?, author = ?, year = ?, genre_id = ?, cover_path = ?
                WHERE id = ?
            """, (title, author, year, genre_id, cover_path, book_id))
            conn.commit()
        finally:
            conn.close()

    def delete_book(self, book_id):
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
            conn.commit()
        finally:
            conn.close()