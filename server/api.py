from flask import Blueprint
from mariadb import connect
from configuration import config

api_routes = Blueprint("routes", __name__)


@api_routes.get("/db_status")
def get_db_status():
    db_conf = config.mariadb
    db_conn = connect(host=db_conf.host, port=db_conf.port, user=db_conf.user, passwd=db_conf.password, db=db_conf.database)
    return db_conn.server_info, 200
