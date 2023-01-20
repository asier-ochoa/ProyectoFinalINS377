from flask import Blueprint, request, jsonify
from mariadb import IntegrityError

from tools import db_connect, EntityNotFoundException, DuplicatedEntityException
from configuration import config
from providers import AdProvider, get_content_types as db_content_types, search_tags as db_tags

provider_api_routes = Blueprint("provider_routes", __name__, url_prefix='/provider')


@provider_api_routes.errorhandler(DuplicatedEntityException)
def handle_duplicated_entity(e):
    return jsonify({"response": f"Error: {e}"}), 422


@provider_api_routes.errorhandler(EntityNotFoundException)
def handle_missing_entity(e):
    return jsonify({"response": f"Error: {e}"}), 404


@provider_api_routes.errorhandler(IntegrityError)
def handle_missing_entity(e):
    return jsonify({"response": "Error: Invalid entry in body"}), 422


@provider_api_routes.get('/content-type')
def get_content_types():
    with db_connect() as conn:
        return jsonify(db_content_types(conn.cursor())), 200


@provider_api_routes.get('/tag')
def search_tags():
    """
    Request Body:
    {
      "query": str
    }
    """
    body: dict = request.get_json(force=True)

    with db_connect() as conn:
        return jsonify(db_tags(body.get('query'), conn.cursor())), 200


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

    with db_connect() as conn:
        ad_provider.submit(conn.cursor())

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

    with db_connect() as conn:
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

    with db_connect() as conn:
        ad_provider = AdProvider.provider_factory_id(p_id, conn.cursor())  # Find provider using id
        ad_provider.create_ad(**body, provider_id=p_id, cursor=conn.cursor())

    return jsonify({"response": "OK"}), 200


@provider_api_routes.get("/ad/<p_id>/list-ads")
def list_ads(p_id):
    with db_connect() as conn:
        ad_provider = AdProvider.provider_factory_id(p_id, conn.cursor())
        return ad_provider.list_ads(conn.cursor())


@provider_api_routes.post("/ad/<p_id>/<ad_id>/edit-tags")
def edit_tags(p_id, ad_id):
    """
    Request body:
    {
      "action": str,
      "tags": [
        {
          "id": int,
          "relative_weight": int
        }
      ]
    }
    """
    action_fields = ("add", "delete")
    body: dict = request.get_json(force=True)
    if body['action'] not in action_fields:
        raise IntegrityError()

    with db_connect() as conn:
        cur = conn.cursor()
        ad_provider = AdProvider.provider_factory_id(p_id, cur)
        if body['action'] == "add":
            ad_provider.add_tags(ad_id, body['tags'], cur)
        else:
            ad_provider.delete_tags(ad_id, body['tags'], cur)

    return jsonify({"response": "OK"}), 200
