from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic

import sys, pyodbc

from app.sql_manager import DataBase


class Edit_data_window(QMainWindow):
    data_edit = pyqtSignal()
    def __init__(self, db, val_product_id, val_product_name, val_product_price, val_product_count, val_product_path):
       super().__init__()
       uic.loadUi(r"design\edit_data_form.ui", self)
       self.setWindowTitle("Edit data")
       self.model = QStandardItemModel(self)
       self.pushButton.clicked.connect(self.edit_data)
       self.db = db
       self.name_input.setText(val_product_name)
       self.price_input.setText(val_product_price)
       self.count_input.setText(val_product_count)
       self.path_input.setText(val_product_path)
       self.product_id = val_product_id
       print(f"\nproduct name: {val_product_name},\n ID: {val_product_id}\n")
    def edit_data(self):              
        try:
            new_product_name = self.name_input.text()
            new_product_price = self.price_input.text()
            new_product_count = self.count_input.text()
            new_product_path = self.path_input.text()
            print(f"\nproduct_name: {new_product_name},\n product_price: {new_product_price}\nproduct_count: {new_product_count}")
            # добавление данных в БД
            self.db.update_product(self.product_id, new_product_name, new_product_price, new_product_count, new_product_path)
            self.data_edit.emit()
            QMessageBox.information(self, "Успех", "Данные обновлены")
            Edit_data_window.close(self)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", "Не удалось выполнить запрос(")
            print(f"Запрос не удалось реализовать(. Ошибка: {e}")


class ManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"design\manager_win.ui", self)
        self.setWindowTitle("DataBase")
        self.db = DataBase(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=KLABSQLW19S1,49172;Trusted_Connection=yes; '
        'user=22200322; Database=DB_for_python_lessons;')
        # Объявление таблицы
        self.model = QStandardItemModel(self)
        self.tableView.setModel(self.model)
        # self.model.setHorizontalHeaderLabels(['ID', 'Имя', 'Номер телефона', 'Роль', 'Пароль', 'Хеш пароля'])
        self.load_data()

        # Подключение кнопок
        self.add_data.clicked.connect(self.add_data_button)
        self.del_data.clicked.connect(self.delete)
        self.edit_data.clicked.connect(self.edit_data_button)

    def load_data(self):
        self.model.clear()
        data = self.db.get_info()

        for row in data:
            print(row)
            items = [QStandardItem(str(field)) for field in row]
            self.model.appendRow(items)
    
    def close_data(self):
        close = self.db.close_db(self.database)

        if not close:
            print("База данных активна")
        else:
            pyodbc.pooling = False
            print("База данных выключена")

    def add_data_button(self):
        self.add = Add_data_window(self.db)
        self.add.setFixedSize(317, 363)
        self.add.data_added.connect(self.load_data)
        self.add.show()

    def delete(self):
        selected_index = self.tableView.selectedIndexes()
        if not selected_index:
            QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста, выберите строку для удаления.')
            return

        row_to_delete = selected_index[0].row()
        val_product_id = self.model.item(row_to_delete, 0).text()
        val_product_name = self.model.item(row_to_delete, 1).text()
        val_product_price = self.model.item(row_to_delete, 2).text()
        val_product_count = self.model.item(row_to_delete, 3).text()
        val_product_path = self.model.item(row_to_delete, 4).text()     


        try:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Подтверждение")
            msg_box.setText("Вы уверены, что хотите продолжить?")
            msg_box.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
            result = msg_box.exec_()
            if result == QMessageBox.Ok:
                self.db.delete_user(val_product_id, val_product_name, val_product_price, val_product_count, val_product_path)
                # print(selected_user_id, selected_username, selected_user_last_name, selected_user_role, selected_user_password)
                QMessageBox.information(self, 'Успех', 'Данные удалены успешно.')
                self.model.removeRow(row_to_delete)
            else:
                QMessageBox.information(self, 'Успех', 'Действие отменено')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', str(e))
            print(e)



    def edit_data_button(self):
        selected_index = self.tableView.selectedIndexes()
        if not selected_index:
            QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста, выберите строку для удаления.')
            return

        row_to_delete = selected_index[0].row()
        val_product_id = self.model.item(row_to_delete, 0).text()
        val_product_name = self.model.item(row_to_delete, 1).text()
        val_product_price = self.model.item(row_to_delete, 2).text()
        val_product_count = self.model.item(row_to_delete, 3).text()
        val_product_path = self.model.item(row_to_delete, 4).text()       
        self.edit = Edit_data_window(self.db, val_product_id, val_product_name, val_product_price, val_product_count, val_product_path)
        self.edit.setFixedSize(406, 387)
        self.edit.data_edit.connect(self.load_data)
        self.edit.show()
        

class Add_data_window(QMainWindow):
    data_added = pyqtSignal()
    def __init__(self, db):
       super().__init__()
       uic.loadUi(r"design\manager_add_product.ui", self)
       self.setWindowTitle("Add data")
       self.model = QStandardItemModel(self)
       self.pushButton.clicked.connect(self.append_data)
       self.db = db
       self.main_window = ManagerWindow()

    def append_data(self):
        product_name = self.product_name.text()
        price = self.product_price.text()
        count = self.product_count.text()
        path = self.product_path.text()
        self.db.add_product(product_name, int(price), int(count), path)
        self.data_added.emit()
        # Уведомление и завершение работы окна Add_data_window
        QMessageBox.information(self, "Успех", "Данные успешно добавлены")
        Add_data_window.close(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ManagerWindow()
    window.setFixedSize(784, 600)
    window.show()
    sys.exit(app.exec())

