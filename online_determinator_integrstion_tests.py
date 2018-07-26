import os
import online_determinator
import unittest
import tempfile
import pymysql
import atexit


path = "settings.ini"
test_path = 'test_settings.ini'

DB_password = online_determinator.get_setting(path, 'Settings', 'DB_password')

user1_mail = online_determinator.get_setting(test_path, 'Users', 'user1_mail')
user2_mail = online_determinator.get_setting(test_path, 'Users', 'user2_mail')
user1_password = online_determinator.get_setting(test_path, 'Users', 'user1_password')
user2_password = online_determinator.get_setting(test_path, 'Users', 'user2_password')

db = pymysql.connect(host="127.0.0.1", port=3306, user="root", password=DB_password,\
                                       database="pony_color_db", charset="utf8")  # Connecting to DB when app started
cursor = db.cursor()


class online_determinator_test_case(unittest.TestCase):

    # Methods of this class:

    def signin(self, mail, password):
        return self.app.post('/api/signin?mail={MAIL}&password={PASSWORD}'.format(MAIL = mail, PASSWORD = password),    # It must be POST !!!
                             follow_redirects=True)

    def signout(self):
        return self.app.get('/api/signout', follow_redirects=True)

    def setUp(self):
        self.db_fd, online_determinator.app.config['DATABASE'] = tempfile.mkstemp()
        online_determinator.app.testing = True
        self.app = online_determinator.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(online_determinator.app.config['DATABASE'])

    # Tests go further:

    def test_empty_root(self):
        rv = self.app.get('/')
        assert b'The requested URL was not found on the server.' in rv.data

    def test_login_logout(self):
        rv = self.signout()
        assert b'Not authorised' in rv.data

        rv = self.signin(user1_mail, user1_password)
        print(rv.data)
        assert b'Signed in successfully' in rv.data
       
        rv = self.signout()
        assert b'Signed out successfully' in rv.data

        rv = self.signin('example@gmail.com', 'default')
        assert b'No such user in database' in rv.data

        rv = self.signin(user2_mail, user2_password)
        assert b'E-mail is not activated' in rv.data

        rv = self.signin(user1_mail, 'default')
        assert b'Wrong password' in rv.data

    def test_getting_color(self):
        rv = self.signin(user1_mail, user1_password)

        rv = self.app.get('/api/get_pony_by_color?color=053550')
        #print(rv.data.decode())
        self.assertEqual(rv._status_code, 200)

        rv = self.app.get('/api/get_pony_by_color?color=#')
        assert b'Invalid color code' in rv.data

        rv = self.signout()

    def test_resend(self):
        rv = self.app.get('/api/resend?mail={MAIL}'.format(MAIL = user2_mail))
        self.assertEqual(rv._status_code, 200)

        rv = self.app.get('/api/resend?mail={MAIL}'.format(MAIL = user1_mail))
        assert b'This account is already activated' in rv.data

        rv = self.app.get('/api/resend?mail={MAIL}'.format(MAIL = 'example@gmail.com'))
        assert b'No such user in database' in rv.data

    def test_verify(self):
        query = '''SELECT verification_code FROM users WHERE email="{MAIL}"'''.format(MAIL = "'%s'" % user2_mail)

        cursor.execute(query)
        results = cursor.fetchall()
        escaped_code = results[0][0]
        code = escaped_code[1: -1]

        rv = self.app.get('/api/verify?code={CODE}'.format(CODE = code))
        self.assertEqual(rv._status_code, 200)

        query = """UPDATE users 
                   SET active = 0, verification_code = "{CODE}"
                   WHERE email = "{MAIL}" """.format(CODE = escaped_code,\
                                                     MAIL = "'%s'" % user2_mail)     # Undoing changes
        cursor.execute(query)
        db.commit()

        code = code[1: -1]
        rv = self.app.get('/api/verify?code={CODE}'.format(CODE = code))
        assert b'Invalid verification code.' in rv.data

    def test_signup(self):
        rv = self.app.post('/api/signup?mail={MAIL}&password={PASSWORD}'.format(MAIL = user2_mail, PASSWORD = '1234'))
        assert b'Password must be at least 8 symbols long.' in rv.data

        rv = self.app.post('/api/signup?mail={MAIL}&password={PASSWORD}'.format(MAIL = 'BAZOONGAS', PASSWORD = '12345678'))
        assert b"Email doesn't match RFC 6531 standards." in rv.data

        rv = self.app.post('/api/signup?mail={MAIL}&password={PASSWORD}'.format(MAIL = user1_mail, PASSWORD = user1_password))
        assert b"E-mail is used" in rv.data

        rv = self.app.post('/api/signup?mail={MAIL}&password={PASSWORD}'.format(MAIL = user2_mail, PASSWORD = user2_password))
        assert b"E-mail is not activated. Check your mailbox for new activation code. It may be in spam folder." in rv.data

        rv = self.app.post('/api/signup?mail={MAIL}&password={PASSWORD}'.format(MAIL = 'example@gmail.com', PASSWORD = '12345678'))
        self.assertEqual(rv._status_code, 200)

        query = """DELETE FROM users WHERE email="{MAIL}" """.format(MAIL = "'example@gmail.com'")

        cursor.execute(query)
        db.commit()

    def test_pony_viewer(self):
        rv = self.signin(user1_mail, user1_password)

        rv = self.app.get('/api/get_all_ponies?page={PAGE}&ponies_per_page={PPP}'.format(PAGE = 2, PPP = 3))
        print(rv.data.decode())
        self.assertEqual(rv._status_code, 200)



        rv = self.signout()


pinkie_pie_data_dict = {'pony_id': 4, 'pony_name': "'Pinkie Pie'", 'body_part': {'body': [{'#F3B6CF': "'Амарантово-розовый'"}], 'hair': [{'#ED458B': "'Глубокий пурпурно-розовый'"}], 'eye': [{'#186F98': "'Небесно-синий'"}, {'#82D1F4': "'Светло-голубой'"}]}}

@atexit.register    # Closing DB connection when app shunting down
def teardown_db():
    if db is not None:
        db.close()
        print('DATABASE CLOSED')
