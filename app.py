from flask import Flask
from flask_restful import Api
from resources import (
    BusinessResource,
    BusinessListResource,
)

app = Flask(__name__)
api = Api(app)

api.add_resource(BusinessListResource, '/business')
api.add_resource(BusinessResource, '/business/<int:_id>')


if __name__ == '__main__':
    app.run(debug=True)
