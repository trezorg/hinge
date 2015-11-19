import unittest
import json
from mongoengine import connect
from storage import (
    MONGODB_URL,
    MONGODB_DATABASE,
)
from app import app


HEADERS = [('Content-Type', 'application/json')]
TEST_BUSINESS_DATA = {
    'name': 'test',
    'location': {
        'lat': 53.10682735591432,
        'lon': -114.11773681640625
    }
}
TEST_REVIEW_DATA = {
    'text': 'test',
    'rating': 3,
    'tags': ['foo', 'bar']
}
TEST_SEARCH_DATA = {
    'distance': 2,
    'location': {
        'lat': 53.10682735591432,
        'lon': -114.11773681640625
    }
}
TEST_WRONG_SEARCH_DATA = {
    'distance': 2,
    'location': {
        'lat': 13.10682735591432,
        'lon': -114.11773681640625
    }
}


class BusinessTest(unittest.TestCase):

    def setUp(self):
        db = connect(host=MONGODB_URL)
        db.drop_database(MONGODB_DATABASE)
        self.app = app.test_client()
        self.app.testing = True

    @classmethod
    def tearDownClass(cls):
        super(cls, BusinessTest).tearDownClass()
        db = connect(host=MONGODB_URL)
        db.drop_database(MONGODB_DATABASE)

    def test_create_business_item(self):
        result = self.app.post(
            '/business', headers=HEADERS, data=json.dumps(TEST_BUSINESS_DATA)
        )
        item = json.loads(result.data)
        self.assertEqual(result.status_code, 201)
        self.assertEqual(item['name'], 'test')
        self.assertEqual(item['rating'], None)
        self.assertEqual(item['reviews'], [])
        return item

    def test_get_business_items(self):
        self.test_create_business_item()
        result = self.app.get('/business')
        self.assertEqual(result.status_code, 200)
        payload = json.loads(result.data)
        self.assertIn('data', payload)
        item = payload['data'][0]
        self.assertEqual(item['name'], 'test')
        self.assertEqual(item['rating'], None)
        self.assertEqual(item['reviews'], [])

    def test_get_business_items_by_distance(self):
        self.test_create_business_item()
        result = self.app.get(
            '/business',
            headers=HEADERS,
            data=json.dumps(TEST_SEARCH_DATA)
        )
        self.assertEqual(result.status_code, 200)
        payload = json.loads(result.data)
        self.assertIn('data', payload)
        self.assertEqual(len(payload['data']), 1)

    def test_get_business_items_by_long_distance(self):
        self.test_create_business_item()
        result = self.app.get(
            '/business',
            headers=HEADERS,
            data=json.dumps(TEST_WRONG_SEARCH_DATA)
        )
        self.assertEqual(result.status_code, 200)
        payload = json.loads(result.data)
        self.assertIn('data', payload)
        self.assertEqual(len(payload['data']), 0)

    def test_get_business_item_by_id(self):
        item = self.test_create_business_item()
        result = self.app.get('/business/{}'.format(item['_id']))
        self.assertEqual(result.status_code, 200)
        item = json.loads(result.data)
        self.assertEqual(item['name'], 'test')
        self.assertEqual(item['rating'], None)
        self.assertEqual(item['reviews'], [])

    def test_update_business_item_by_id(self):
        item = self.test_create_business_item()
        result = self.app.put(
            '/business/{}'.format(item['_id']),
            headers=HEADERS,
            data=json.dumps({'name': 'new_name'})
        )
        self.assertEqual(result.status_code, 201)
        item = json.loads(result.data)
        self.assertEqual(item['name'], 'new_name')


class BusinessReviewTest(unittest.TestCase):

    def setUp(self):
        db = connect(host=MONGODB_URL)
        db.drop_database(MONGODB_DATABASE)
        self.app = app.test_client()
        self.app.testing = True

    @classmethod
    def tearDownClass(cls):
        super(cls, BusinessReviewTest).tearDownClass()
        db = connect(host=MONGODB_URL)
        db.drop_database(MONGODB_DATABASE)

    def test_add_business_review(self):
        result1 = self.app.post(
            '/business', headers=HEADERS, data=json.dumps(TEST_BUSINESS_DATA)
        )
        self.assertEqual(result1.status_code, 201)
        item = json.loads(result1.data)
        item_id = item['_id']
        result2 = self.app.post(
            '/business/{}/review'.format(item_id),
            headers=HEADERS,
            data=json.dumps(TEST_REVIEW_DATA)
        )
        self.assertEqual(result2.status_code, 201)
        item = json.loads(result2.data)
        self.assertEqual(item['name'], 'test')
        self.assertEqual(item['rating'], 3)
        self.assertEqual(len(item['reviews']), 1)
        self.assertEqual(item['reviews'][0]['text'], 'test')
        self.assertEqual(item['reviews'][0]['tags'], ['foo', 'bar'])


if __name__ == '__main__':
    unittest.main()
