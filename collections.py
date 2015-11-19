import os
from datetime import datetime
from mongoengine import (
    connect,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    StringField,
    DateTimeField,
    LineStringField,
    ListField,
    GeoPointField,
    IntField,
    FloatField,
    SequenceField,
)

MONGODB_URL = os.environ.get('MONGODB_URL')
if not MONGODB_URL:
    MONGODB_URL = "mongodb://localhost:27017/hinge"

connect(host=MONGODB_URL)


class Review(EmbeddedDocument):
    text = StringField(required=True)
    created = DateTimeField(default=datetime.now)
    rating = IntField(required=True, min_value=1, max_value=5)
    tags = LineStringField(required=True)


class Business(Document):
    id = SequenceField(required=True)
    name = StringField(max_length=200, required=True)
    created = DateTimeField(default=datetime.now)
    tags = LineStringField(required=True)
    rating = FloatField(required=True, min_value=1, max_value=5)
    location = GeoPointField(required=True)
    reviews = ListField(EmbeddedDocumentField(Review))


