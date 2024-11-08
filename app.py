
from flask import Flask,render_template,request
from db import DatabaseManager
app = Flask(__name__)


db = DatabaseManager("shop_dp.db")

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

    return render_template("product_page.html",product=product)




if __name__  == "__main__":
    app.run(debug=True)