from flask import Blueprint, render_template, request, redirect, session
from db import get_db

records = Blueprint("records", __name__)

@records.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html")

@records.route("/add", methods=["GET", "POST"])
def add_record():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        data = (
            request.form["file_number"],
            request.form["title"],
            request.form["department"],
            request.form["created_date"],
            request.form["status"],
            request.form["remarks"]
        )

        conn = get_db()
        conn.execute("""
        INSERT INTO records (file_number, title, department, created_date, status, remarks)
        VALUES (?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()

        return redirect("/view")

    return render_template("add_record.html")

@records.route("/view")
def view_records():
    if "user" not in session:
        return redirect("/")

    conn = get_db()
    records = conn.execute("SELECT * FROM records").fetchall()
    return render_template("view_records.html", records=records)

@records.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_record(id):
    conn = get_db()

    if request.method == "POST":
        conn.execute("""
        UPDATE records SET file_number=?, title=?, department=?, created_date=?, status=?, remarks=?
        WHERE id=?
        """, (
            request.form["file_number"],
            request.form["title"],
            request.form["department"],
            request.form["created_date"],
            request.form["status"],
            request.form["remarks"],
            id
        ))
        conn.commit()
        return redirect("/view")

    record = conn.execute("SELECT * FROM records WHERE id=?", (id,)).fetchone()
    return render_template("edit_record.html", record=record)

@records.route("/delete/<int:id>")
def delete_record(id):
    if session.get("role") != "admin":
        return "Unauthorized Access"

    conn = get_db()
    conn.execute("DELETE FROM records WHERE id=?", (id,))
    conn.commit()
    return redirect("/view")
@records.route("/report", methods=["GET", "POST"])
def report():
    if "user" not in session:
        return redirect("/")

    records = []
    if request.method == "POST":
        department = request.form["department"]
        conn = get_db()
        records = conn.execute(
            "SELECT * FROM records WHERE department=?",
            (department,)
        ).fetchall()

    return render_template("report.html", records=records)
