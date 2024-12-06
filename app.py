
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
    cart_products = []
    total= 0
    if len(cart) > 0:
        for product_id in cart:
            product = db.get_product(product_id)
            cart_products.append(product)
            total += product[2] * cart[str(product_id)]           

    return dict(categories=categories,cart=cart,cart_products=cart_products,total=total)



@app.route("/")
def index():
    products = db.get_all_products()
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
    return redirect(url_for("product_page", product_id=product_id))

@app.route("/products/remove-from-cart/<int:product_id>")
def delete_product(product_id):
    cart = session["cart"]
    if str(product_id) in cart:
        del cart[str(product_id)]
    session['cart'] = cart
    session.modified  = True
    if request.referrer:
        return redirect(request.referrer)#перенаправлення на попередню сторінку
    else:
        return redirect(url_for("index"))

@app.route("/registration")
def registration():
    return render_template("registration.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/delivery")
def delivery():
    return render_template("delivery.html")

if __name__  == "__main__":
    app.run(debug=True)