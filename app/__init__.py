from flask import Flask
from flask_bootstrap import Bootstrap
from flask_dropzone import Dropzone

bootstrap = Bootstrap()
dropzone = Dropzone()

def create_app():

    app = Flask(__name__, static_url_path='/model')
    app.config["SECRET_KEY"] = "a very safe secret key"
    app.config["DROPZONE_ALLOWED_FILE_CUSTOM"] = True
    app.config["DROPZONE_ALLOWED_FILE_TYPE"] = ".csv"
    bootstrap.init_app(app)
    dropzone.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app