import unittest,json
from base import BaseClass

class Test_Entry_resources(BaseClass):

    get_entries= '/mydiary/v1/entries'
    add_entry = '/mydiary/v1/entries'
    get_single = '/mydiary/v1/entries/1'
    delete_entry  = '/mydiary/v1/entries/1'
    edit_entry = '/mydiary/v1/entries/1'

    """ This class tests the functionality of entries endpoint"""
    def SetUp(self):
        app = create_app('testing')
        self.tester = app.test_client(self)

    def test_adding_entry(self):
        ''' Testing if the Api can add an entry
        requested by a logged in user '''
        res = self.sing_in_user()
        token = json.loads(res.data.decode('utf-8'))['token']
        headers = {'Authorization': 'Bearer {}'.format(token)}

        res= self.tester.post(self.add_entry,headers=headers,
            data = json.dumps(self.data), content_type = 'application/json')
        res_msg = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res_msg["message"], "Entry added")

    def test_get_entries(self):
        ''' Testing if the Api can fetch all entries
        requested by a logged in user '''
        res = self.sing_in_user()
        token = json.loads(res.data.decode('utf-8'))['token']
        headers = {'Authorization': 'Bearer {}'.format(token)}
        res= self.tester.get(self.get_entries,headers=headers,
        content_type = 'application/json')
        self.assertEqual(res.status_code, 200)
        self.assertIn("All Entries", str(res.data))
        self.assertIn('Authorization', str(res.headers))

    def test_get_single_entry(self):
        ''' Testing if the Api can fetch a single
        requested by a logged in user '''
        res = self.sing_in_user()
        token = json.loads(res.data.decode('utf-8'))['token']
        headers = {'Authorization': 'Bearer {}'.format(token)}
        res= self.tester.get(self.get_single, headers=headers,
        content_type = 'application/json')
        self.assertEqual(res.status_code, 200)



    def test_update_entry(self):
        ''' Testing if the Api can update an entry
        requested by a logged in user '''
        res = self.sing_in_user()
        token = json.loads(res.data.decode('utf-8'))['token']
        headers = {'Authorization': 'Bearer {}'.format(token)}
        res= self.tester.put(self.edit_entry,headers=headers,
        content_type = 'application/json')
        self.assertEqual(res.status_code, 200)
        self.assertIn("Entry was updated", str(res.data))


    def test_delete_entry(self):
        ''' Testing if the Api can delete an entry
        requested by a logged in user '''
        res = self.sing_in_user()
        token = json.loads(res.data.decode('utf-8'))['token']
        headers = {'Authorization': 'Bearer {}'.format(token)}
        res= self.tester.delete(self.delete_entry,headers=headers,
        content_type = 'application/json')
        self.assertEqual(res.status_code, 200)
        self.assertIn("Entry deleted", str(res.data))
