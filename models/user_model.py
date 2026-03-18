import sqlite3


def get_user_by_username(username):
    conn = sqlite3.connect("snippets.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, password FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()

    return user


def create_user(username, hashed_password):
    conn = sqlite3.connect("snippets.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashed_password)
    )

    conn.commit()
    conn.close()
