from flask import Flask
from instance.config import DevelopmentConfig as dev_config
from flask_jsonrpc import JSONRPC
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config.from_object(dev_config)
# Настроим БД
app.config['SQL_ALCHEMY_DATABASE_URI'] = 'postgresql://{username}:{password}@{url}:{port}/{db_name}'\
    .format(username=dev_config.DB_USER, password=dev_config.DB_PASS, url=dev_config.DB_HOST,
            port=dev_config.DB_PORT, db_name=dev_config.DB_NAME)

db = SQLAlchemy(app)
jsonrpc = JSONRPC(app, '/api/')

from .views import *
