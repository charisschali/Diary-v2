from app.create_database import createdb_con
from werkzeug.security import generate_password_hash,check_password_hash


conn = createdb_con()
cur = conn.cursor()

class ClearClass():
    """This class has methods for dropping tables
    and deleting table data
    """
    @staticmethod
    def clear_table():
        query = "TRUNCATE entries,users"
        cur.execute(query)
        conn.commit()

    @staticmethod
    def drop_tables():
        query = "DROP TABLE entries,users"
        cur.execute(query)
        conn.commit()
    @staticmethod
    def create_table():
        query = """ CREATE TABLE entries (
            id SERIAL ,
            user_id INTEGER NOT NULL,
            date VARCHAR(20),
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            PRIMARY KEY (user_id,id),
            FOREIGN KEY (user_id)
            REFERENCES users (id)

            )
                """
        query2 = """
            CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(225) NOT NULL
            )
            """
        cur.execute(query2)
        cur.execute(query)
        conn.commit()

class User():
    """
    This model saves new user data into the database and provides
    methods for fetching user's data.
    """
    @staticmethod
    # saves user's details to database
    def save(user):
        hash_pwd = generate_password_hash(user[2])
        cur.execute("insert into users (username,email,password) values(%s,%s,%s)",(user[0],user[1],hash_pwd))
        conn.commit()

    @staticmethod
    def verify_password(email,password):
        cur.execute("select password from users where email = %s",(email,))
        fetch_data = cur.fetchone()
        hashed_pwd = (fetch_data)[0]
        if check_password_hash(hashed_pwd,password):
            return True
        else:
            return False

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
            if fetch_data:
                return list(fetch_data)[0]
            else:
                return False
        except Exception as e:
            return e

    @staticmethod
    def get_pwd_by_email(email):
        """
        gets user's password using email
        """
        try:
            cur.execute("select password from users where email = %s",(email,))
            fetch_data = cur.fetchone()
            return list(fetch_data)[0]
        except Exception as e:
            return e

    @staticmethod
    def get_id_by_email(email):
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
        query = "select entries.id,date,title,content from entries WHERE user_id={} and id={}".format(user_id,entryId)
        cur.execute(query)
        user_entries = cur.fetchall()
        return user_entries

    @staticmethod
    def save(entry):
        """
        saves an entry to the database
        """
        cur.execute("insert into entries (user_id,date,title,content) values(%s,%s,%s,%s)",entry)
        conn.commit()
        query = "select entries.id,date,title,content from entries WHERE user_id = {} and title = '{}'".format(entry[0],entry[2])
        cur.execute(query)
        entry = cur.fetchone()
        return {'id':entry[0],"date":entry[1],"title":entry[2],"content":entry[3]}

    @staticmethod
    def get_entry_id(entryId):
        """
        This method fetches entry id
        """
        query = "select entries.id from entries WHERE entries.id={}".format(entryId)
        cur.execute(query)
        entry_id = cur.fetchone()
        return entry_id
        conn.close()

    @staticmethod
    def delete_entry(entryId):
        """
        deletes an entry
        """
        query = "DELETE FROM entries WHERE entries.id={}".format(entryId)
        cur.execute(query)
        conn.commit()

    @staticmethod
    def update_entry(new_entry,entryId):
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
        query = "select entries.id,date,title,content from  entries inner join users on  entries.user_id=users.id WHERE users.id={}".format(user_id)
        cur.execute(query)
        user_entries = cur.fetchall()
        return user_entries
        conn.close()

    @staticmethod
    def entry_date(entryId):
        """
        Returns the date when an entry was created
        """
        query = "select date from entries WHERE id={} ".format(entryId)
        cur.execute(query)
        date = cur.fetchone()
        return date

    @staticmethod
    def verify_title(title,user_id):
        query ="select entries.title from entries where user_id = {} and title = '{}' ".format(user_id,title)
        cur.execute(query)
        title = cur.fetchone()
        if title:
            return True
        return False
