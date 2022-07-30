import os
from flask import Flask
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import ImmutableMultiDict

"""Constants"""
TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
HOME_PAGE = 'pages/home.html'

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


SQLALCHEMY_DATABASE_URI = 'postgresql://machk:claudine@localhost:5432/lopfyyur'
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)


def multidict_to_dict(data: ImmutableMultiDict) -> dict:
    return {field: data.getlist(field) if field == "genres" else data.get(field, None) for
            field in data.keys()}
