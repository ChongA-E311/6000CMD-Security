from Main import app, getProductSingle, getProducrDesc, getReviews
from flask import render_template

@app.route("/product/<int:item_id>")
def product_page(item_id):
    product = getProductSingle(item_id)
    desc = getProducrDesc(item_id)
    reviews = getReviews(item_id)    
    
    if not product:
        return "Product not found", 404
    
    if not product.get("image"):
        product["image"] = "images/null_photo.jpg"
        
    product = dict(product)
        
    product["desc"] = desc["desc"]
    reviews = [dict(r) for r in reviews]

    return render_template("Amazing_Bargin_Product.HTML", product=product, reviews=reviews)