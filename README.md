hinge-api-interview-ironwood
=============================

Test task for hinge vacancy

Install
-------

Install by cloning from the GitHub repo:

    $ git clone git://github.com/trezorg/hinge.git
    $ cd hinge
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ python app.py


Testing
--------

    $ MONGODB_DATABASE=hingetest nosetests

    or

    $ MONGODB_URL='mongodb://localhost:27017/hingetest' nosetests


Create business item
----------------------

    curl -X POST -H "Content-Type: application/json" \
        http://127.0.0.1:5000/business \
        -d '{"name": "test", "location": {"lat":53.10682735591432, "lon":-114.11773681640625}}'


Get business item
----------------------

    curl -X GET -H "Content-Type: application/json" \
        http://127.0.0.1:5000/business/:id


Update business item
----------------------

    curl -X PUT -H "Content-Type: application/json" \
        http://127.0.0.1:5000/business/:id \
        -d '{"name": "test2", "location": {"lat":53.10682735591432, "lon":-114.11773681640625}}'

Get business items
----------------------

    curl -X GET http://127.0.0.1:5000/business


Search business items by point distance
------------------------------------------

    curl -X GET -H "Content-Type: application/json" \
        http://127.0.0.1:5000/business \
        -d '{"distance": 2, "location": {"lat":53.10682735591432, "lon":-114.11773681640625}}'


Add business review
--------------------

    curl -X POST -H "Content-Type: application/json" \
        http://127.0.0.1:5000/business/:id/review \
        -d '{"text": "text", "tags": ["test1", "test2"], "rating": 4}'
