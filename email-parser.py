import imaplib
import email
import base64
from online_determinator import get_setting

path = "settings.ini"

FROM_EMAIL = get_setting(path, 'Settings', 'project_mail')
FROM_PWD = get_setting(path, 'Settings', 'mail_password')
SMTP_SERVER = "imap.gmail.com"


def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        search_res = mail.search(None, 'ALL')
        type, data = search_res

        mail_ids = data[0]

        id_list = mail_ids.split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id,first_email_id, -1):
            typ, data = mail.fetch(str(i).encode(), '(RFC822)' )

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(data[0][1], _class = email.message.EmailMessage) #email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print('From : ' + email_from)
                    print('Subject : ' + email_subject + '\n')
        mail.logout()

    except Exception as e:
        print('Exception:')
        print(e)
        try:
            mail.logout()
            print('Logged out')
        except Exception:
            print("Can't close mail")


read_email_from_gmail()

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
