from flask import Flask
from flask_bootstrap import Bootstrap
from flask_dropzone import Dropzone
from flask_session import Session

bootstrap = Bootstrap()
dropzone = Dropzone()
session = Session()

def create_app():

    app = Flask(__name__)
    app.secret_key = "a very safe secret key"
    app.config["SECRET_KEY"] = app.secret_key
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config["DROPZONE_ALLOWED_FILE_CUSTOM"] = True
    app.config["DROPZONE_ALLOWED_FILE_TYPE"] = ".csv"
    
    bootstrap.init_app(app)
    dropzone.init_app(app)
    session.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
