import logging
import sys

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_oauthlib.provider import OAuth2Provider
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

from app.models import *

oauth_provider = OAuth2Provider(app)

oauth_logger = logging.getLogger('oauthlib')
oauth_logger.addHandler(logging.StreamHandler(sys.stdout))
oauth_logger.setLevel(logging.DEBUG)

for x in ['DEFAULT_DATABASE', 'OAUTH_DATABASE']:
    db.create_all(bind=app.config[x])

from flask_restful import Api

api_root = Api(app)

from app.routes import *
from app.api import *
