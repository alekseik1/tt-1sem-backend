from flask import Flask
from instance.config import DevelopmentConfig as dev_config
from flask_jsonrpc import JSONRPC

app = Flask(__name__)
app.config.from_object(dev_config)

jsonrpc = JSONRPC(app, '/api/')

from .views import *
