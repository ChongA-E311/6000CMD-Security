from Main import app, getUser
from flask import render_template, request, session, redirect, url_for
from werkzeug.security import check_password_hash

# Handles login page functions
@app.route("/Login", methods=["GET", "POST"])
def login():
    
    """ 
    Checks the incoming input against the database.
    Gets input by request.form.
    Gets data from database by user = getUser().
    Compare data with if function.
    """
    
    if request.method == "POST":
        login_input = request.form["login_input"]
        password = request.form["password"]

        user_row = getUser(input_value=login_input)

        if user_row and check_password_hash(user_row["password"], password):
            session["user_id"] = user_row["id"]
            return redirect(url_for("loadHome")) 
        else:
            return render_template("Amazing_Bargain_Login.html", error="Invalid login.")

    return render_template("Amazing_Bargain_Login.html")

#Logout
@app.route("/logout")
def logout():
    session.clear()  # remove all session data
    return redirect(url_for("login"))  # send user back to login page