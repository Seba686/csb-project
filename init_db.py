import sqlite3
from os import getenv, remove, path
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
load_dotenv()

if path.exists("database.db"):
    remove("database.db")

con = sqlite3.connect("database.db")
c = con.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS user(
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0
    )
""")
c.execute("""
    CREATE TABLE IF NOT EXISTS post(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        content TEXT NOT NULL,
        is_public INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(username) REFERENCES user(username)
    )
""")
c.execute(
    "INSERT INTO user (username, password, is_admin) VALUES ('admin', ?, 1)",
    # A3 Sensitive data exposure: To fix, comment the line below and uncomment the line below that.
    (getenv("ADMIN_PASSWORD"),)
    #(generate_password_hash(getenv("ADMIN_PASSWORD")),)
)
con.commit()
con.close()