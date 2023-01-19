from flask import Blueprint, request, jsonify
from tools import db_connect, DuplicatedEntityException
from configuration import config
from providers import AdProvider

api_routes = Blueprint("routes", __name__)


@api_routes.errorhandler(DuplicatedEntityException)
def handle_duplicated_entity(e):
    return jsonify({"response": f"Error: {e}"}), 422


@api_routes.get("/db_status")
def get_db_status():
    db_conf = config.mariadb
    db_conn = db_connect()
    return db_conn.server_info, 200


@api_routes.post("/ad_provider/create")
def post_ad_provider():
    """
    Request Body:
    {
        "company_name": <str>,
        "email": <str>
    }
    """
    body: dict = request.get_json(force=True)
    ad_provider = AdProvider(**body)

    conn = db_connect()
    ad_provider.submit(conn.cursor())
    conn.commit()

    return jsonify({"response": "OK"}), 200
