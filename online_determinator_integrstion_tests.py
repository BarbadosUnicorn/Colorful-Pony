import os
import online_determinator
import unittest
import tempfile

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


    def test_getting_color(self):
        rv = self.app.get('/api/get_pony_by_color?color=053550')
        self.assertEqual(rv._status_code, 200)


    def test_invalid_ccolor_code(self):
        rv = self.app.get('/api/get_pony_by_color?color=#')
        assert  b'Invalid color code' in rv.data



if __name__ == '__main__':
    unittest.main()
