import os
from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL

mysql = MySQL()

# Create the Flask app

def create_app():
    app = Flask(__name__, template_folder='web', static_folder='web/static')
    app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
    app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    CORS(app, resources=r'/*')
    app.config.from_object('myapp.config')
    app.secret_key = os.environ.get('SECRET_KEY')
    
    mysql.init_app(app)
    register_blueprints(app)
    return app

def register_blueprints(app: Flask):
    from . import auth, main
    app.register_blueprint(auth.routes.blueprint)
