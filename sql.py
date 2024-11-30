import pyodbc
# import sqlite3


class DataBase:
    def __init__(self, conn_str):
        self.connect = pyodbc.connect(conn_str)
        # self.connect = sqlite3.connect(file_name)
        self.cursor = self.connect.cursor()

    def get_info(self):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM users_tb""").fetchall()

    def get_info_r(self):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM users_right""").fetchall()

    def add_user(self, username, user_num, password):
        with self.connect:
            return self.cursor.execute("""INSERT INTO users_tb (username, user_last_name, user_role, user_password) VALUES (?, ?, ?, ?)""",
                                       (username, user_num, 'admin' if username == 'Тимур' else 'user', password, ))

    def add_user_r(self, username, user_num, password):
        with self.connect:
            return self.cursor.execute("""INSERT INTO users_right (username, user_lastname, user_role, user_password) VALUES (?, ?, ?, ?)""",
                                       (username, user_num, 'admin' if username == 'Тимур' else 'user', password, ))

    def update_user(self, user_id, username, last_name, password):
        with self.connect:
            return self.cursor.execute("""UPDATE users_tb SET username=(?), user_last_name = (?), user_password = (?) WHERE user_id=(?)""", (username, last_name, password, user_id))

    def delete_user(self, user_id, username, num, role, password):
        with self.connect:
            return self.cursor.execute("""DELETE FROM users_tb WHERE user_id=(?) AND username=(?) AND user_last_name=(?) AND user_role=(?) AND user_password=(?)""",
                                       (user_id, username, num, role, password))

    def delete_user_right(self, user_id, username, num, role, password):
        with self.connect:
            return self.cursor.execute("""DELETE FROM users_right WHERE user_id=(?) AND username=(?) AND user_lastname=(?) AND user_role=(?) AND user_password=(?)""",
                                       (user_id, username, num, role, password))

    def send_to_left_table(self, user_id, username, user_lastname, user_role, user_password):
        with self.connect:
            return self.cursor.execute("""INSERT INTO users_tb (user_id, username, user_lastname, user_role, user_password) VALUES (?, ?, ?, ?, ?)""",
                                       (user_id, username, user_lastname, user_role, user_password))
