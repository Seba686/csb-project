import sqlite3
from werkzeug.security import generate_password_hash

def register_user(username, password):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    try:
        # A3 Sensitive data exposure: To fix, comment the line below and uncomment the line below that.
        hash_value = password
        #hash_value = generate_password_hash(password)
        c.execute(
            "INSERT INTO user (username, password, is_admin) VALUES (?, ?, ?)",
            (username, hash_value, 0)
        )
        con.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        con.close()

def login_user(username):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    c.execute(
        "SELECT username, password, is_admin FROM user WHERE username = ?",
        (username,)
    )
    row = c.fetchone()
    con.close()
    if row:
        return {"username": row[0], "password": row[1], "is_admin": bool(row[2])}
    return None

def create_post(username, content, is_public = True):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    try:
        c.execute(
            "INSERT INTO post (username, content, is_public) VALUES (?, ?, ?)",
            (username, content, int(is_public))
        )
        con.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        con.close()

def get_all_posts():
    con = sqlite3.connect("database.db")
    c = con.cursor()
    c.execute(
        "SELECT id, username, content, is_public, created_at FROM post ORDER BY created_at DESC"
    )
    rows = c.fetchall()
    con.close()
    return [
        {
            "id": row[0],
            "username": row[1],
            "content": row[2],
            "is_public": bool(row[3]),
            "created_at": row[4]
        }
        for row in rows
    ]

def get_all_public_posts():
    con = sqlite3.connect("database.db")
    c = con.cursor()
    c.execute(
        "SELECT id, username, content, is_public, created_at FROM post WHERE is_public = 1 ORDER BY created_at DESC"
    )
    rows = c.fetchall()
    con.close()
    return [
        {
            "id": row[0],
            "username": row[1],
            "content": row[2],
            "is_public": True,
            "created_at": row[4]
        }
        for row in rows
    ]

def get_posts_by_user(username):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    c.execute(
        # A1 Injection: To fix, comment the line below and uncomment the line below that. To exploit this vulnerability, a user can choose their username to be ' OR 1=1 OR ' (with the single quotes).
        "SELECT id, username, content, is_public, created_at FROM post WHERE username = '" + username + "' ORDER BY created_at DESC"
        #"SELECT id, username, content, is_public, created_at FROM post WHERE username = ? ORDER BY created_at DESC", (username,)
    )
    rows = c.fetchall()
    con.close()
    return [
        {
            "id": row[0],
            "username": row[1],
            "content": row[2],
            "is_public": bool(row[3]),
            "created_at": row[4]
        }
        for row in rows
    ]

def get_post_by_id(post_id):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    c.execute(
        "SELECT id, username, content, is_public, created_at FROM post WHERE id = ?",
        (post_id,)
    )
    row = c.fetchone()
    con.close()
    if row:
        return {
            "id": row[0],
            "username": row[1],
            "content": row[2],
            "is_public": bool(row[3]),
            "created_at": row[4]
        }
    return None