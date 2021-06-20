import logging
import random

from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from service.apis.locations import filter_locations, SearchConfig

all_locations_info_link = "https://yourtrip.qbank.pro/public/data.php?type=all_objects"
trips = Blueprint("trips", __name__)
logging.basicConfig(filename='std.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level="INFO")


@trips.route("/pack", methods=["POST"])
def pack_trip_by_params():
    data = request.json
    try:
        cfg = SearchConfig(**data)
    except ValidationError as error:
        return str(error), 500

    available_locations = filter_locations(cfg)
    pack_size = random.randint(3, 5)
    tours = random.sample(available_locations, pack_size)
    return jsonify(tours)
