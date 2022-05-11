import sqlite3

class BotDB:

    def __init__(self, db_file):  # initialization bd
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT 'id' FROM 'users' WHERE 'users_id' = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        result = self.cursor.execute("SELECT 'id' FROM 'users' WHERE 'users_id' = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id):
        self.cursor.execute("INSERT INTO 'users' ('user_id') VALUES (?)", (user_id,))
        return self.conn.commit()

    def add_day(self, join_user_day):
        self.cursor.execute("INSERT INTO 'users' ('join_date_day') VALUES (?)", (join_user_day,))
        return self.conn.commit()

    def get_day(self, join_user_day):
        result = self.cursor.execute("SELECT 'id' FROM 'users' WHERE 'join_date_day' = ?", (join_user_day,))
        return result.fetchone()[0]

    def add_hour(self, join_user_hour):
        self.cursor.execute("INSERT INTO 'users' ('join_date_hour') VALUES (?)", (join_user_hour,))
        return self.conn.commit()

    def get_day(self, join_user_hour):
        result = self.cursor.execute("SELECT 'id' FROM 'users' WHERE 'join_date_hour' = ?", (join_user_hour,))
        return result.fetchone()[0]

    def close(self):  # close bd
        self.conn.close()