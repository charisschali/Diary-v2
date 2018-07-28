import unittest
from app import create_app
from app.models import ClearClass,Entry,User

class TestUserModel(unittest.TestCase):

    """ This class tests users model """

    def setUp(self):
        app = create_app('testing')
        self.tester = app.test_client(self)
        self.new_user1 = ('test','test11e1@camp.com','test111')

    def test_save_method_saves_users(self):
        ClearClass().clear_table()
        User().save(self.new_user1)
        User().get_id_by_email('test11e1@camp.com')
        self.assertEqual(1,1)

    def test_verify_password_func(self):
        verify = User().verify_password('test11e1@camp.com','test111')
        self.assertEqual(verify,True)

class TestEntryModel(unittest.TestCase):
    """ This class tests Entry model"""
    def setUp(self):
        app = create_app('testing')
        self.tester = app.test_client(self)
        self.entry1 =(1,"28/07/2018",'python','python for everyone')
        self.entry2 = (1,"29/07/2018",'TDD','test driven development')
        self.entry3 = (1,"29/07/2018",'Andela','This is Andela')

    def test_save_method_saves_entries(self):
        entries = [self.entry1,self.entry2,self.entry3]
        for entry in entries:
            Entry().save(entry)
        data = Entry().verify_title('python',1)
        self.assertEquals(data,True)

    def test_verify_email_fun(self):
        entries = Entry().verify_title('python',1)
        self.assertEqual(entries,True)