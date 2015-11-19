import os
from datetime import datetime
from mongoengine import (
    connect,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    DateTimeField,
    StringField,
    ListField,
    PointField,
    IntField,
    FloatField,
    SequenceField,
)

MONGODB_URL = os.environ.get('MONGODB_URL')
MONGODB_DATABASE = os.environ.get('MONGODB_DATABASE') or 'hinge'
if not MONGODB_URL:
    MONGODB_URL = "mongodb://localhost:27017/{}".format(MONGODB_DATABASE)

connect(host=MONGODB_URL)


class Review(EmbeddedDocument):
    text = StringField(required=True)
    created = DateTimeField(default=datetime.now)
    rating = IntField(required=True, min_value=1, max_value=5)
    tags = ListField(StringField(), required=True)


class Business(Document):
    _id = SequenceField(required=True)
    name = StringField(max_length=200, required=True)
    created = DateTimeField(default=datetime.now)
    tags = ListField(StringField(), default=list)
    rating = FloatField(min_value=1, max_value=5, default=None)
    location = PointField(required=True)
    reviews = ListField(EmbeddedDocumentField(Review), default=list)


