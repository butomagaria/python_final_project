import sqlite3

class UserDB:
    def __init__(self, db_path="users.sqlite3"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def fetch_user_credentials(self):
        self.cursor.execute("SELECT username, email, password FROM users")
        return self.cursor.fetchall()

    def user_exists(self, username, email):
        self.cursor.execute("SELECT * FROM users WHERE username=? OR email=?", (username, email))
        return self.cursor.fetchone()

    def add_user(self, username, password, email):
        self.cursor.execute("INSERT INTO users (username, password, email,watch_later,favorites,watched) VALUES (?, ?, ?,?,?,?)", (username, password, email,"","",""))
        self.conn.commit()

    def get_password(self, username):
        self.cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def update_username(self, old_name, new_name):
        self.cursor.execute("UPDATE users SET username = ? WHERE username = ?", (new_name, old_name))
        self.conn.commit()

    def update_password(self, username, new_password):
        self.cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
        self.conn.commit()

    def get_email(self, username):
        self.cursor.execute("SELECT email FROM users WHERE username=?", (username,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def update_email(self, username, new_email):
        self.cursor.execute("UPDATE users SET email = ? WHERE username = ?", (new_email, username))
        self.conn.commit()

    def delete_user(self, username):
        self.cursor.execute("DELETE FROM users WHERE username=?", (username,))
        self.conn.commit()


    def add_movie_to_list(self, username, column, movie):
        self.cursor.execute(f"SELECT {column} FROM users WHERE username=?", (username,))
        result = self.cursor.fetchone()
        movies = []
        if result and result[0]:
            movies = result[0].split(", ") if result[0] else []
        if movie not in movies:
            movies.append(movie)
            movie_str = ", ".join(movies)
            self.cursor.execute(f"UPDATE users SET {column}=? WHERE username=?", (movie_str, username))
            self.conn.commit()

    def remove_movie_from_list(self, username, column, movie):
        self.cursor.execute(f"SELECT {column} FROM users WHERE username=?", (username,))
        result = self.cursor.fetchone()
        if result and result[0]:
            movies = result[0].split(", ") if result[0] else []
            if movie in movies:
                movies.remove(movie)
                movie_str = ", ".join(movies)
                self.cursor.execute(f"UPDATE users SET {column}=? WHERE username=?", (movie_str, username))
                self.conn.commit()

    def is_movie_in_list(self, username, column, movie):
        self.cursor.execute(f"SELECT {column} FROM users WHERE username=?", (username,))
        result = self.cursor.fetchone()
        if result and result[0]:
            movies = result[0].split(", ") if result[0] else []
            return movie in movies
        return False

    def get_user_movies(self, username, column):
        self.cursor.execute(f"SELECT {column} FROM users WHERE username=?", (username,))
        result = self.cursor.fetchone()
        if result and result[0]:
            return [m.strip(" []") for m in result[0].split(", ") if m.strip()]
        return []
