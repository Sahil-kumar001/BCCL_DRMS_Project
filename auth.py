from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import check_password_hash
from db import get_db

auth = Blueprint("auth", __name__)

@auth.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()

        if user and check_password_hash(user["password"], password):
            session["user"] = username
            session["role"] = user["role"]
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid Credentials")

    return render_template("login.html")

@auth.route("/logout")
def logout():
    session.clear()
    return redirect("/")