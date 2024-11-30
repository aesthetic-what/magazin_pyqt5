import pyodbc
# import sqlite3


class DataBase:
    def __init__(self, conn_str):
        self.connect = pyodbc.connect(conn_str)
        # self.connect = sqlite3.connect(file_name)
        self.cursor = self.connect.cursor()
        # self.admins_logins = admin_logins

    def check_user(self, login):
        with self.connect:
            result = self.cursor.execute("""SELECT * FROM users WHERE login = ?""", (login, )).fetchone()
            if result is not None:
                return False
            else:
                return True

    def login_user(self, login):
        with self.connect:
            return self.cursor.execute("""SELECT login, username, password, role FROM users WHERE login=(?)""", (login, )).fetchone()

    def add_user(self, login, username, password):
        with self.connect:
            return self.cursor.execute("""INSERT INTO users (login, username, role, password) VALUES (?, ?, ?, ?)""", (login, username, 'user', password))

