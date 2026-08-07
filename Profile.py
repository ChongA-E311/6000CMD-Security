from flask import render_template, request, session, redirect, url_for, flash
from Main import app, connect_db, getUser


@app.route("/profile", methods=["GET", "POST"])
def profile():

    # -----------------------------
    # 1. Ensure the user is logged in
    # -----------------------------
    if "user_id" not in session:
        flash("You must be logged in to view your profile.")
        return redirect(url_for("login"))

    user = getUser(user_id=session["user_id"])
    if not user:
        flash("User not found.")
        return redirect(url_for("login"))

    user = dict(user)  # convert sqlite3.Row → dict for template usage


    # -----------------------------
    # 2. Handle form submission (POST)
    # -----------------------------
    if request.method == "POST":

        new_username = request.form.get("username")
        new_email = request.form.get("email")
        new_password = request.form.get("password")

        db = connect_db()

        # Update username & email
        db.execute("""
            UPDATE users SET username = ?, email = ?
            WHERE user_id = ?
        """, (new_username, new_email, user["user_id"]))

        # Update password only if provided
        if new_password.strip() != "":
            from werkzeug.security import generate_password_hash
            hashed = generate_password_hash(new_password)
            db.execute("""
                UPDATE users SET password = ? WHERE user_id = ?
            """, (hashed, user["user_id"]))

        db.commit()
        db.close()

        flash("Profile updated successfully.")

        # Reload updated user data
        return redirect(url_for("profile"))


    # -----------------------------
    # 3. Display profile page (GET)
    # -----------------------------
    return render_template("Amazing_Bargain_Profile.html", user=user)
