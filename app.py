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

    return render_template("index.html", items=products)
    
    

if __name__  == "__main__":
    app.run(debug=True)