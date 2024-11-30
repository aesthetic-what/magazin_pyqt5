from PyQt5.QtWidgets import QMainWindow, QMessageBox
from app.sql_login_reg import DataBase
from PyQt5 import uic

# from hashlib import md5

class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'design/register_win.ui', self)
        self.setWindowTitle('Регистрация')

        # connect database
        self.db = DataBase(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=KLABSQLW19S1,49172;Trusted_Connection=yes; '
        'user=22200322; Database=DB_for_python_lessons;')

        #connect button
        self.login_btn.clicked.connect(self.login)
        self.reg_btn.clicked.connect(self.register)

    def login(self):
        from main import LoginWindow
        self.login_win = LoginWindow()
        self.login_win.show()
        self.close()

    def register(self):
        login = self.login_line.text()
        username = self.username_line.text()
        password = self.password_line.text()
        conf_password = self.conf_password_line.text()

        # hash_login = md5(login.encode('utf-8')).hexdigest()
        # hash_pass = md5(password.encode('utf-8')).hexdigest()
        
        if not login or not username or not password or not conf_password:
            QMessageBox.warning(self, 'Warning', 'Вы не заполнили все поля')
            return

        unique_login = self.db.check_user(login)
        if not unique_login:
            QMessageBox.information(self, 'Предупреждение', 'Пользователь с таким логином уже есть')
            return
        else:
            self.db.add_user(login, username, password)
            QMessageBox.information(self, 'Congrat', 'Вы успешно зарегистрировались')