import unittest,json
from app import create_app
from app.models import ClearClass

class Test_Auth_Endpoints(unittest.TestCase):

    """ This class tests /auth/login and /auth/register endpoints"""

    def setUp(self):
        app = create_app('testing')
        self.tester = app.test_client(self)
        self.singup_url ='/mydiary/v1/auth/register'
        self.singin_url ='/mydiary/v1/auth/login'
        self.new_user = {"username":'test',
                'email':'test11e1@camp.com',
                'password':'test111',
                'confirm_password':'test111'}
        self.new_user2 = {"username":'test',
            'email':'test1@camp.com',
            'password':'test',
            'confirm_password':'test1'}
        self.missing_email= {'password':'test'}
        self.missing_pwd= {'email':'test11e1@camp.com'}

        self.user = {
            'email':'test11e1@camp.com',
            'password':'test111',
            }
        self.user2 = {
            'email':'test11e1@camp.com',
            'password':'tes',
            }
        self.user3 = {
            'email':'chariss@camp.com',
            'password':'test',
            }
    def tearDown(self):
        ClearClass().clear_table()

# Test sing_up endpoint
    def test_singup_endpoint(self):
        response = self.tester.post(self.singup_url,data=json.dumps(self.new_user),
        content_type="application/json")
        self.assertEquals(response.status_code,201)

# Tests for password mismatch
    def test_singup_with_unmatched_password(self):
        response = self.tester.post(self.singup_url,data=json.dumps(self.new_user2),
        content_type="application/json")
        self.assertEquals(response.status_code,400)

# Test sing up with existing email
    def test_singup_with_existing_email(self):
        self.tester.post(self.singup_url,data=json.dumps(self.new_user),
        content_type="application/json")
        response = self.tester.post(self.singup_url,data=json.dumps(self.new_user),
        content_type="application/json")
        self.assertEquals(response.status_code,400)

# Test sing_in endpoint
    def test_singin_endpoint(self):
        self.tester.post(self.singup_url,data=json.dumps(self.new_user),
        content_type="application/json")
        response = self.tester.post(self.singin_url,data=json.dumps(self.user),
        content_type="application/json")
        self.assertEquals(response.status_code,200)
        res = json.loads(response.data.decode('utf8'))
        self.assertIn("token",str(res))

#password don't match
    def test_sing_with_incorrect_password(self):
        self.tester.post(self.singup_url,data=json.dumps(self.new_user),
        content_type="application/json")
        response = self.tester.post(self.singin_url,data=json.dumps(self.user2),
        content_type="application/json")
        res = json.loads(response.data.decode('utf8'))
        self.assertIn("{'Server Response': 'Your password was Incorrect, please double check it.'}",str(res))

#sign in with  unregisted email
    def test_singin_with_unexisting_email(self):
        self.tester.post(self.singup_url,data=json.dumps(self.new_user),
        content_type="application/json")
        response = self.tester.post(self.singin_url,data=json.dumps(self.user3),
        content_type="application/json")
        self.assertEquals(response.status_code,400)

#sign in with  missing email email
    def test_singin_with_without_email(self):
        response = self.tester.post(self.singin_url,data=json.dumps(self.missing_email),
        content_type="application/json")
        self.assertEquals(response.status_code,400)

#sign in with  missing password email
    def test_singin_with_without_password(self):
        response = self.tester.post(self.singin_url,data=json.dumps(self.missing_pwd),
        content_type="application/json")
        self.assertEquals(response.status_code,400)
