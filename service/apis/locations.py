import logging
import math
from datetime import timedelta, datetime
from typing import List, Optional, Tuple

import requests
from flask import Blueprint, jsonify, request
from pydantic import BaseModel, ValidationError

from service.utils.locations import Location, all_locations_info_link

locations = Blueprint("locations", __name__)
logging.basicConfig(filename='std.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level="INFO")


class SearchConfig(BaseModel):
    budget: Optional[Tuple[int, int]] = [0, math.inf]
    date: Optional[str]
    categories: Optional[List[str]]
    tags: Optional[List[str]]


def get_locations_info() -> list:
    info = requests.get(all_locations_info_link)
    return info.json()


def _perdelta(start, times, delta):
    curr = start
    dates = []
    iteration = 0
    while iteration < times:
        dates.append(curr)
        curr += delta
        iteration += 1
    return dates


@locations.route("/all", methods=["GET"])
def get_all_locations():
    locations_mock = get_locations_info()
    return jsonify(locations_mock)


@locations.route("/get_by_params", methods=["POST"])
def get_locations_by_params():
    data = request.json
    try:
        cfg = SearchConfig(**data)
    except ValidationError as error:
        return str(error), 500

    available_locations = filter_locations(cfg)
    return jsonify(available_locations)


def filter_locations(cfg) -> List[dict]:
    locations_mock = get_locations_info()
    available_locations = [_filter_location(location, cfg) for location in locations_mock]
    return list(filter(None, available_locations))


def _filter_location(location: dict, cfg: SearchConfig) -> Optional[dict]:
    loc = Location(**location)

    if cfg.categories:
        categories_check = set(loc.categories).intersection(set(cfg.categories))
        if not categories_check:
            return

    if cfg.budget:
        budget_min = cfg.budget[0]
        budget_max = cfg.budget[1]
        loc.providers = [provider for provider in loc.providers if budget_min <= provider["price"] <= budget_max]
        if not loc.providers:
            return

    if cfg.tags:
        tags_check = set(loc.tags).intersection(set(cfg.tags))
        if not tags_check:
            return

    if cfg.date:
        request_date = datetime.strptime(cfg.date, "%Y-%m-%d")
        for provider in loc.providers:
            pdate = provider["date_available"]
            start_date = pdate["start_date"]
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            recurring = pdate["recurring"]
            available_dates = [fdate for fdate in _perdelta(start_date, 100, timedelta(days=recurring))]
            if request_date not in available_dates:
                return
    return loc.__dict__


@locations.route("/cities", methods=["GET"])
def get_all_cities():
    locations_mock = get_locations_info()
    available_locations = [location["location"]["address"] for location in locations_mock]
    city_list = list(filter(lambda city: city != "null", available_locations))
    unique_cities = {city.split(",", 1)[0] for city in city_list}
    return jsonify(list(unique_cities))
