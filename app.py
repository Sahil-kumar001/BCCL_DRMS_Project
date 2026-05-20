from flask import Flask, render_template, request, redirect, url_for, session
from db import get_db
import sqlite3

import auth
import records

app = Flask(__name__)
app.secret_key = "bccl_secret_key"  # session security

# Helper function
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        # NOTE: For learning purpose plain password is used
        # In real systems, password hashing should be implemented
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()

        if user:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", user=session["user"])

# ---------------- ADD RECORD ----------------
@app.route("/add", methods=["GET", "POST"])
def add_record():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        file_number = request.form["file_number"]
        title = request.form["title"]
        department = request.form["department"]
        created_date = request.form["created_date"]
        status = request.form["status"]
        remarks = request.form["remarks"]

        conn = get_db()
        conn.execute("INSERT INTO records (file_number, title, department, created_date, status, remarks) VALUES (?, ?, ?, ?, ?, ?)",
                     (file_number, title, department, created_date, status, remarks))
        conn.commit()
        return redirect("/view")

    return render_template("add_record.html")

# ---------------- VIEW RECORDS ----------------
@app.route("/view")
def view_records():
    if "user" not in session:
        return redirect("/")

    conn = get_db()
    records = conn.execute("SELECT * FROM records").fetchall()
    return render_template("view_records.html", records=records)

# ---------------- EDIT RECORD ----------------
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_record(id):
    if "user" not in session:
        return redirect("/")

    conn = get_db()

    if request.method == "POST":
        conn.execute("""UPDATE records SET 
                        file_number=?, title=?, department=?, created_date=?, status=?, remarks=?
                        WHERE id=?""",
                     (request.form["file_number"], request.form["title"], request.form["department"],
                      request.form["created_date"], request.form["status"], request.form["remarks"], id))
        conn.commit()
        return redirect("/view")

    record = conn.execute("SELECT * FROM records WHERE id=?", (id,)).fetchone()
    return render_template("edit_record.html", record=record)

# ---------------- DELETE RECORD ----------------
@app.route("/delete/<int:id>")
def delete_record(id):
    if "user" not in session:
        return redirect("/")

    conn = get_db()
    conn.execute("DELETE FROM records WHERE id=?", (id,))
    conn.commit()
    return redirect("/view")

# ---------------- REPORT ----------------
@app.route("/report", methods=["GET", "POST"])
def report():
    if "user" not in session:
        return redirect("/")

    records = []
    if request.method == "POST":
        department = request.form["department"]
        conn = get_db()
        records = conn.execute("SELECT * FROM records WHERE department=?", (department,)).fetchall()

    return render_template("report.html", records=records)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

app = Flask(__name__)
app.secret_key = "bccl_secret_key"

app.register_blueprint(auth)
app.register_blueprint(records)

if __name__ == "__main__":
    app.run(debug=True)
