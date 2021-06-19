from flask import Blueprint, request

hello = Blueprint("hello", __name__)


@hello.route("/hey", methods=["GET"])
def hello_user():
    return "Hello Steve!"
    # cfg = request.args
