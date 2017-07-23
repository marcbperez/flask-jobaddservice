from ..database import db
from ..database.model import Model
from werkzeug.security import gen_salt
from datetime import datetime


class Job(db.Model, Model):
    """Job add REST model."""

    __tablename__ = 'job'

    provider = db.Column(db.String(200))
    link = db.Column(db.String(200))
    author = db.Column(db.String(200))
    location = db.Column(db.String(200))
    title = db.Column(db.String(200))
    description = db.Column(db.String(10000))

    def serialize(self):
        """Returns the serialized version of this model."""
        serialized = Model.serialize(self)
        serialized['provider'] = self.provider
        serialized['link'] = self.link
        serialized['author'] = self.author
        serialized['location'] = self.location
        serialized['title'] = self.title
        serialized['description'] = self.description

        return serialized

    @classmethod
    def add_parser_args(cls, parser):
        """Adds model parameters to parser validation."""
        parser.add_argument(
            'public', required=True, help='Job add visibility.')
        parser.add_argument(
            'provider', required=True, help='Job add provider.')
        parser.add_argument('link', required=True, help='Job add link.')
        parser.add_argument('author', required=True, help='Job add author.')
        parser.add_argument(
            'location', required=True, help='Job add location.')
        parser.add_argument('title', required=True, help='Job add title.')
        parser.add_argument(
            'description', required=True, help='Job add description.')

    @classmethod
    def update(cls, model, etag, public, updated, created, provider, link,
               author, location, title, description):
        """Updates a model if the etag matches."""
        if model.etag != etag:
            return False

        model.etag = gen_salt(40)
        model.public = public == '1'
        model.updated = updated
        model.created = created
        model.provider = provider
        model.link = link
        model.author = author
        model.location = location
        model.title = title
        model.description = description

        db.session.commit()

        return model

    @classmethod
    def create(cls, user, public, updated, created, provider, link,
               author, location, title, description):
        """Creates a model owned by the provided user."""
        model = cls()
        model.user_id = user.id if user else 0
        model.etag = gen_salt(40)
        model.public = public == '1'
        model.updated = updated
        model.created = created
        model.provider = provider
        model.link = link
        model.author = author
        model.location = location
        model.title = title
        model.description = description

        db.session.add(model)
        db.session.commit()

        return model
