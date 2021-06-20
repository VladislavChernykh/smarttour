from flask import Flask

from service.apis.locations import locations
from service.apis.users import users
from service.apis.categories import categories
from service.apis.trips import trips

api_prefix = "/api"
docs_folder = "openapi"
docs_path = f"{api_prefix}/{docs_folder}"

app = Flask(__name__, static_folder=docs_folder, static_url_path=docs_path)

blueprints_to_add = [
    locations, users, categories, trips
]
for blueprint in blueprints_to_add:
    url_prefix = f"{api_prefix}/{blueprint.name}"
    app.register_blueprint(blueprint, url_prefix=url_prefix)

if __name__ == "__main__":
    app.run(debug=True, port=80, host="localhost")
