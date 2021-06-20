from typing import List

all_locations_info_link = "https://yourtrip.qbank.pro/public/data.php?type=all_objects"


class Provider:
    id: int
    name: str
    price: int
    date_available: List[str]
    duration: str
    rating: str

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __iter__(self):
        for key in self.__dict__:
            yield key, getattr(self, key)


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

