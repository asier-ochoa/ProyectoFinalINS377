from flask import Blueprint, request, jsonify
from admin import create_content_type
from tools import db_connect

admin_api_routes = Blueprint("admin_routes", __name__, url_prefix='/admin')


@admin_api_routes.post('/content-type/create')
def post_content_type():
    """
    Request Body:
    {
        content_type: <str>
    }
    """
    body: dict = request.get_json(force=True)

    conn = db_connect()
    create_content_type(**body, cursor=conn.cursor())
    conn.commit()
    return jsonify({"response": "OK"}), 200