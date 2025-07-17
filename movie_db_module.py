import sqlite3
import random


class MovieDB:
    def __init__(self, db_path="baza_filmi.sqlite3"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def get_titles(self):
        self.cursor.execute("SELECT Title FROM bazebi")
        return [row[0] for row in self.cursor.fetchall()]

    def get_movie_by_title(self, title):
        self.cursor.execute("SELECT Title, Year, [Movie Info], Genre FROM bazebi WHERE Title = ?", (title,))
        return self.cursor.fetchone()

    def get_movies_by_genres(self, genres):
        if not genres:
            self.cursor.execute("SELECT Title, Year, [Movie Info], Genre FROM bazebi")
            return self.cursor.fetchall()

        placeholders = " OR ".join(["Genre LIKE ?"] * len(genres))
        sql = f"SELECT Title, Year, [Movie Info], Genre FROM bazebi WHERE {placeholders}"
        values = [f"%{g}%" for g in genres]
        self.cursor.execute(sql, values)
        return self.cursor.fetchall()

    def get_random_movie_by_genres(self, genres):
        movies = self.get_movies_by_genres(genres)
        return random.choice(movies) if movies else None