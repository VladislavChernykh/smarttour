import random

from flask import Blueprint, jsonify

users = Blueprint("users", __name__)


@users.route("/all", methods=["GET"])
def get_all_users():
    users_mock = []
    fnames = ["Олег", "Иван", "Андрей", "Николай", "Владислав", "Вячеслав", "Владимир", "Алексей", "Митрофан",
              "Аркадий", "Семён", "Илья", "Юрий"]
    lnames = ["Беляев", "Чернов", "Агутин", "Малинин", "Краснощёков", "Иванов", "Запашный", "Хорин", "Алексеев",
              "Желтов", "Краснов", "Прохоров"]
    for i in range(100):
        user = {
            "id": i,
            "first_name": random.choice(fnames),
            "last_name": random.choice(lnames),
        }
        users_mock.append(user)
    return jsonify(users_mock)
