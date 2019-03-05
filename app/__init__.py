from flask import Flask
from instance.config import DevelopmentConfig as dev_config
from flask_jsonrpc import JSONRPC
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
CORS(app)
app.config.from_object(dev_config)
# Настроим БД
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{username}:{password}@{url}:{port}/{db_name}'\
    .format(username=dev_config.DB_USER, password=dev_config.DB_PASS, url=dev_config.DB_HOST,
            port=dev_config.DB_PORT, db_name=dev_config.DB_NAME)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jsonrpc = JSONRPC(app, '/api/')
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from .views import *
