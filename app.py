from flask import Flask,render_template
from db import DatabaseManager
app = Flask(__name__)


db = DatabaseManager("shop_dp.db")

@app.route("/")
def index():
    products = db.get_all_products()
    print(products)
    return render_template("index.html", items=products)


@app.route("/tech")
def tech_catefory():
    
    return "Привіт!"
    

if __name__  == "__main__":
    app.run()