from flask import Flask
from instance.config import DevelopmentConfig as dev_config
from flask_jsonrpc import JSONRPC
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object(dev_config)

jsonrpc = JSONRPC(app, '/api/')

from .views import *
