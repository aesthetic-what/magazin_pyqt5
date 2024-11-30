from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic

from app.sql_admin import DataBase


class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"design\main_window.ui", self)
        self.setWindowTitle("DataBase")
        self.db = DataBase(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=KLABSQLW19S1,49172;Trusted_Connection=yes; '
        'user=22200322; Database=DB_for_python_lessons;')
        # Объявление таблицы
        self.model_left = QStandardItemModel(self)
        self.leftTable.setModel(self.model_left)
        self.model_left.setHorizontalHeaderLabels(
            ['ID', 'Имя', 'Номер телефона', 'Роль', 'Пароль', 'Хеш пароля'])
        self.load_data()

        self.model_right = QStandardItemModel(self)
        self.rightTable.setModel(self.model_right)
        self.model_right.setHorizontalHeaderLabels(
            ['ID', 'Имя', 'Номер телефона', 'Роль', 'Пароль', 'Хеш пароля'])
        self.load_right_data()

        # Подключение кнопок
        self.addButton.clicked.connect(self.add_data_button)
        self.delButton_l.clicked.connect(self.delete)
        self.delButton_r.clicked.connect(self.delete_r)
        self.editButton.clicked.connect(self.edit_data_button)
        self.send_to_left.clicked.connect(self.send_to_left_Button)
        self.send_to_right.clicked.connect(self.send_to_right_Button)

    def add_data_button(self):
        self.add = AddDataWindow(self.db)
        self.add.setFixedSize(406, 279)
        self.add.data_added.connect(self.load_data)
        self.add.data_added_r.connect(self.load_right_data)
        self.add.show()

    def send_to_left_Button(self):
        selected_index = self.rightTable.selectedIndexes()
        if not selected_index:
            QMessageBox.warning(self, 'Предупреждение',
                                'Пожалуйста, выберите строку для удаления.')
            return

        row_to_send = selected_index[0].row()
        selected_user_id = self.model_right.item(row_to_send, 0).text()
        selected_login = self.model_right.item(row_to_send, 1).text()
        selected_username = self.model_right.item(row_to_send, 2).text()
        selected_user_role = self.model_right.item(row_to_send, 3).text()
        selected_user_password = self.model_right.item(row_to_send, 4).text()
        new_row = [QStandardItem(self.model_right.item(row_to_send, col).text())
                   for col in range(self.model_left.columnCount())]
        self.db.send_to_left_table(
                         selected_login,
                         selected_username,
                         selected_user_role,
                         selected_user_password)
        self.db.delete_user_right(selected_user_id,
                                  selected_login,
                                  selected_username,
                                  selected_user_role,
                                  selected_user_password)
        self.model_left.appendRow(new_row)
        self.model_right.removeRow(row_to_send)

    def send_to_right_Button(self):
        selected_index = self.leftTable.selectedIndexes()
        if not selected_index:
            QMessageBox.warning(self, 'Предупреждение',
                                'Пожалуйста, выберите строку для удаления.')
            return

        row_to_send = selected_index[0].row()
        selected_user_id = self.model_left.item(row_to_send, 0).text()
        selected_login = self.model_left.item(row_to_send, 1).text()
        selected_username = self.model_left.item(row_to_send, 2).text()
        selected_user_role = self.model_left.item(row_to_send, 3).text()
        selected_user_password = self.model_left.item(row_to_send, 4).text()
        new_row = [QStandardItem(self.model_left.item(row_to_send, col).text())
                   for col in range(self.model_left.columnCount())]

        self.db.send_to_right_table(
                           selected_login,
                           selected_username,
                           selected_user_role,
                           selected_user_password)
        self.db.delete_user(selected_user_id,
                            selected_login,
                            selected_username,
                            selected_user_role,
                            selected_user_password)
        self.model_right.appendRow(new_row)
        self.model_left.removeRow(row_to_send)

    def load_data(self):
        self.model_left.clear()
        data = self.db.get_info()

        for row in data:
            # print(row)
            items = [QStandardItem(str(field)) for field in row]
            self.model_left.appendRow(items)

    def load_right_data(self):
        self.model_right.clear()
        data = self.db.get_info_r()

        for row in data:
            # print(row)
            items = [QStandardItem(str(field)) for field in row]
            self.model_right.appendRow(items)

    def add_data_button(self):
        self.add = AddDataWindow(self.db)
        self.add.setFixedSize(406, 400)
        self.add.data_added.connect(self.load_data)
        self.add.data_added_r.connect(self.load_right_data)
        self.add.show()

    def delete(self):
        selected_index_l = self.leftTable.selectedIndexes()
        if not selected_index_l:
            QMessageBox.warning(self, 'Предупреждение',
                                'Пожалуйста, выберите строку для удаления.')
            return

        row_to_delete = selected_index_l[0].row()
        selected_user_id = self.model_left.item(row_to_delete, 0).text()
        selected_username = self.model_left.item(row_to_delete, 1).text()
        selected_user_last_name = self.model_left.item(row_to_delete, 2).text()
        selected_user_role = self.model_left.item(row_to_delete, 3).text()
        selected_user_password = self.model_left.item(row_to_delete, 4).text()


        try:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Подтверждение")
            msg_box.setText("Вы уверены, что хотите продолжить?")
            msg_box.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
            result = msg_box.exec_()
            if result == QMessageBox.Ok:
                self.db.delete_user(selected_user_id, selected_username,
                                    selected_user_last_name, selected_user_role, selected_user_password)
                print(selected_user_id, selected_username, selected_user_last_name,
                      selected_user_role, selected_user_password)
                QMessageBox.information(
                    self, 'Успех', 'Данные удалены успешно.')
                self.model_left.removeRow(row_to_delete)
            else:
                QMessageBox.information(self, 'Успех', 'Действие отменено')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', str(e))
            print(e)
        

    def delete_r(self):
        selected_index = self.rightTable.selectedIndexes()
        if not selected_index:
            QMessageBox.warning(self, 'Предупреждение',
                                'Пожалуйста, выберите строку для удаления.')
            return

        row_to_delete_r = selected_index[0].row()
        user_id_r = self.model_right.item(row_to_delete_r, 0).text()
        username_r = self.model_right.item(row_to_delete_r, 1).text()
        user_lastname_r = self.model_right.item(row_to_delete_r, 2).text()
        user_role_r = self.model_right.item(row_to_delete_r, 3).text()
        user_password_r = self.model_right.item(row_to_delete_r, 4).text()

        try:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Подтверждение")
            msg_box.setText("Вы уверены, что хотите продолжить?")
            msg_box.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
            result = msg_box.exec_()
            if result == QMessageBox.Ok:
                self.db.delete_user_right(user_id_r, username_r,
                                    user_lastname_r, user_role_r, user_password_r)
                # print(selected_user_id, selected_username, selected_user_last_name,
                #       selected_user_role, selected_user_password)
                QMessageBox.information(
                    self, 'Успех', 'Данные удалены успешно.')
                self.model_right.removeRow(row_to_delete_r)
            else:
                QMessageBox.information(self, 'Успех', 'Действие отменено')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', str(e))
            print(e)
 

    def edit_data_button(self):
        selected_index = self.leftTable.selectedIndexes()
        if not selected_index:
            QMessageBox.warning(self, 'Предупреждение',
                                'Пожалуйста, выберите строку для удаления.')
            return

        row_to_delete = selected_index[0].row()
        val_user_id = self.model_left.item(row_to_delete, 0).text()
        val_username = self.model_left.item(row_to_delete, 1).text()
        val_user_last_name = self.model_left.item(row_to_delete, 2).text()
        val_user_role = self.model_left.item(row_to_delete, 3).text()
        val_user_password = self.model_left.item(row_to_delete, 4).text()
        self.edit = EditDataWindow(
            self.db, val_user_id, val_username, val_user_last_name, val_user_role, val_user_password)
        self.edit.setFixedSize(406, 319)
        self.edit.data_edit.connect(self.load_data)
        self.edit.show()


