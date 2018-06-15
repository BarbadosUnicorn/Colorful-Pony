import imaplib
import email
from online_determinator import get_setting

path = "settings.ini"

FROM_EMAIL = get_setting(path, 'Settings', 'project_mail')
FROM_PWD = get_setting(path, 'Settings', 'mail_password')


def read_email_from_gmail(senders_address, mail_password, recipient_address):    # It searching for senders last message in recipients mailbox
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

########################################################################################################################
#                                 Make it able to delete all "senders" messages                                        #
########################################################################################################################

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


print(read_email_from_gmail(FROM_EMAIL, FROM_PWD,FROM_EMAIL))

'''
# Import the email modules we'll need
from email.parser import Parser
from email.message import Message

#  If the e-mail headers are in a file, uncomment this line:
#headers = Parser().parse(open(messagefile, 'r'))

#  Or for parsing headers in a string, use:
headers = Parser().parsestr('From: <user@example.com>\n'
        'To: <someone_else@example.com>\n'
        'Subject: Test message\n'
        '\n'
        'Body would go here\n')

body = Message().get_payload()
#  Now the header items can be accessed as a dictionary:
print('To: %s' % headers['to'])
print('From: %s' % headers['from'])
print('Subject: %s' % headers['subject'])
print('Body: %s' % body)
print(headers.__dict__)
'''
'''
import base64
mail_list = mail.list()
        print("mail_list:")
        print(mail_list[1])

        select_results = mail.select("INBOX")
        print('select_results:')
        print(select_results[1])

        search_results = mail.search(None, 'ALL')
        print("search_results:")
        print(search_results)

        first_message = mail.fetch(b'1', '(RFC822)')
        print("first_message:")
        print(first_message)


        status, data = mail.fetch(b'1', '(RFC822)')

        msg = email.message_from_bytes(data[0][1], _class = email.message.EmailMessage)

        payload = msg.get_payload()[ 0 ]

        payload_data = payload.get_payload()
        #print("payload_data:")
        #encoded = payload_data.encode()
        #decoded = base64.b64decode(payload_data)
        #print(decoded.decode())
'''
'''
status, data = mail.fetch(str(i).encode(), '(RFC822)')
            #print("data[0][1].decode():")
            #print(data[0][1].decode())    # To get message text as it looks in browser
'''
'''
search_res = mail.search(None, '(FROM "<%s>")' % FROM_EMAIL)

        type, data = search_res
        mail_ids = data[0]

        id_list = mail_ids.split()

        if not len(id_list) == 0:
            first_email_id = int(id_list[0])
            latest_email_id = int(id_list[-1])

            for i in range(latest_email_id,first_email_id-1, -1):
                print("i = " + str(i))

                status, data = mail.fetch(str(i).encode(), '(RFC822)')

                msg = email.message_from_bytes(data[0][1], _class = email.message.EmailMessage)
                print('msg._payload:')
                print(msg._payload)
        else:
            print('No messages found')
'''
