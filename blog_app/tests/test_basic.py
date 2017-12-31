import base64
import unittest

from flask import json

from blog_app.app import app
from blog_app.database import db


class BasicTest(unittest.TestCase):
    TEST_USER = 'user'
    TEST_USER_EMAIL = 'foo@bar.com'
    TEST_USER_PASS = 'pass'

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/test'
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()
            self.register(self.TEST_USER,
                          self.TEST_USER_EMAIL,
                          self.TEST_USER_PASS,
                          self.TEST_USER_PASS)

        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    ########################
    #### helper methods ####
    ########################

    def get_auth_headers(self):
        return {
            'Authorization': 'Basic ' + base64.b64encode(
                bytes(self.TEST_USER + ":" + self.TEST_USER_PASS, 'ascii')).decode('ascii')
        }

    def register(self, username, email, password, confirm):
        return self.app.post(
            '/api/auth/register',
            data=json.dumps(dict(username=username, email=email, password=password, confirm=confirm)),
            content_type='application/json',
            follow_redirects=True
        )
