from flask import Blueprint, jsonify

users = Blueprint("users", __name__)


@users.route("/all", methods=["GET"])
def get_all_users():
    users_mock = [
        {
            "id": 1,
            "first_name": "Олег",
            "last_name": "Олегов",
        },
        {
            "id": 2,
            "first_name": "Иван",
            "last_name": "Иванов",
        }
    ]
    return jsonify(users_mock)

# @locations.route("/get_by_category", methods=["GET"])
# def get_all_locations():