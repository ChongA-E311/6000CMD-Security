from Main import app, connect_db
from flask import request, flash, redirect, url_for, render_template
from werkzeug.security import generate_password_hash
import time

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        # 1. Check password match
        if password != confirm:
            flash("Passwords do not match.")
            return redirect(url_for("register"))

        # 2. Check if username already exists
        db = connect_db()
        existing_user = db.execute(
            "SELECT * FROM users WHERE username = ? OR email = ?",
            (username, email)
        ).fetchone()

        if existing_user:
            db.close()
            flash("Username or email already exists.")
            return redirect(url_for("register"))

        # 3. Insert new user
        hashed_pw = generate_password_hash(password)

        db.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed_pw)
        )
        db.commit()
        db.close()

        time.sleep(2.5)
        flash("Registration successful! Please login.")
        return redirect(url_for("loadHome"))

    # GET request → show form
    return render_template("Amazing_Bargin_Register.html")