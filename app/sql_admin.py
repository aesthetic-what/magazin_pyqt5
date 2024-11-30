import pyodbc
# import sqlite3


class DataBase:
    def __init__(self, conn_str):
        self.connect = pyodbc.connect(conn_str)
        self.cursor = self.connect.cursor()

    def get_info(self):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM users""").fetchall()

    def get_info_r(self):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM users_right""").fetchall()

    def add_user(self, login, username, password):
        with self.connect:
            return self.cursor.execute("""INSERT INTO users (login, username, role, password) VALUES (?, ?, ?, ?)""",
                                       (login, username, 'user', password, ))

    def add_user_r(self, login, username, password):
        with self.connect:
            return self.cursor.execute("""INSERT INTO users_right (login, username, role, password) VALUES (?, ?, ?, ?)""",
                                       (login, username, 'user', password, ))

    def update_user(self, user_id, login, username, role, password):
        with self.connect:
            return self.cursor.execute("""UPDATE users SET login=(?), username=(?), role=(?), password=(?) WHERE user_id=(?)""", (login, username, role, password, user_id))

    def delete_user(self, user_id, login, username, role, password):
        with self.connect:
            return self.cursor.execute("""DELETE FROM users WHERE user_id=(?) AND login=(?) AND username=(?) AND role=(?) AND password=(?)""",
                                       (user_id, login, username, role, password))

    def delete_user_right(self, user_id, login, username, role, password):
        with self.connect:
            return self.cursor.execute("""DELETE FROM users_right WHERE user_id=(?) AND login=(?) AND username=(?) AND role=(?) AND password=(?)""",
                                       (user_id, login, username, role, password))

    def send_to_left_table(self, login, username, role, password):
        with self.connect:
            return self.cursor.execute("""INSERT INTO users (login, username, role, password) VALUES (?, ?, ?, ?)""",
                                       (login, username, role, password))

    def send_to_right_table(self, login, username, role, password):
        with self.connect:
            return self.cursor.execute("""INSERT INTO users_right (login, username, role, password) VALUES (?, ?, ?, ?)""",
                                       (login, username, role, password))
