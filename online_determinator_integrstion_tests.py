import os
import online_determinator
import unittest
import tempfile
import imaplib
import email

def signin(self, username, password):
    return self.app.post('/api/signin', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def signout(self):
    return self.app.get('/api/signout', follow_redirects=True)


def read_email_from_gmail(senders_address, mail_password, recipient_address):    # It searching for "senders" last message in "recipients" mailbox
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(recipient_address, mail_password)
        mail.select('inbox')

        search_res = mail.search(None, '(FROM "<%s>")' % senders_address)

        type, data = search_res
        mail_ids = data[0]

        id_list = mail_ids.split()

        if not len(id_list) == 0:
            latest_email_id = int(id_list[-1])

            status, data = mail.fetch(str(latest_email_id).encode(), '(RFC822)')

            msg = email.message_from_bytes(data[0][1], _class = email.message.EmailMessage)

            mail.logout()

            return msg._payload
        else:
            mail.logout()

            return ''

    except Exception as e:
        print('Exception:')
        print(e)
        try:
            mail.logout()
            print('Logged out')
        except Exception:
            print("Unable to close mail-server connection")


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
