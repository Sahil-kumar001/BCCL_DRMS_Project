import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("database.db")
c = conn.cursor()

# Users table
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

# Insert admin user
admin_password = generate_password_hash("admin123")
c.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
          ("admin", admin_password, "admin"))

# Records table
c.execute("""
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_number TEXT,
    title TEXT,
    department TEXT,
    created_date TEXT,
    status TEXT,
    remarks TEXT
)
""")

conn.commit()
conn.close()

print("Database Initialized Successfully")