import pyodbc

class DataBase:
    def __init__(self, conn_str):
        self.connect = pyodbc.connect(conn_str)
        self.cursor = self.connect.cursor()

    def get_info(self):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM products_tb""").fetchall()

    def add_product(self, product_name, price, count, product_path):
        with self.connect:
            return self.cursor.execute("""INSERT INTO products_tb (product_name, price, count, path) VALUES (?, ?, ?, ?)""", 
            (product_name, price, count, product_path))

    def update_product(self, product_id, product_name, price, count, path):
        with self.connect:
            return self.cursor.execute("""UPDATE products_tb SET product_name=(?), price=(?), count=(?), path=(?) WHERE product_id=(?)""", (product_name, price, count, path, product_id))
        
    def delete_user(self, product_id, product_name, price, count, path):
        with self.connect:
            return self.cursor.execute("""DELETE FROM products_tb WHERE product_id = (?) AND product_name = (?) AND price = (?) AND count = (?) AND path=(?)""", 
                                        (product_id, product_name, price, count, path))