import psycopg2

class BotDB:

    def __init__(self, db_uri):  # initialization bd
        self.conn = psycopg2.connect(db_uri)
        self.cursor = self.conn.cursor()

    # def user_exists(self, user_id):
    #     result = self.cursor.execute("SELECT 'id' FROM 'users' WHERE 'users_id' = ?", (user_id,))
    #     return bool(len(result.fetchall()))

    # def get_user_id(self, user_id):  # get a user info
    #     result = self.cursor.execute("SELECT 'id' FROM 'users' WHERE 'users_id' = ?", (user_id,))
    #     return result.fetchone()[0]

    def add_data(self, user_id, join_user_day):  # add user id and join day to bd
        self.cursor.execute("INSERT INTO users(user_id, join_data_day) VALUES (%s, %s)", (user_id, join_user_day))
        return self.conn.commit()

    # def get_day(self, join_user_day):  # get a join day info
    #     result = self.cursor.execute("SELECT 'id' FROM 'users' WHERE 'join_date_day' = ?", (join_user_day,))
    #     return result.fetchone()[0]

    def close(self):  # close bd
        self.conn.close()