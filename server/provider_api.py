from flask import Blueprint, request, jsonify
from tools import db_connect, EntityNotFoundException, DuplicatedEntityException
from configuration import config
from providers import AdProvider, get_content_types as db_content_types

provider_api_routes = Blueprint("provider_routes", __name__, url_prefix='/provider')


@provider_api_routes.errorhandler(DuplicatedEntityException)
def handle_duplicated_entity(e):
    return jsonify({"response": f"Error: {e}"}), 422


@provider_api_routes.errorhandler(EntityNotFoundException)
def handle_missing_entity(e):
    return jsonify({"response": f"Error: {e}"}), 404


@provider_api_routes.get('/content-type')
def get_content_types():
    conn = db_connect()
    return jsonify(db_content_types(conn.cursor())), 200


@provider_api_routes.post("/ad/create")
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


@provider_api_routes.get("/ad/get")
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

    return jsonify(ret), 200


@provider_api_routes.post("/ad/<p_id>/create-ad")
def post_ad(p_id):
    """
    Request Body:
    {
        "name": str,
        "ad_type": int,
        "content_route": str,
        "redirect_url": str
    }
    """
    body: dict = request.get_json(force=True)

    conn = db_connect()
    ad_provider = AdProvider.provider_factory_id(p_id, conn.cursor())  # Find provider using id
    ad_provider.create_ad(**body, provider_id=p_id, cursor=conn.cursor())
    conn.commit()

    return jsonify({"response": "OK"}), 200
