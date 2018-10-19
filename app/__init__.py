from flask import Flask
from instance.config import DevelopmentConfig as dev_config

app = Flask(__name__)
app.config.from_object(dev_config)

from .views import *
