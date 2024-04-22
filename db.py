import sqlite3


class DataBase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def registration_user(self, user_id, nic, user_password):
        with self.connection:
            self.cursor.execute(f"INSERT INTO users (`user_id`, `user_nic`, `user_password`) "
                                f"VALUES({user_id}, '{nic}', '{user_password}')")

    def get_info(self):
        with self.connection:
            # a = self.cursor.execute("SELECT user_password FROM users WHERE user_id = 1635382551").fetchone()
            a = self.cursor.execute("SELECT * FROM users").fetchall()
            for el in a:
                print(el[3])

    def get_id_list(self):
        with self.connection:
            lst = self.cursor.execute("SELECT user_id FROM users").fetchall()
            id_list = []
            for el in lst:
                id_list.append(el[0])
            return id_list

    def add_question_and_answer(self, question, answer, user_id):
        with self.connection:
            self.cursor.execute(f"UPDATE users SET `question` = '{question}',"
                                f"`answer` = '{answer}'where `user_id` =  {user_id}")

    def get_password(self, user_id):
        with self.connection:
            password = self.cursor.execute(f"SELECT user_password FROM "
                                           f"users WHERE user_id = '{user_id}'").fetchall()
            return password[0][0]

    def get_question(self, user_id):
        with self.connection:
            question = self.cursor.execute(f"SELECT question FROM "
                                           f"users WHERE user_id = '{user_id}'").fetchall()
            return question[0][0]

    def get_answer(self, user_id):
        with self.connection:
            answer = self.cursor.execute(f"SELECT answer FROM "
                                         f"users WHERE user_id = '{user_id}'").fetchall()
            return answer[0][0]

    def add_income(self, income, user_id, category):
        with self.connection:
            self.cursor.execute(f"INSERT INTO users_data (`user_id`, `income`, `income_category`) "
                                f"VALUES({user_id}, '{income}', '{category}')")

    def get_income_category(self, user_id):
        with self.connection:
            income_category = self.cursor.execute(f"SELECT income_category FROM "
                                                  f"users_data WHERE user_id = '{user_id}'").fetchall()
        return [i[0] for i in income_category]