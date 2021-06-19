from flask import Blueprint, jsonify

locations = Blueprint("locations", __name__)


@locations.route("/all", methods=["GET"])
def get_all_locations():
    locations_mock = [
        {
            "id": 1,
            "name": "Rosa Khutor",
            "alias": "Роза Хутор",
            "categories": ["mountains", "active", "hot"],
            "tags": [""],
            "providers": [
                {
                    "id": 1,
                    "name": "provider1",
                    "price": 3000,
                    "time_available": "9-16"
                },
                {
                    "id": 2,
                    "name": "provider2",
                    "price": 3200,
                    "time_available": "10-17"
                }
            ]
        },
        {
            "id": 2,
            "name": "Agursky waterfalls",
            "alias": "Агурские водопады",
            "categories": ["nature", "waterfalls"],
            "tags": [""],
            "providers": [
                {
                    "id": 1,
                    "name": "provider1",
                    "price": 1000,
                    "time_available": "9-16"
                }
            ]
        }
    ]
    return jsonify(locations_mock)

# @locations.route("/get_by_category", methods=["GET"])
# def get_all_locations():