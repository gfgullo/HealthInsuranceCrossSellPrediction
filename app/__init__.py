from flask import Flask
from flask_bootstrap import Bootstrap


bootstrap = Bootstrap()

def create_app():

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "a very safe secret key"
    bootstrap.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app