from flask import Flask
from instance.config import DevelopmentConfig as dev_config
from flask_jsonrpc import JSONRPC
from flask_cors import CORS
from werkzeug.contrib.profiler import ProfilerMiddleware
import sys

app = Flask(__name__)
CORS(app)
app.config.from_object(dev_config)
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])

jsonrpc = JSONRPC(app, '/api/')

from .views import *
