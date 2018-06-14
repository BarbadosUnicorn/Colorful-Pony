import os
import online_determinator
import unittest
import tempfile


def signin(self, username, password):
    return self.app.post('/api/signin', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def signout(self):
    return self.app.get('/api/signout', follow_redirects=True)


class online_determinator_test_case(unittest.TestCase):

    def setUp(self):
        self.db_fd, online_determinator.app.config['DATABASE'] = tempfile.mkstemp()
        online_determinator.app.testing = True
        self.app = online_determinator.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(online_determinator.app.config['DATABASE'])

    def test_empty_root(self):
        rv = self.app.get('/')
        assert b'The requested URL was not found on the server.' in rv.data

########################################################################################################################
#                                    Changes must be applied further                                                   #
########################################################################################################################

    def test_login_logout(self):

        rv = self.signin('xtraand0ne@gmail.com', '12345678')
        assert b'Signed in successfully' in rv.data

        rv = self.signout()
        assert b'You were logged out' in rv.data

        rv = self.signin('adminx', 'default')
        assert b'No such user in database' in rv.data

        #rv = self.signin('adminx404', 'default')
        #assert b'E-mail is not activated' in rv.data

        rv = self.signin('xtraand0ne@gmail.com', 'default')
        assert b'Wrong password' in rv.data


    def test_getting_color(self):    # You need to login at first

        rv = self.app.get('/api/get_pony_by_color?color=053550')
        self.assertEqual(rv._status_code, 200)


    def test_invalid_color_code(self):    # You need to login at first

        rv = self.app.get('/api/get_pony_by_color?color=#')
        assert b'Invalid color code' in rv.data



if __name__ == '__main__':
    unittest.main()
