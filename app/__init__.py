from flask import Flask
from instance.config import TestingConfig as config
from flask_jsonrpc import JSONRPC
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
CORS(app)
app.config.from_object(config)
# Настроим БД
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{username}:{password}@{url}:{port}/{db_name}'\
    .format(username=config.DB_USER, password=config.DB_PASS, url=config.DB_HOST,
            port=config.DB_PORT, db_name=config.DB_NAME)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jsonrpc = JSONRPC(app, '/api/')
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from .views import *
