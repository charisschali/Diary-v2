import unittest,json

class Test_Auth_Endpoints(unittest.TestCase):

    """ This class tests /auth/login and /auth/register endpoints"""

    def setUp(self):
        app = create_app('testing')
        self.tester = app.test_client(self)
        self.singup_url ='/mydiary/v1/auth/login'
        self.singin_url ='/mydiary/v1/auth/register'
        self.new_user = {"username":'test',
                'email':'test@camp.com',
                'password':'test',
                'confirm_password':'test'}
        self.new_user2 = {"username":'test',
            'email':'test1@camp.com',
            'password':'test',
            'confirm_password':'test1'}
        self.new_user3 = {"username":'test',
            'email':'test@camp.com',
            'password':'test',
            'confirm_password':'test1'}

        self.user = {
            'email':'test@camp.com',
            'password':'test',
            }
        self.user2 = {
            'email':'test@camp.com',
            'password':'tes',
            }


# Test sing_up endpoint
    def test_singup_endpoint(self):
        response = self.tester.post(self.singup_url,data=json.dumps(self.new_user),
        content_type="application/json")
        self.assertEquals(response.status_code,201)
        res = json.loads(response.data.decode('utf8'))
        self.assertIn("Account created",str(res))

    def test_singup_with_unmatched_password(self):
#Tests for password mismatch
        response = self.tester.post(self.singup_url,data=json.dumps(self.new_user2),
        content_type="application/json")
        self.assertEquals(response.status_code,400)

# Test sing up with existing email
    def test_singup_with_existing_email(self):
        response = self.tester.post(self.singup_url,data=json.dumps(self.new_user),
        content_type="application/json")
        self.assertEquals(response.status_code,400)


# Test sing_in endpoint
    def test_singin_endpoint(self):
        response = self.tester.post(self.singin_url,data=json.dumps(self.user),
        content_type="application/json")
        self.assertEquals(response.status_code,200)
        res = json.loads(response.data.decode('utf8'))
        self.assertIn("token",str(res))
#password don't match
    def test_sing_with_incorrect_password(self):
        response = self.tester.post(self.singin_url,data=json.dumps(self.user2),
        content_type="application/json")
        res = json.loads(response.data.decode('utf8'))
        self.assertIn("password is incorrect",str(res))
#sign in with  unregisted email
def test_singin_with_unexisting_email(self):
        response = self.tester.post(self.singin_url,data=json.dumps(self.user2),
        content_type="application/json")
        res = json.loads(response.data.decode('utf8'))
        self.assertIn("password is incorrect",str(res))
        res = json.loads(response.data.decode('utf8'))
        self.assertEquals(response.status_code,400)



