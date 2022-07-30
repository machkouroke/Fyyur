from flask import Flask
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import inspect

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Base:
    def asdict(self) -> dict:
        """
        Return a dictionary representation of the model.
        """
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


class Show(db.Model, Base):
    __tablename__ = 'show'
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
    start_time = db.Column(db.DateTime, primary_key=True)
    venue = db.relationship('Venue', backref=db.backref('shows', lazy=True, cascade="save-update, merge, "
                                                                                    "delete, delete-orphan"))
    artist = db.relationship('Artist', backref=db.backref('shows', lazy=True, cascade="save-update, merge, "
                                                                                      "delete, delete-orphan"))


class Venue(db.Model, Base):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(1000))
    facebook_link = db.Column(db.String(500))
    website = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean)
    genres = db.Column(db.PickleType())
    seeking_description = db.Column(db.TEXT())

    def __repr__(self):
        return f'<Venue {self.id} {self.name}>'


class Artist(db.Model, Base):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.PickleType())
    image_link = db.Column(db.String(1000))
    facebook_link = db.Column(db.String(500))
    website = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.TEXT())

    def __repr__(self):
        return f'<Artist {self.id} {self.name}>'
