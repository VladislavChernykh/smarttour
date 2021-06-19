import logging
from datetime import date, timedelta, datetime
import math
import pathlib
from typing import List, Optional

import requests
from flask import Blueprint, jsonify, request
from pydantic import BaseModel, ValidationError

from service.utils.locations import Location

all_locations_info_link = "https://yourtrip.qbank.pro/public/data.php?type=all_objects"
locations = Blueprint("locations", __name__)
locations_filepath = pathlib.Path(__file__).parent.parent.joinpath("mocks").joinpath("locations.json")
logging.basicConfig(filename='std.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level="INFO")

class SearchConfig(BaseModel):
    budget: Optional[List[int]] = [0, math.inf]
    date: Optional[str]
    categories: Optional[List[str]]
    tags: Optional[List[str]]


# class Provider:
#     id: int
#     name: str
#     price: int
#     date_available: List[str]
#     duration: str
#     rating: str
#
#     def __init__(self, **entries):
#         self.__dict__.update(entries)
#
#
# class Location:
#     id: int
#     name: str
#     alias: str
#     categories: List[str]
#     tags: List[str]
#     image_src: str
#     difficulty: int
#     extra_params: List[dict]
#     description: str
#     latlng: str
#     providers: List[Provider]
#
#     def __init__(self, **entries):
#         self.__dict__.update(entries)


def get_locations_info() -> list:
    info = requests.get(all_locations_info_link)
    return info.json()
    # with open(locations_filepath, "r", encoding="utf-8") as reader:
    #     return json.loads(reader.read())

def perdelta(start, times, delta):
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

    locations_mock = get_locations_info()
    # available_locations = [location for location in locations_mock if filter_location(location, cfg)]
    available_locations = [filter_location(location, cfg) for location in locations_mock]
    available_locations = list(filter(None, available_locations))
    return jsonify(available_locations)


def filter_location(location: dict, cfg: SearchConfig) -> Optional[dict]:
    loc = Location(**location)

    if cfg.categories:
        # categories_check = any(x in loc.categories for x in cfg.categories)
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
            available_dates = [fdate for fdate in perdelta(start_date, 100, timedelta(days=recurring))]
            if request_date not in available_dates:
                return
    return loc.__dict__
