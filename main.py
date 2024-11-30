import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from app.sql_login_reg import DataBase

from admin_menu import AdminWindow
from register import RegisterWindow
from manager_menu import ManagerWindow
from user_product_list import ProductApp

from hashlib import md5

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'design/login_win.ui', self)
        self.setWindowTitle('Авторизация')

        #Подключение базы данных
        self.db = DataBase(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=KLABSQLW19S1,49172;Trusted_Connection=yes; '
        'user=22200322; Database=DB_for_python_lessons;')

        # Подключение кнопок
        self.login_btn.clicked.connect(self.login)
        self.reg_btn.clicked.connect(self.register)
        self.guest_button.clicked.connect(self.guest)

    def guest(self):
        self.shop = ProductApp()
        self.shop.show()
        self.close()

    def login(self):
        try:
            login_line = self.login_line.text()
            password_line = self.password_line.text()

            if not login_line or not password_line:
                QMessageBox.warning(self, 'Ошибка', 'Вы не заполнили все поля')
                return

            # hash_login = md5(login_line.encode('utf-8')).hexdigest()
            # hash_pass = md5(password_line.encode('utf-8')).hexdigest()
            
            login, name, password, role = self.db.login_user(login_line)

            print(f'Имя: {name}\nПароль: {password}\nРоль: {role}')
            if not password_line == password or not login_line == login:
                QMessageBox.warning(self, 'ошибка', 'Вы ввели неправильный пароль')
                return
                
            if role == 'admin':
                QMessageBox.information(self, 'Успех', f'Вы успешно авторизовались как админ.\nДобро пожаловать {name}')
                self.open_admin_window()
            elif role == 'manager':
                QMessageBox.information(self, 'Успех', f'Вы успешно авторизовались как менеджер.\nДобро пожаловать {name}')
                self.open_manager_window()

            else:
                QMessageBox.information(self, 'Успех', f'Вы успешно авторизовались как пользователь.\nДобро пожаловать {name}')
                self.open_shop_win()
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', 'Такого ползователя нет')
            print(e)

    def open_shop_win(self):
        self.shop = ProductApp()
        self.shop.show()
        self.close()

    def open_admin_window(self):
        self.admin = AdminWindow()
        self.admin.show()
        self.close()

    def open_manager_window(self):
        self.manager = ManagerWindow()
        self.manager.show()
        self.close()

    def register(self):
       self.reg_window = RegisterWindow()
       self.reg_window.show()
       self.close() 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())