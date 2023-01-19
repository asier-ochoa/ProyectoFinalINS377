from flask import Blueprint, request, jsonify
from tools import db_connect, DuplicatedEntityException, EntityNotFoundException
from configuration import config
from providers import AdProvider

api_routes = Blueprint("routes", __name__)


@api_routes.errorhandler(DuplicatedEntityException)
def handle_duplicated_entity(e):
    return jsonify({"response": f"Error: {e}"}), 422


@api_routes.errorhandler(EntityNotFoundException)
def handle_missing_entity(e):
    return jsonify({"response": f"Error: {e}"}), 404


@api_routes.get("/db_status")
def get_db_status():
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


@api_routes.get("/ad_provider/get")
def get_ad_provider():
    """
    Request Body:
    {
        "company_name": <str>
    }
    """
    body: dict = request.get_json(force=True)

    conn = db_connect()
    ret = AdProvider(**body, email="").get_provider(conn.cursor())
    if ret is None:
        raise EntityNotFoundException("Company with name {body['company_name']} could not be found!")

    return ret, 200


@api_routes.post("/ad_provider/<p_id>/create_ad")
def post_ad(p_id):
    """
    Request Body:
    """
    body: dict = request.get_json(force=True)

    conn = db_connect()
    ad_provider = AdProvider.provider_factory_id(p_id, conn.cursor())  # Find provider using id
    ad_provider.create_ad(**body, cursor=conn.cursor())

    return jsonify({"response": "OK"}), 200
