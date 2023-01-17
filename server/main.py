from flask import Flask
from configuration import config
from api import api_routes

app = Flask(__name__)
app.register_blueprint(api_routes)

if __name__ == "__main__":
    app.run(port=config.server.port, debug=True)
