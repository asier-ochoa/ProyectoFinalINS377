from flask import Flask
from configuration import config
from provider_api import provider_api_routes
from server.admin_api import admin_api_routes
from server.tools import EntityNotFoundException, DuplicatedEntityException

app = Flask(__name__)
app.register_blueprint(provider_api_routes)
app.register_blueprint(admin_api_routes)


if __name__ == "__main__":
    app.run(port=config.server.port)
