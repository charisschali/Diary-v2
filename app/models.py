import jwt,psycopg2
from app.create_database import createdb_con
from werkzeug.security import generate_password_hash,check_password_hash

conn = createdb_con()
cur = conn.cursor()

class BaseClass():
    """This class has methods for dropping tables
    and deleting table data
    """
    def clear_table(self):
        query = "TRUNCATE entries,users"
        cur.execute(query)
        conn.commit()

    def drop_tables(self):
        query = "DROP TABLE entries,users"
        cur.execute(query)
        conn.commit()

class User():
    """
    This model saves new user data into the database and provides
    methods for fetching user's data.
    """
    def save(self,user):
        """ saves user's details to database
        """
        cur.execute("insert into users (username,email,password) values(%s,%s,%s)",user)
        conn.commit()

    @classmethod
    def get_user_by_email(cls,email):
        """
        fetches user's details using email
        """
        try:
            cur.execute("select * from users where email = %s",(email,))
            fetch_data = cur.fetchone()
            return list(fetch_data)
        except Exception as e:
            return e

    @staticmethod
    def match_email(email):
        """
        matches user's email address that is stored
        to the databse
        """
        try:
            cur.execute("select email from users where email = %s",(email,))
            fetch_data = cur.fetchone()
            return list(fetch_data)[0]
        except Exception as e:
            return e


    def get_pwd_by_email(self,email):
        """
        gets user's password using email
        """
        try:
            cur.execute("select password from users where email = %s",(email,))
            fetch_data = cur.fetchone()
            return list(fetch_data)[0]
        except Exception as e:
            return e


    def get_id_by_email(self,email):
        cur.execute("select users.id from users where email = %s",(email,))
        user_id = cur.fetchone()
        return user_id

class Entry():
    """
    This class will store diary entries
    and also have methods that will manipulate
    those entries.
    """

    @staticmethod
    def get_by_id(entryId,user_id):
        """
        This method fetches user entry by its id
        """
        query="select entries.id,date,title,content from entries WHERE user_id={} and id={}".format(user_id,entryId)
        cur.execute(query)
        user_entries = cur.fetchall()
        return user_entries
        conn.close()

    def save(self,entry):
        """
        saves an entry to the database
        """
        cur.execute("insert into entries (user_id,date,title,content) values(%s,%s,%s,%s)",entry)
        conn.commit()
    @staticmethod
    def get_entry_id(entryId):
        """
        This method fetches entry id
        """
        query="select entries.id from entries WHERE entries.id={}".format(entryId)
        cur.execute(query)
        entry_id = cur.fetchone()
        return entry_id
        conn.close()


    def delete_entry(self,entryId):
        """
        deletes an entry
        """
        query = "DELETE FROM entries WHERE entries.id={}".format(entryId)
        cur.execute(query)
        conn.commit()

    def update_entry(self,new_entry,entryId):
        """
        updates a user an entry if it exists with new data
        """
        query = "UPDATE entries SET title = '{}',content= '{}'  WHERE entries.id = {}".format(new_entry[0],new_entry[1],entryId)
        cur.execute(query)
        conn.commit()

    @staticmethod
    def get_all_entries(user_id):
        """
        This method fetches entries of a user
        """
        query="select entries.id,date,title,content from  entries inner join users on  entries.user_id=users.id WHERE users.id={}".format(user_id)
        cur.execute(query)
        user_entries = cur.fetchall()
        return user_entries
        conn.close()

    @staticmethod
    def entry_date(entryId):
        """
        Returns the date when an entry was created
        """
        query="select date from entries WHERE id={} ".format(entryId)
        cur.execute(query)
        date = cur.fetchone()
        return date
