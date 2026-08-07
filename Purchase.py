from Main import app, getProductSingle, connect_db
from flask import session, redirect, url_for, render_template, request
from datetime import datetime

def addPurchase(user_id, item_id, amount):
    db = connect_db()
    db.execute("""INSERT INTO purchases (user_id, item_id, amount, purchase_date) VALUES (?, ?, ?, datetime('now'))""", (user_id, item_id, amount))
    db.commit()
    db.close()


@app.route("/buy/<int:item_id>", methods=["POST"])
def buy_now(item_id):
    # Must be logged in
    if "user_id" not in session:
        return redirect(url_for("login"))

    product = getProductSingle(item_id)
    if not product:
        return "Product not found", 404

    # Safely get requested amount
    try:
        amount = int(request.form.get("amount", 1))
    except ValueError:
        amount = 1

    # Clamp to stock limits
    amount = max(1, min(amount, product["stock"]))

    # Update stock in DB
    db = connect_db()
    db.execute(
        "UPDATE products SET stock = stock - ? WHERE item_id = ?", 
        (amount, item_id)
    )
    db.commit()
    db.close()

    # Record purchase
    addPurchase(session["user_id"], item_id, amount)

    # Confirmation page
    return render_template(
        "Amazing_Bargain_Purchase.html",
        product=product,
        amount=amount
    )