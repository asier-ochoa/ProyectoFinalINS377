from flask import Blueprint, request, jsonify
from mariadb import IntegrityError

from admin import *
from tools import db_connect

admin_api_routes = Blueprint("admin_routes", __name__, url_prefix='/admin')


@admin_api_routes.errorhandler(IntegrityError)
def handle_missing_entity(e):
    return jsonify({"response": "Error: Invalid entry in body"}), 422


@admin_api_routes.post('/content-type/create')
def post_content_type():
    """
    Request Body:
    {
        content_type: <str>
    }
    """
    body: dict = request.get_json(force=True)

    with db_connect() as conn:
        create_content_type(**body, cursor=conn.cursor())

    return jsonify({"response": "OK"}), 200


@admin_api_routes.post('/tag/create')
def post_tag():
    """
    Request Body:
    {
        name: str,
        description: str
    }
    """
    body: dict = request.get_json(force=True)

    with db_connect() as conn:
        create_category_tag(**body, cursor=conn.cursor())

    return jsonify({"response": "OK"}), 200
