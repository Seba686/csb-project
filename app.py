from os import getenv
from dotenv import load_dotenv
load_dotenv()
import secrets
from flask import Flask, abort, render_template, request, redirect, session, url_for, flash
from db import (
     register_user, login_user,
    create_post, get_all_public_posts, get_posts_by_user, get_all_posts, get_post_by_id
)
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    posts = get_all_public_posts()
    return render_template("index.html", posts=posts)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if register_user(username, password):
            flash("Registration successful. Please log in.")
            return redirect(url_for("login"))
        else:
            flash("Username already exists.")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = login_user(username)
        if user:
            hash_value = user["password"]
            # A3 Sensitive data exposure: To fix, comment the line below and uncomment the line below that.
            if user["password"] == password:
            #if check_password_hash(hash_value, password):
                session["username"] = user["username"]
                session["is_admin"] = user["is_admin"]
                session["csrf_token"] = secrets.token_hex(16)
                flash("Logged in successfully.")
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid credentials.")
        else:
            flash("Invalid credentials.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    if session.get("is_admin"):
        posts = get_all_posts()
        return render_template("dashboard.html", posts=posts, admin=True)
    else:
        posts = get_posts_by_user(username)
        return render_template("dashboard.html", posts=posts, admin=False)

@app.route("/create_post", methods=["GET", "POST"])
def create():
    if "username" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        # Cross-Site Request Forgery: To fix, uncomment the two lines below.
        #if session["csrf_token"] != request.form["csrf_token"]:
        #    abort(403)
        content = request.form["content"]
        is_public = request.form.get("is_public") == "on"
        if create_post(session["username"], content, is_public):
            flash("Post created.")
            return redirect(url_for("dashboard"))
        else:
            flash("Failed to create post.")
    return render_template("create_post.html")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = get_post_by_id(post_id)
    if not post:
        abort(404)
    # A5 Broken access control: To fix, uncomment the block of code below.
    """
    elif post["is_public"] == 0:
        if "username" not in session:
            abort(404)
        elif post["username"] != session["username"] and session["is_admin"] != 1:
            abort(404)
    """
    
    # A7 Cross-Site Scripting (XSS): To fix, comment the line below and uncomment the line below that.
    return post["content"]
    #return render_template("show_post.html", post=post)

if __name__ == "__main__":
    app.run(debug=True)