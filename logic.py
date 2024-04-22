from db import DataBase


def check_user(user_id: int):
    db = DataBase("../Bot_for_accounting_money/database")
    id_list = db.get_id_list()
    print(user_id)
    return True if user_id in id_list else False


def start_registration(user_id, user_nic, user_password):
    db = DataBase("../Bot_for_accounting_money/database")
    db.registration_user(user_id, user_nic, user_password)


def check_string_for_password(str) -> bool:
    if len(str) > 5 or len(str) < 3 or not str.isalnum():
        return False
    return True


def add_question_and_answer(question, answer, user_id):
    db = DataBase("../Bot_for_accounting_money/database")
    db.add_question_and_answer(question, answer, user_id)


def check_password(password, user_id):
    db = DataBase("../Bot_for_accounting_money/database")
    if password == db.get_password(user_id):
        return True
    else:
        return False


def get_question(user_id):
    db = DataBase("../Bot_for_accounting_money/database")
    question = db.get_question(user_id)
    return question


def get_answer(user_id):
    db = DataBase("../Bot_for_accounting_money/database")
    answer = db.get_answer(user_id)
    return answer


def get_password(user_id):
    db = DataBase("../Bot_for_accounting_money/database")
    return db.get_password(user_id)


def add_income(income, user_id, category):
    db = DataBase("../Bot_for_accounting_money/database")
    db.add_income(income, user_id, category)


def check_income(income):
    if income.isdigit():
        return True
    else:
        return False


def get_income_category(user_id):
    db = DataBase("../Bot_for_accounting_money/database")
    lst = list(set(db.get_income_category(user_id)))
    return lst