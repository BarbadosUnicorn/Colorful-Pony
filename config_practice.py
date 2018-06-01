import configparser, pymysql, bcrypt
import os



def create_config(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "DB_password", "DB_password_value")
    config.set("Settings", "mail_password", "mail_password_value")


    with open(path, "w") as config_file:
        config.write(config_file)


def get_config(path):
    """
    Returns the config object
    """
    if not os.path.exists(path):
        create_config(path)

    config = configparser.ConfigParser()
    config.read(path)
    return config


def get_setting(path, section, setting):
    """
    Print out a setting
    """
    config = get_config(path)
    value = config.get(section, setting)
    #msg = "{section} {setting} is {value}".format(section=section, setting=setting, value=value)
    #print(msg)
    return value


def update_setting(path, section, setting, value):
    """
    Update a setting
    """
    config = get_config(path)
    config.set(section, setting, value)
    with open(path, "w") as config_file:
        config.write(config_file)


def delete_setting(path, section, setting):
    """
    Delete a setting
    """
    config = get_config(path)
    config.remove_option(section, setting)
    with open(path, "w") as config_file:
        config.write(config_file)


def random_string_generator(len):    # Making string of [A-Z, a-z, 0-9] with desired length. Len >= 0
    import string, random

    token = ""
    for x in range(len):
        token += random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)

    return token


'''
if __name__ == "__main__":
    path = "settings.ini"
    DB_password = get_setting(path, 'Settings', 'DB_password')
    mail_password = get_setting(path, 'Settings', 'mail_password')

    #update_setting(path, "Settings", "font_size", "12")
    #delete_setting(path, "Settings", "font_style")
'''

def send_email(message_text, senders_adress, mail_password, recipient_adress):
    import smtplib
    from email.mime.text import MIMEText

    me = senders_adress
    you = recipient_adress
    smtp_server = 'smtp.gmail.com'
    msg = MIMEText(message_text)
    msg['Subject'] = 'E-mail verification '
    msg['From'] = me
    msg['To'] = you
    s = smtplib.SMTP(smtp_server)
    s.starttls()
    s.login(senders_adress, mail_password)
    s.sendmail(me, [you], msg.as_string())
    s.quit()


#path = "settings.ini"

#mail_password = get_setting(path, 'Settings', 'mail_password')
#project_mail_adress = get_setting(path, 'Settings', 'project_mail')

#send_email('Hello, G-mail!', project_mail_adress, mail_password,'xtraand0ne@gmail.com')

'''
db = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="00000000",\
                                                                   database="pony_color_db", charset="utf8")
cursor = db.cursor()


query = """SELECT id FROM color WHERE name="Баклажановый0" """

cursor.execute(query)
results = cursor.fetchall()

print(results is ())

db.close()
'''

password = '日本語' # random_string_generator(730)
password = password.encode()
print(password)
#password = b"super secret password"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(len(hashed.decode()))
if bcrypt.checkpw(password, hashed):
    print("It Matches!")
else:
    print("It Does not Match :(")
print(password.decode())

'''
a = 'Some index files failed to download they have been ignored or old ones used instead 5'
count = 0
for i in a:
    if not i.isalpha() and not i == ' ':
        count += 1
if count != 0:
    print('Строка содержит символы отличные от букв и пробелов')
else:
    print('Строка несодержит символы отличные от букв и пробелов')
'''


