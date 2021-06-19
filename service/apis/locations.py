import json
import pathlib
from typing import List

from flask import Blueprint, jsonify, request
from pydantic import BaseModel, StrictStr, ValidationError

# from service.utils.locations import Location

locations = Blueprint("locations", __name__)
locations_filepath = pathlib.Path(__file__).parent.parent.joinpath("mocks").joinpath("locations.json")


class SearchConfig(BaseModel):
    budget: List[int]
    datetime: StrictStr



# class Provider(BaseModel):
class Provider():
    id: int
    name: str
    price: int
    datetime_available: List[str]
    duration: str
    rating: str

    def __init__(self, **entries):
        self.__dict__.update(entries)


# class Location(BaseModel):
class Location:
    id: int
    name: str
    alias: str
    categories: List[str]
    tags: List[str]
    image_src: str
    difficulty: int
    extra_params: List[dict]
    description: str
    latlng: str
    providers: List[Provider]


    def __init__(self, **entries):
        self.__dict__.update(entries)


def get_source_info() -> dict:
    with open(locations_filepath, "r", encoding="utf-8") as reader:
        return json.loads(reader.read())


@locations.route("/all", methods=["GET"])
def get_all_locations():
    locations_mock = get_source_info()
    return jsonify(locations_mock)


@locations.route("/get_by_params", methods=["POST"])
def get_locations_by_params():
    data = request.json
    try:
        cfg = SearchConfig(**data)
    except ValidationError as error:
        return str(error), 500

    budget_min = cfg.budget[0]
    budget_max = cfg.budget[1]
    locations_mock = get_source_info()
    available_locations = []
    for location in locations_mock:
        loc = Location(**location)
        loc.providers = [provider for provider in loc.providers if budget_min <= provider["price"] <= budget_max]
        available_locations.append(loc.__dict__)
    return jsonify(available_locations)
