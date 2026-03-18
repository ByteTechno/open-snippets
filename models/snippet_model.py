# models/snippet_model.py
import sqlite3
DB_NAME = "snippets.db"
def get_all_snippets_with_users():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT snippets.id, snippets.title, snippets.content, snippets.created_at, users.username
        FROM snippets
        JOIN users ON snippets.user_id = users.id
        ORDER BY snippets.created_at DESC
    ''')
    result = cursor.fetchall()
    conn.close()
    return result

def add_snippet(user_id, title, content):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO snippets (user_id, title, content) VALUES (?, ?, ?)",
        (user_id, title, content)
    )
    conn.commit()
    conn.close()

def delete_snippet(snippet_id, user_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM snippets WHERE id = ? AND user_id = ?",
        (snippet_id, user_id)
    )
    conn.commit()
    conn.close()

def get_snippets_by_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, title, content, created_at FROM snippets WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    )
    results = cursor.fetchall()
    conn.close()
    return results

def get_snippet_by_id(snippet_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT snippets.id, snippets.title, snippets.content, snippets.created_at, snippets.user_id, users.username
        FROM snippets
        JOIN users ON snippets.user_id = users.id
        WHERE snippets.id = ?
    """, (snippet_id,))

    snippet = cursor.fetchone()
    conn.close()
    return snippet


def update_snippet(snippet_id, user_id, title, content):
    conn = sqlite3.connect(DB_NAME)   
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE snippets SET title = ?, content = ? WHERE id = ? AND user_id = ?",
        (title, content, snippet_id, user_id)
    )

    conn.commit()
    conn.close()

def search_snippets(q):
    conn = sqlite3.connect(DB_NAME)   
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT snippets.id, snippets.title, snippets.content, snippets.created_at, users.username
        FROM snippets
        JOIN users ON snippets.user_id = users.id
        WHERE snippets.title LIKE ? OR snippets.content LIKE ?
        ORDER BY snippets.created_at DESC
    """, (f"%{q}%", f"%{q}%"))

    results = cursor.fetchall()
    conn.close()
    return results