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
        self.cursor.execute("""SELECT id,title,price FROM products """)
        products = self.cursor.fetchall()
        self.close()
        return products
    
    def get_product(self,product_id):
        self.open()
        self.cursor.execute("""SELECT * FROM products WHERE id =? """,[product_id])
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
        self.cursor.execute("""SELECT products.id,products.title,products.price,categories.title
                                FROM products
                                INNER JOIN  categories ON products.category_id=categories.id 
                                WHERE categories.title =? """,[categorie])
        products = self.cursor.fetchall()
        self.close()    
        return products
    
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
        
    def add_to_order(self,item_id,quantity,order_id):
        self.open()
        self.cursor.execute("""INSERT INTO product_in_order(order_id,product_id,quantity)
                                VALUES(?,?,?)""",[order_id,item_id,quantity])
        self.connect.commit()
        self.close()

    def create_order(self,user_id):
        self.open()
        self.cursor.execute("""INSERT INTO orders(user_id, status)
                                VALUES(?,?)""",[user_id, "Нове замовлення"])
        order_id = self.cursor.lastrowid
        self.connect.commit()
        self.close()

        return order_id
        
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