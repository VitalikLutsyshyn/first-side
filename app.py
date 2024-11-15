
from flask import Flask,render_template,request
from db import DatabaseManager
app = Flask(__name__)


db = DatabaseManager("shop_dp.db")

@app.context_processor
def get_categories():
    categories = db.get_all_categories()
    return dict(categories=categories)

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


@app.route("/category/<category>")
def search_category(category):
    products = db.search_title_categories(category)
    title = db.get_category_title(category) 
    return render_template("category.html",items=products,title=title[0])




if __name__  == "__main__":
    app.run(debug=True)