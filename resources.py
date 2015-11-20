from flask.ext.restful import reqparse
from flask_restful import (
    Resource,
    abort,
    fields,
    marshal_with,
)
from storage import (
    Business,
    Review,
)


parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('text', type=str)
parser.add_argument('rating', type=int)
parser.add_argument('tags', location='json', type=list)
parser.add_argument('location', type=dict)
parser.add_argument('distance', type=int)

REVIEW_FIELDS = {
    'text': fields.String,
    'tags': fields.List(fields.String),
    'rating': fields.Integer,
    'created': fields.DateTime,
}

BUSINESS_FIELDS = {
    '_id': fields.Integer,
    'name': fields.String,
    'tags': fields.List(fields.String),
    'rating': fields.Float,
    'location': fields.Raw,
    'reviews': fields.List(fields.Nested(REVIEW_FIELDS)),
    'created': fields.DateTime
}
METERS_PER_MILE = 1609.34


def get_record_by_id(_id):
    record = Business.objects(_id=_id)
    if not record:
        abort(404, message="Business with id {} doesn't exist".format(_id))
    return record[0]


class BusinessResource(Resource):

    @marshal_with(BUSINESS_FIELDS)
    def get(self, _id):
        return get_record_by_id(_id)

    def delete(self, _id):
        get_record_by_id(_id)
        Business.objects(_id=_id).delete()
        return '', 204

    @marshal_with(BUSINESS_FIELDS)
    def put(self, _id):
        record = get_record_by_id(_id)
        args = parser.parse_args()
        name = args.get('name')
        location = args.get('location')
        if name is not None:
            record.name = name
        if location is not None and isinstance(location, dict):
            lat = location['lat']
            lon = location['lon']
            record.location = {
                "type": "Point",
                "coordinates": [lon, lat]
            }
        record.save()
        return record, 201


class BusinessListResource(Resource):

    @marshal_with(BUSINESS_FIELDS, envelope='data')
    def get(self):
        args = parser.parse_args()
        distance = args.get('distance')
        location = args.get('location')
        filter_kwargs = {}
        if distance is not None and location is not None:
            filter_kwargs = {
                'location__near': [location['lon'], location['lat']],
                'location__max_distance': distance * METERS_PER_MILE
            }
        records = Business.objects(**filter_kwargs)
        return list(records)

    @marshal_with(BUSINESS_FIELDS)
    def post(self):
        args = parser.parse_args()
        name = args.get('name')
        location = args.get('location')
        if name is None or location is None:
            abort(400, message='Bad request data')
        lat = location['lat']
        lon = location['lon']
        record = Business()
        record.name = name
        record.location = {
            "type": "Point",
            "coordinates": [lon, lat]
        }
        record.save()
        return record, 201


class BusinessReviewResource(Resource):

    @marshal_with(BUSINESS_FIELDS)
    def post(self, _id):
        record = get_record_by_id(_id)
        args = parser.parse_args()
        text = args.get('text')
        rating = args.get('rating')
        tags = args.get('tags')
        reviews_count = len(record.reviews)
        new_rating = round(
            ((record.rating or 0) * reviews_count + rating) /
            (reviews_count + 1),
            2
        )
        review = Review()
        review.text = text
        review.tags = tags
        review.rating = rating
        record.reviews.append(review)
        record.rating = new_rating
        record.tags = sorted(set(record.tags + tags))
        record.save()
        return record, 201
