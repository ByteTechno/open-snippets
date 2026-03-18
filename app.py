# app.py
from flask import Flask, render_template
from auth.routes import auth_bp
from snippets.routes import snippets_bp
from main.routes import main_bp
import os
import sqlite3

# Create Flask Application
app = Flask(__name__)
# 💡 Interview Tip: Production environments should use environment variables for SECRET_KEY
# import os
# app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-for-local-only')
app.secret_key = 'super-secret-key'  # Used for session encryption

# ✅ Global Error Handling (Enhanced professional feel)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

# ✅ Database Initialization (Auto-create tables on first run)
def init_db():
    if not os.path.exists("snippets.db"):
        conn = sqlite3.connect("snippets.db")
        cursor = conn.cursor()

        # Create Users table
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # Create Snippets table
        cursor.execute('''
            CREATE TABLE snippets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()
        print("✅ Database initialization successful (snippets.db created)")
    else:
        print("✅ snippets.db detected, skipping initialization")

# ✅ Initialize Database
init_db()

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(snippets_bp)
app.register_blueprint(main_bp)

# ✅ Run Application
if __name__ == "__main__":
    app.run(debug=True)
