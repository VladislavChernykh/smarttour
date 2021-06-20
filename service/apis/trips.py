import logging
import random
from typing import List

from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from service.apis.locations import filter_locations, SearchConfig, get_locations_info
from service.utils.categories import translate_categories, translate_tags

trips = Blueprint("trips", __name__)
logging.basicConfig(filename='std.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level="INFO")
MIN_GENERATED_TOUR_NUMBER = 3
MAX_GENERATED_TOUR_NUMBER = 5


@trips.route("/pack", methods=["POST"])
def pack_trip_by_params():
    data = request.json
    try:
        cfg = SearchConfig(**data)
    except ValidationError as error:
        return str(error), 500

    available_locations = filter_locations(cfg)
    pack_size = random.randint(MIN_GENERATED_TOUR_NUMBER, MAX_GENERATED_TOUR_NUMBER)
    random.shuffle(available_locations)
    tour_pack = []
    balance = cfg.budget[1]
    for location in available_locations:
        if balance <= 0 or len(tour_pack) > pack_size:
            return tour_pack

        providers = [provider for provider in location["providers"]]
        prices = list(filter(None, [provider["price"] for provider in providers]))
        price = random.choice(prices)
        if price < balance:
            balance -= price
            tour_pack.append(location)
    tour_pack = _translate_info(tour_pack)
    return jsonify(tour_pack)


@trips.route("/pack/random", methods=["GET"])
def pack_random_trip():
    locations_mock = get_locations_info()
    pack_size = random.randint(MIN_GENERATED_TOUR_NUMBER, MAX_GENERATED_TOUR_NUMBER)
    tour_pack = random.sample(locations_mock, pack_size)
    tour_pack = _translate_info(tour_pack)
    return jsonify(tour_pack)


def _translate_info(tour_pack) -> List[dict]:
    tour_pack = [translate_categories(loc) for loc in tour_pack]
    tour_pack = [translate_tags(loc) for loc in tour_pack]
    return tour_pack
