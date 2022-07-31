from config import db

from sqlalchemy import inspect


class Utilities:
    """
    Utilities function for All Model
    """
    def asdict(self) -> dict:
        """
        Return a dictionary representation of the model.
        The dictionary contains all the attributes of the model
        """
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


class Base(db.Model, Utilities):
    """
    Base class for Venue and Artist
    """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image_link = db.Column(db.String(1000))
    facebook_link = db.Column(db.String(500))
    website = db.Column(db.String(500))
    phone = db.Column(db.String(120))
    genres = db.Column(db.PickleType())
    seeking_description = db.Column(db.TEXT())


class Show(Utilities, db.Model):
    __tablename__ = 'show'
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
    start_time = db.Column(db.DateTime, primary_key=True)
    venue = db.relationship('Venue', backref=db.backref('shows', lazy=True, cascade="save-update, merge, "
                                                                                    "delete, delete-orphan"))
    artist = db.relationship('Artist', backref=db.backref('shows', lazy=True, cascade="save-update, merge, "
                                                                                      "delete, delete-orphan"))


class Venue(Base):
    __tablename__ = 'Venue'
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Venue {self.id} {self.name}>'


class Artist(Base):
    __tablename__ = 'Artist'

    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Artist {self.id} {self.name}>'
