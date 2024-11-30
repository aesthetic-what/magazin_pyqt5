import pyodbc

class DataBase:
    def __init__(self, str_conn):
        self.connect = pyodbc.connect(str_conn)
        self.cursor = self.connect.cursor()

    def get_info(self):
        """
        Это функция для вывода товаров в каталог
        """
        with self.connect:
            return self.cursor.execute("""SELECT product_id, product_name, price, count, path FROM products_tb""").fetchall()

    def buy_prod(self, count, product_name):
        """
        Покупка товара
        """
        with self.connect:
            return self.cursor.execute("""UPDATE products_tb SET count=(?) WHERE product_name=(?)""", (count, product_name,))

    def change_info(self, articule, new_name):
        """При отстутсвии товара (количество = 0) изменяет название товара"""
        with self.connect:
            return self.cursor.execute("""UPDATE products_tb SET product_name=(?) WHERE product_id=(?)""", (articule, new_name))