class AddDataWindow(QMainWindow):
    data_added = pyqtSignal()
    data_added_r = pyqtSignal()

    def __init__(self, db):
        super().__init__()
        uic.loadUi(r"design\add_data_form.ui", self)
        self.setWindowTitle("Add data")
        self.model = QStandardItemModel(self)
        self.pushButton.clicked.connect(self.append_data)
        self.right_table.clicked.connect(self.append_data_r)
        self.db = db
        self.main_window = AdminWindow()

    def append_data(self):
        username = self.lineEdit.text()
        last_name = self.lineEdit_2.text()
        password = self.lineEdit_3.text()
        self.db.add_user(username, last_name, password)
        self.data_added.emit()
        # Уведомление и завершение работы окна Add_data_window
        QMessageBox.information(self, "Успех", "Данные успешно добавлены")
        AddDataWindow.close(self)

    def append_data_r(self):
        username = self.lineEdit.text()
        last_name = self.lineEdit_2.text()
        password = self.lineEdit_3.text()
        self.db.add_user_r(username, last_name, password)
        self.data_added_r.emit()
        # Уведомление и завершение работы окна Add_data_window
        QMessageBox.information(self, "Успех", "Данные успешно добавлены")
        AddDataWindow.close(self)


class EditDataWindow(QMainWindow):
    data_edit = pyqtSignal()

    def __init__(self, db, val_user_id, val_username, val_last_name, val_user_role, val_user_password):
        super().__init__()
        uic.loadUi(r"design\edit_data.ui", self)
        self.setWindowTitle("Edit data")
        self.model = QStandardItemModel(self)
        self.pushButton.clicked.connect(self.edit_data)
        self.db = db
        self.NameEdit.setText(val_username)
        self.LastnameEdit.setText(val_last_name)
        self.PassEdit.setText(val_user_password)
        self.RoleEdit.setText(val_user_role)
        self.user_id = val_user_id
        print(f"\nИмя пользователя: {val_username},\n ID: {val_user_password}\nrole: {val_user_role}")

    def edit_data(self):
        try:
            new_login = self.NameEdit.text()
            new_username = self.LastnameEdit.text()
            new_role = self.RoleEdit.text()
            new_password = self.PassEdit.text()
            # добавление данных в БД
            self.db.update_user(self.user_id, new_login, new_username,
                                new_role, new_password)
            self.data_edit.emit()
            QMessageBox.information(self, "Успех", "Данные обновлены")
            EditDataWindow.close(self)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", "Не удалось выполнить запрос(")
            print(f"Запрос не удалось реализовать(. Ошибка: {e}")

