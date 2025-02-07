
from flask import Flask,render_template,request,session,redirect,url_for,flash
from db import DatabaseManager
from config import SECRET_KEY
from flask_login import LoginManager, UserMixin, login_user,logout_user,current_user,login_required


app = Flask(__name__)
app.secret_key = SECRET_KEY
db = DatabaseManager("shop_dp.db")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "alert-warning"
login_manager.login_message = "Зареєструйтеся або увійдіть в акаунт, щоб продовжити"
class User(UserMixin):
    def __init__(self,id,name,surname,email,phone_number,password):
        super().__init__()
        self.id = id
        self.name=name
        self.surname = surname
        self.email=email
        self.phone_number = phone_number
        self.password = password

@login_manager.user_loader#Підвантаження даних про користувача
def load_user(user_id):
    user_data = db.get_user_by_id(user_id)
    if user_data:
        return User(user_id,user_data[1],user_data[2],user_data[3],user_data[4],user_data[5] )
    else:
        return None

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
    flash("Товар додано в кошик","alert-success")
    return redirect(url_for("product_page", product_id=product_id))

@app.route("/products/remove-from-cart/<int:product_id>")
def delete_product(product_id):
    cart = session["cart"]
    if str(product_id) in cart:
        del cart[str(product_id)]
    session['cart'] = cart
    session.modified  = True
    flash("Товар видалено з кошика","alert-danger")
    if request.referrer:
        return redirect(request.referrer)#перенаправлення на попередню сторінку
    else:
        return redirect(url_for("index"))

@app.route("/registration", methods=["POST","GET"])#Дозвіл надсилання даних сторінці
def registration():
    if request.method == "POST":
        name = request.form.get("name", "").strip() #в зміну Name Записується імя яке вказано в формі на сайті
        surname = request.form.get("surname", "").strip()
        email =request.form.get("email", "").strip()
        phone_number = request.form.get("phone_number", "").strip()
        password = request.form.get("password", "").strip()
        password2 = request.form.get("password2", "").strip()
        
        errors = []

        if not name or not email or not phone_number or not password or not password2 or not surname:
            errors.append("Заповніть всі поля")
        if "@" not in email:
            errors.append("Введіть коректний email")
        if len(password) < 8:
            errors.append("Пароль має містити хоча б 8 символів")
        if password != password2:
            errors.append("Паролі мають співпадати")
                
        for symbol in phone_number.replace("(","").replace(")",""):
            if not symbol.isdigit():
                errors.append("Номер телефону має бути в форматі 9998887775")
                break
        if len(errors)>0:
            for error in errors:
                flash(error,"alert-warning")
        else:
            db.create_user(name,surname,email,phone_number,password)
            flash("Ви успішно зареєструвалися","alert-primary")
            return redirect(url_for("login"))
    return render_template("registration.html")



@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        email =request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not email or not password:
            flash("Заповніть всі поля","alert-warming")
        else:
            user_db = db.check_user(email,password)
            if not user_db:
                flash("Неправильний логін або пароль","alerm-warning")
            else:
                user = User(user_db[0],user_db[1],user_db[2],user_db[3],user_db[4],user_db[5] )
                login_user(user)
                return redirect(url_for("index"))

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Ви вийшли з профілю","alert-primary")
    return redirect(url_for("login"))

@app.route("/order",methods =["POST","GET"])
@login_required
def order():

    if "cart" not in session or len(session["cart"]) == 0:
        if request.referrer:
            return redirect(request.referrer)
        else:
            return redirect(url_for("index"))
        
    if request.method == "POST":
        country =request.form.get("country", "").strip()
        city =request.form.get("city", "").strip()
        street =request.form.get("street", "").strip()
        comment =request.form.get("comment", "").strip()
        post_service =request.form.get("post_service", "").strip()
        delivery_type =request.form.get("delivery_type", "").strip()

        if not country or not city or not street or not comment or not post_service or not delivery_type:
                flash("Заповніть всі поля","alert-warning")
        else:           
            cart = session["cart"]
            cart_id = db.create_cart(cart)
            order_id = db.create_order(current_user.id,city,street,comment,cart_id,post_service,delivery_type)
            flash(f"Ваше замовлення оформлено. Ваш номер замовлення: №{order_id}","alert-success")
            session["cart"] = {}
            return redirect(url_for("index"))
        
    return render_template("order.html")


@app.route("/my_orders")
@login_required
def my_orders():
    orders = db.get_user_orders(current_user.id)

    return render_template("user_orders.html",orders=orders)



if __name__  == "__main__":
    app.run(debug=True)