from Main import app, getProducts, getUser
from flask import render_template, request, session

@app.route("/")
def loadHome():
    user = None
    
    if "user_id" in session:
        user = getUser(user_id=session["user_id"])
        if user:  
            user = dict(user)
    """ 
    Calls on all products in database that is displayed in home page by Jinja loop in HTML.
    Checks if image is NULL.
    Adds image to NULL image rows.
    """
    products = getProducts()
    for p in products:
        if not p.get("image"):
            p["image"] = "images/null_photo.jpg"

    return render_template("Amazing_Bargain_Home.html", user=user, products=products)

@app.route("/search")
def search():
    query = request.args.get("query", "")  # get the search term from the URL

    # basic search in product names
    products = getProducts()
    results = [p for p in products if query.lower() in p["item_name"].lower()]
    for p in results:
        if p["image"] == None:
            p["image"] = "images/null_photo.jpg"
    
    # Debugger
    #print(query)
            
    #for p in results: 
    #    print (p)

    return render_template("Amazing_Bargain_Home.html", products=results)


if __name__ == "__main__":
    app.run(debug=True)