import sqlite3 

class DatabaseManager:
    def __init__(self,dbname):
        self.dbname = dbname
        self.connect = None
        self.cursor = None

    def open(self):
        self.connect = sqlite3.connect(self.dbname)
        self.cursor = self.connect.cursor()
        
    def close(self):
        self.cursor.close()
        self.connect.close()

    def get_all_products(self):
        self.open()
        self.cursor.execute("""SELECT id,title,price,description,quantiti,image,category_id FROM products """)
        products = self.cursor.fetchall()
        self.close()
        return products
    
    def get_product(self,product_id):
        self.open()
        self.cursor.execute("""SELECT products.id,products.title,products.price,products.description,products.quantiti,products.image,categories.id,categories.title
                                FROM products
                                INNER JOIN  categories ON products.category_id=categories.id 
                                WHERE products.id =? """,[product_id])
        product = self.cursor.fetchone()
        self.close()
        return product
        
    def search_product(self,product_title):
        self.open()
        self.cursor.execute("""SELECT * FROM products WHERE title LIKE? """,['%'+product_title+'%'])
        products = self.cursor.fetchall()
        self.close()
        return products


    def search_title_categories(self,categorie):
        self.open()
        # self.cursor.execute("""SELECT id FROM categories WHERE title =? """,[categorie])
        # category_id = self.cursor.fetchone()[0]
        # self.cursor.execute("""SELECT * FROM products WHERE category_id =? """,[category_id])
        self.cursor.execute("""SELECT products.id,products.title,products.price,products.description,products.quantiti,products.image,categories.id,categories.title
                                FROM products
                                INNER JOIN  categories ON products.category_id=categories.id 
                                WHERE categories.english_title =? """,[categorie])
        products = self.cursor.fetchall()
        self.close()    
        return products
    

    def get_category_title(self,english_title):
        self.open()
        self.cursor.execute("""SELECT title FROM categories WHERE english_title =?""",[english_title])
        title = self.cursor.fetchone()
        self.close()
        return title


    def create_user(self, name, surname, email, phone_number, password):
        self.open()
        self.cursor.execute("""SELECT * FROM users WHERE email=? OR phone_number=?""",[email,phone_number])
        is_user_exist = self.cursor.fetchone()
        if is_user_exist:
            return False
        else:     
            self.cursor.execute("""INSERT INTO users (name,surname,email,phone_number,password)
                                    VALUES (?, ?, ?, ?, ?)""",[name, surname, email, phone_number, password])
            self.connect.commit()
            self.close()
            return True
        
    def check_user(self,email,password):
        self.open()
        self.cursor.execute("""SELECT * FROM users WHERE email=? AND password=?""",[email,password])
        user_register = self.cursor.fetchone()
        self.close()

        return user_register
    
    def get_user_by_id(self,id):
        self.open()
        self.cursor.execute("""SELECT * FROM users WHERE id=?""",[id])
        user_register = self.cursor.fetchone()
        self.close()

        return user_register
        
    def add_to_order(self,item_id,quantity,order_id):
        self.open()
        self.cursor.execute("""INSERT INTO product_in_order(order_id,product_id,quantity)
                                VALUES(?,?,?)""",[order_id,item_id,quantity])
        self.connect.commit()
        self.close()

    # def create_order(self,user_id):
    #     self.open()
    #     self.cursor.execute("""INSERT INTO orders(user_id, status)
    #                             VALUES(?,?)""",[user_id, "Нове замовлення"])
    #     order_id = self.cursor.lastrowid
    #     self.connect.commit()
    #     self.close()

    #     return order_id
        
    def submit_order(self,order_id,city,address,comment,status):
        self.open()
        self.cursor.execute("""UPDATE orders
                                SET city=?,address=?,comment=?,status=?
                                WHERE id=?""",[city,address,comment,status,order_id])
        self.connect.commit()
        self.close()

    def get_current_order(self,current_user_id ):
        self.open()
        self.cursor.execute("""SELECT id FROM orders WHERE user_id=? AND status=? """,[current_user_id,"Нове замовлення"])
        order = self.cursor.fetchone()

        self.close()
        return order 
    
    
    def get_order_list(self,order_id):
        self.open()
        self.cursor.execute("""SELECT pio.product_id,pio.quantity,p.title,p.price
                            FROM product_in_order pio
                            INNER JOIN products p ON pio.product_id = p.id
                            WHERE pio.order_id = ?
                            """,[order_id])
        products = self.cursor.fetchall()
        self.close()
        return products
    

    
    def get_all_categories(self):
        self.open()
        self.cursor.execute("""SELECT * FROM categories""")
        all_categories = self.cursor.fetchall()
        self.close()
        return all_categories
    
    def get_cart_product(self):
        self.open()
        self.cursor.execute("""SELECT * FROM cart""")

    def create_cart(self,cart):
        self.open()
        self.cursor.execute("""INSERT INTO carts(status) VALUES("new")""")
        cart_id = self.cursor.lastrowid#отримання id кошиика
        for product_id in cart:
            self.cursor.execute("""INSERT INTO product_in_cart(cart_id,product_id,quantity) VALUES(?,?,?)""",[cart_id,int(product_id),cart[product_id]])
        self.connect.commit()
        self.close()
        return cart_id

    def create_order(self,user_id,city,adress,comment,cart_id,post_service,delivery_type):
        self.open()
        self.cursor.execute("""INSERT INTO orders(user_id,city,address,comment,cart_id,post_service,delivery_type) VALUES(?,?,?,?,?,?,?)""",
                            [user_id,city,adress,comment,cart_id,post_service,delivery_type])
        order_id = self.cursor.lastrowid
        self.connect.commit()
        self.close()
        return order_id
    
    def get_user_orders(self,user_id):
        self.open()
        self.cursor.execute("""SELECT o.id,o.city,o.address,o.comment,o.cart_id,o.post_service,o.delivery_type,p.title,p.price,pic.quantity FROM orders o
                            INNER JOIN product_in_cart pic ON o.cart_id= pic.cart_id
                            INNER JOIN products p ON pic.product_id = p.id
                             WHERE o.user_id = ?
                            GROUP BY o.id   
                            """,[user_id])
        user_orders = self.cursor.fetchall()
        self.close()
        return user_orders

