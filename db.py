import sqlite3

class BotDB:

    def __init__(self, db_file):  # initialization bd
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT 'id' FROM 'users' WHERE 'users_id' = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):  # get a user info
        result = self.cursor.execute("SELECT 'id' FROM 'users' WHERE 'users_id' = ?", (user_id,))
        return result.fetchone()[0]

    def add_data(self, user_id, join_user_day):  # add user id and join day to bd
        self.cursor.execute("INSERT INTO 'users' (users_id, join_date_day) VALUES (?, ?)", (user_id, join_user_day))
        return self.conn.commit()

    def get_day(self, join_user_day):  # get a join day info
        result = self.cursor.execute("SELECT 'id' FROM 'users' WHERE 'join_date_day' = ?", (join_user_day,))
        return result.fetchone()[0]

    def close(self):  # close bd
        self.conn.close()