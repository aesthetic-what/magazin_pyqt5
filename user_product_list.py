import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize, Qt
from PyQt5 import uic

from app.sql_user import DataBase

class ProductApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Продуктовый интерфейс")
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=KLABSQLW19S1,49172;Trusted_Connection=yes;user=22200322;Database=DB_for_python_lessons;'
        uic.loadUi('design/shop_window.ui', self)
        # Основной виджет и макет
        self.db = DataBase(conn_str)
        # Список товаров
        self.shop_list.setIconSize(QSize(100, 100))  # Размер иконки
        self.load_products()
        self.buy_button.clicked.connect(self.buy_prod)
        self.exit_button.clicked.connect(self.exit)

    def parse_item_text(self, item_text):
        parts = item_text.split()
        try:
            price_index = parts.index("Цена:")
            count_index = parts.index("Количество:")
            article = parts[1]
            product_name = ' '.join(parts[2:price_index])
            price = parts[price_index + 1]
            count = parts[count_index + 1]
            return {
                "article": article,
                "product_name": product_name,
                "price": price,
                "count": count
            }
        except ValueError as e:
            print(f"Ошибка при обработке текста: {e}")
            return None

    def buy_prod(self):
        try:
            cur_item = self.shop_list.currentItem()
            item_text = self.shop_list.currentItem().text()
            parsed_data = self.parse_item_text(item_text)
            if parsed_data:
                article = int(parsed_data["article"])
                product_name = parsed_data["product_name"]
                price = int(parsed_data["price"])
                count = int(parsed_data["count"])
                # print(f"Art: {parsed_data['article']}")
                # print(f"Name: {parsed_data['product_name']}")
                # print(f"Price: {parsed_data['price']}")
                # print(f"Count: {parsed_data['count']}")

                # Если товар отсутствует, то вывести ошибку
                if count == 0:
                    QMessageBox.warning(self, 'Ошибка', 'Товар отсутсвует или нет в наличии')
                    return

                # messageBox
                msg_box = QMessageBox()
                msg_box.setWindowTitle('Подтвердите')
                msg_box.setText('Подтвердие покупку')
                msg_box.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
                result = msg_box.exec_()

                if result == QMessageBox.Ok:

                    print(count)
                    count -= 1
                    self.db.buy_prod(count, product_name)
                    print(count)
                    prod_list = [f"Артикул: {article}\n {product_name}\n Цена: {price} руб.\n Количество: {count}"]
                    cur_item.setText(' '.join(map(str, prod_list)))
                    QMessageBox.information(self, 'Успех', 'товар успешно куплен')
                elif result == QMessageBox.Cancel:
                    QMessageBox.information(self, 'Отмена', 'Покупка отменена')
        except ValueError as e:
            print(f"Ошибка при обработке текста: {e}")
            return None
        # processed_item = [int(item) if item.isdigit() else str(item) for item in item_list]
        # print(processed_item)
        # print(processed_item[3], type(processed_item[3]))


    def exit(self):
        from main import LoginWindow
        self.login_win = LoginWindow()
        self.login_win.show()
        self.close()

    def load_products(self):
        # Запрос для получения данных

        for row in self.db.get_info():
            id, name, price, count, path = row
            print(id, name, price, count)
            if count == 0:
                name = name + ' (нет в наличии)'

            # Создание элемента списка
            item = QListWidgetItem(f"Артикул: {id} \n {name} \n Цена: {price} руб.\n Количество: {count}")
            pixmap = QPixmap(f'photo/{path}').scaled(100, 100)  # Подгрузка изображения
            icon = QIcon(pixmap)
            item.setIcon(icon)

            self.shop_list.addItem(item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProductApp()
    window.show()
    sys.exit(app.exec_())