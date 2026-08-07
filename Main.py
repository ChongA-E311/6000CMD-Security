from flask import Flask, session
import sqlite3

app = Flask(__name__)
app.secret_key = "keyseriously"

def connect_db():
    """
    Connects to database
    """
    conn = sqlite3.connect("AmazingBarginDB.db")
    conn.row_factory = sqlite3.Row
    return conn

def getUser(input_value=None, user_id=None):
    """
    Returns a single user row matching either id or username.
    One of the two arguments must be provided.
    """
    if not input_value and not user_id:
        return None
    db = connect_db()
    user = None
    if user_id:
        user = db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    else:
        user = db.execute("SELECT * FROM users WHERE email = ? OR username = ?", (input_value, input_value)).fetchone()
    db.close()
    return user
   
def getProducts():
    """
    Returns all rows in product database. 
    """
    db = connect_db()
    rows = db.execute("SELECT * FROM products").fetchall()
    db.close()
    
    products = [dict(row) for row in rows]
    
    return products

def get_current_user():
    """Returns dict of logged-in user, or None if not logged in"""
    if "user_id" in session:
        user_row = getUser(user_id=session["user_id"])
        if user_row:
            return dict(user_row)
    return None

def getProductSingle(item_id):
    db = connect_db()
    row = db.execute("SELECT * FROM products WHERE item_id = ?", (item_id,)).fetchone()
    db.close()
    if row:
        return dict(row)  # convert sqlite3.Row to dict for mutability
    return None

def getProducrDesc(item_id):
    db = connect_db()
    desc_row = db.execute("SELECT desc FROM productDesc WHERE item_id = ?",(item_id,)).fetchone()
    db.close()
    
    return desc_row

def getReviews(item_id):
    db = connect_db()
    review_rows = db.execute("""SELECT username, reviewTxt, rating FROM reviews WHERE item_id = ?""", (item_id,)).fetchall()
    db.close()
    
    return review_rows

# Import all routes AFTER app is created
from Login import *
from Home import *
from Product import *
from Profile import *
from Register import *
from Purchase import *

if __name__ == "__main__":
    app.run(debug=True)
    
#test
#for user in getUser():
#    print(user["username"], user["email"]) 