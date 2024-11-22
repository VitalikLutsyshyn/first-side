
from flask import Flask,render_template,request,session,redirect,url_for
from db import DatabaseManager
from config import SECRET_KEY


app = Flask(__name__)
app.secret_key = SECRET_KEY

db = DatabaseManager("shop_dp.db")

@app.context_processor
def get_categories():
    categories = db.get_all_categories()
    cart = session.get('cart', {})
    return dict(categories=categories,cart=cart)

@app.route("/")
def index():
    products = db.get_all_products()
    print(products)
    return render_template("index.html", items=products)


@app.route("/search")
def search():
    products = []
    if request.method == "GET":
        search = request.args.get("search")
        products = db.search_product(search)

    return render_template("search.html", items=products)


@app.route("/products/<int:product_id>")
def product_page(product_id):
    product = db.get_product(product_id)
    cart = session["cart"]

    return render_template("product_page.html",product=product)


@app.route("/category/<category>")
def search_category(category):
    products = db.search_title_categories(category)
    title = db.get_category_title(category) 
    return render_template("category.html",items=products,title=title[0])

@app.route("/products/add-to-cart/<int:product_id>")
def addtocart(product_id):
    if "cart" not in session:
        session["cart"] = {}
    cart = session["cart"]
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1
        
    session['cart'] = cart
    session.modified  = True
    print(cart)
    
    return redirect(url_for("product_page", product_id=product_id))


if __name__  == "__main__":
    app.run(debug=True)