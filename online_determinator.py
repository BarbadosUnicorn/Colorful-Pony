import pymysql, configparser, os, bcrypt
from flask import Flask, jsonify, request
from flask_mail import Mail, Message

path = "settings.ini"
app = Flask(__name__)


def color_retriever(color_input):    # Making R, G and B variables from input string

    rgb = str(color_input)

    if len(rgb) != 6: int('', 16)    # Test for catching exceptions on "non-6-digit" colors
    int(rgb, 16)                     # Another test for catching exceptions on "non-HEX" colors

    R16 = rgb[len(rgb) - 6:len(rgb) - 4]
    G16 = rgb[len(rgb) - 4:len(rgb) - 2]
    B16 = rgb[len(rgb) - 2:]

    color = {'R': R16, 'G': G16, 'B': B16}

    return color


def RGBtoLab(color):    # Converter from RGB to CIE Lab. Reference white used D65/2° standard illuminant

        # RGB to XYZ
        r = int(color['R'], 16) / 255
        g = int(color['G'], 16) / 255
        b = int(color['B'], 16) / 255

        if ( r > 0.04045 ):
            r = ( ( r + 0.055 ) / 1.055 ) ** 2.4
        else:
            r = r / 12.92

        if ( g > 0.04045 ):
            g = ( ( g + 0.055 ) / 1.055 ) ** 2.4
        else:
            g = g / 12.92

        if ( b > 0.04045 ):
            b = ( ( b + 0.055 ) / 1.055 ) ** 2.4
        else:
            b = b / 12.92

        X = r * 41.24 + g * 35.76 + b * 18.05
        Y = r * 21.26 + g * 71.52 + b * 7.22
        Z = r * 1.93 + g * 11.92 + b * 95.05

        # XYZ to CIE Lab
        X = X / 95.047
        Y = Y / 100
        Z = Z / 108.883

        if ( X > 0.008856 ):
            X = X ** ( 1/3 )
        else:
            X = ( 7.787 * X ) + ( 16 / 116 )

        if ( Y > 0.008856 ):
            Y = Y ** ( 1/3 )
        else:
            Y = ( 7.787 * Y ) + ( 16 / 116 )

        if ( Z > 0.008856 ):
            Z = Z ** ( 1/3 )
        else:
            Z = ( 7.787 * Z ) + ( 16 / 116 )

        L = ( 116 * Y ) - 16
        a = 500 * ( X - Y )
        b = 200 * ( Y - Z )
        # Any of L, a and b can be '+' or '-'

        return {'L': L, 'a': a, 'b': b}


def create_config(path): # Create a config file
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "DB_password", "DB_password_value")
    config.set("Settings", "mail_password", "mail_password_value")
    config.set("Settings", "project_mail", "project.mail@example.com")
    config.set("Settings", "salt", "00000000000000000000000000000000")
    config.set("Settings", "URL", "project_URL")

    with open(path, "w") as config_file:
        config.write(config_file)


def get_config(path):  # Returns the config object
    if not os.path.exists(path):
        create_config(path)

    config = configparser.ConfigParser()
    config.read(path)
    return config


def get_setting(path, section, setting):  # Get a setting
    config = get_config(path)
    value = config.get(section, setting)
    return value


def send_email(message_text, senders_address, mail_password, recipient_address):
    import smtplib
    from email.mime.text import MIMEText

    me = senders_address
    you = recipient_address
    smtp_server = 'smtp.gmail.com'
    msg = MIMEText(message_text)
    msg['Subject'] = 'E-mail verification '
    msg['From'] = me
    msg['To'] = you
    s = smtplib.SMTP(smtp_server)
    s.starttls()
    s.login(senders_address, mail_password)
    s.sendmail(me, [you], msg.as_string())
    s.quit()


def random_string_generator(length):    # Making string of [A-Z, a-z, 0-9] with desired length. Len >= 0
    import string, random

    token = ""
    for x in range(length):
        token += random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)

    return token


def test_email(email):
    import re
    pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    if re.match(pattern, email):
        return 1==1
    else:
        return 1==0


def simple_response(status_code, status, description):
    message = {"status":status,"description":description}
    resp = jsonify(message)
    resp.status_code = status_code
    return resp


def expires(days):
    import time
    lease = days * 24 * 60 * 60  # days in seconds
    end = time.gmtime(time.time() + lease)
    expires = time.strftime("%a, %d-%b-%Y %T GMT", end)
    return expires


DB_password = get_setting(path, 'Settings', 'DB_password')


@app.route('/api/get_pony_by_color')  # Function to find closest color in database.
def closest_color_online_determinator():

    color_input = request.args.get('color')
    cookies = request.cookies

    if not('value' in cookies):
        return simple_response(403, "error", "Not authorised")

    if 'value' in cookies:
        db = pymysql.connect(host="127.0.0.1", port=3306, user="root", password=DB_password,\
                                                                   database="pony_color_db", charset="utf8")
        cursor = db.cursor()
        escaped_value = cookies['value']
        query = """SELECT id FROM sessions WHERE key="{KEY}" """.format(KEY = escaped_value)    # Find user, hash and salt in DB
        cursor.execute(query)

        results = cursor.fetchall()

        if results is ():  # Here we come if user not logged in.
            db.close()
            return simple_response(403, "error", "Not authorised")

        else:    # Here we come if everything OK.

            try:
                color = color_retriever(color_input)    # Try-except block for better input color processing

            except:
                db.close()
                return simple_response(403, "error", "Invalid color code.")

            color = RGBtoLab(color)

            query = """SELECT color.id, color.name, pony.name, body_part.name, color.RGB
                      FROM pony_color
                      INNER JOIN color     ON pony_color.color_id = color.id
                      INNER JOIN pony      ON pony_color.pony_id  = pony.id
                      INNER JOIN body_part ON pony_color.type_id  = body_part.id
                      GROUP BY color.id, pony.id, body_part.id
                      ORDER BY MIN((L - {L})*(L - {L})+(a - {a})*(a - {a})+(b - {b})*(b - {b})) LIMIT 1""".format(L = color['L'],\
                                                                                                  a = color['a'], b = color['b'])

            cursor.execute(query)
            results = cursor.fetchall()

            db.close()

            response = '[ '

            for row in results:

                    #color_id    = row[0]
                    color_name  = row[1]
                    name        = row[2]
                    body_part   = row[3]
                    color       = row[4]
                    response = response[:-1] + '{"body_part":"%s","color":"%s","name":"%s","color_name":"%s"},' %(body_part,\
                                                                                        color, name, color_name)    # Concating objects to response

                    response = response[:-1] + ']'    # JSON response is an array of objects

            return response


@app.route('/api/signup')   # Creates non-activated user in DB and sends activation code via link. Code also writes in DB. E-mail is username.
def user_creator():

    user_mail = request.args.get('mail')
    user_password = request.args.get('password')

    if len(str(user_password)) < 8:  # If it's shorter then 8 symbols - rise error!
        return simple_response(403, "error", "Password must be at least 8 symbols long.")
        pass

    if not test_email(user_mail):    # Check if email match RFC 6531 standards.
        return simple_response(403, "error", "Email doesn't match RFC 6531 standards.")
        pass

    project_mail = get_setting(path, 'Settings', 'project_mail')
    project_mail_password = get_setting(path, 'Settings', 'mail_password')
    project_salt = get_setting(path, 'Settings', 'salt')
    URL = get_setting(path, 'Settings', 'URL')

    db = pymysql.connect(host="127.0.0.1", port=3306, user="root", password=DB_password,\
                                                                   database="pony_color_db", charset="utf8")
    cursor = db.cursor()
    escaped_user_mail = db.escape(user_mail)
    user_password = db.escape(user_password)

    query = """SELECT active, verification_code FROM users WHERE email="{MAIL}" """.format(MAIL = escaped_user_mail)    # Check if it's already in DB

    cursor.execute(query)
    results = cursor.fetchall()
    print(results)

    if results is ():  # Here we come if there is no such e-mail in DB. It's user-creation time!
        salt_one = random_string_generator(32)
        project_salt = project_salt
        to_hash = project_salt + user_password + salt_one             ######## THIS IS HOW PASSWORDS ########
        hashed = bcrypt.hashpw(to_hash.encode(), bcrypt.gensalt())    ########    MUST BE HASHED     ########
        hash = hashed.decode()
        verification_code =  random_string_generator(70)
        escaped_verification_code = db.escape(verification_code)
        active = 0

        query = """INSERT INTO users (email, hash, salt_one, verification_code, active)
                   VALUES ("{MAIL}", "{HASH}", "{SALT_ONE}", "{VERIFICATION_CODE}", "{ACTIVE}") """.format(\
                                                    MAIL = escaped_user_mail, HASH = hash, SALT_ONE = salt_one, \
                                                    VERIFICATION_CODE = escaped_verification_code, ACTIVE = active)

        cursor.execute(query)
        db.commit()    # Always commit changes!
        verification_URL = URL + '/api/verify?code=' + verification_code
        send_email(verification_URL, project_mail, project_mail_password, user_mail) # Sending link to verify e-mail
        db.close()
        return simple_response(200, "success", "Account created. Activation link sent to your email.")

    elif results[0] == 1:    # If e-mail already activated - 403 [e-mail is used]
        db.close()
        return simple_response(403, "error", "E-mail is used")

    else:    # Send new activation code
        verification_code =  random_string_generator(70)
        escaped_verification_code = db.escape(verification_code)

        query = """UPDATE users
                   SET verification_code="{VERIFICATION_CODE}"
                   WHERE email="{MAIL}" """.format(VERIFICATION_CODE = escaped_verification_code, MAIL = escaped_user_mail)

        cursor.execute(query)   # Changing activation key
        db.commit()    # Always commit changes!
        db.close()

        verification_URL = URL + '/api/verify?code=' + verification_code

        send_email(verification_URL, project_mail, project_mail_password, user_mail) # Sending link to verify e-mail

        return simple_response(403, "error", "E-mail is not activated. Check your mailbox for new activation code. It may be in spam folder.")


@app.route('/api/verify')    # Get verification code, activate user if E-mail and code match DB record.
def verification():

    verification_code = request.args.get('code')

    db = pymysql.connect(host="127.0.0.1", port=3306, user="root", password=DB_password,\
                                                                   database="pony_color_db", charset="utf8")
    cursor = db.cursor()
    verification_code = db.escape(verification_code)

    query = """SELECT id FROM users WHERE verification_code="{CODE}" """.format(CODE = verification_code)

    cursor.execute(query)
    results = cursor.fetchall()

    if results is ():
        db.close()
        return simple_response(403, "error", "Invalid verification code.")

    else:
        query = """UPDATE users 
                   SET active = 1, verification_code = 0
                   WHERE verification_code="{CODE}" """.format(CODE = verification_code)     # Here the table should be modified.
        cursor.execute(query)
        db.commit()
        db.close()
        return simple_response(200, "success", "Verification complete")


@app.route('/api/resend')    # Sends new verification code and changes it in DB. For non-existing users ni DB say that they are not in DB.
def resend_verification_code():

    user_mail = request.args.get('mail')

    project_mail = get_setting(path, 'Settings', 'project_mail')
    project_mail_password = get_setting(path, 'Settings', 'mail_password')
    URL = get_setting(path, 'Settings', 'URL')

    db = pymysql.connect(host="127.0.0.1", port=3306, user="root", password=DB_password,\
                                                                   database="pony_color_db", charset="utf8")
    cursor = db.cursor()
    escacped_user_mail = db.escape(user_mail)

    query = """SELECT active FROM users WHERE email="{MAIL}" """.format(MAIL = escacped_user_mail)    # Check if it's already in DB

    cursor.execute(query)
    results = cursor.fetchall()

    if results is ():  # Here we come if there is no such e-mail in DB.
        db.close()
        return simple_response(403, "error", "No such user in database")

    elif results[0] == 1:  # If e-mail already already activated - 403 [e-mail is used]
        db.close()
        return simple_response(403, "error", "This account is already activated")

    else:    # Send new activation code
        verification_code =  random_string_generator(70)
        verification_code = db.escape(verification_code)

        query = """UPDATE users
                   SET verification_code="{VERIFICATION_CODE}"
                   WHERE email="{MAIL}" """.format(VERIFICATION_CODE = verification_code, MAIL = escacped_user_mail)

        cursor.execute(query)    # Changing activation key
        db.commit()
        db.close()

        verification_URL = URL + '/api/verify?code=' + verification_code

        send_email(verification_URL, project_mail, project_mail_password, user_mail) # Sending link to verify e-mail

        return simple_response(200, "success", "Check your mailbox for new activation code. It may be in spam folder.")


@app.route('/api/signin')
def sign_in():

    user_mail = request.args.get('mail')
    user_password = request.args.get('password')
    project_salt = get_setting(path, 'Settings', 'salt')

    db = pymysql.connect(host="127.0.0.1", port=3306, user="root", password=DB_password,\
                                                                   database="pony_color_db", charset="utf8")
    cursor = db.cursor()
    escaped_user_mail = db.escape(user_mail)
    user_password = db.escape(user_password)

    query = """SELECT active, hash, salt_one FROM users WHERE email="{MAIL}" """.format(MAIL = escaped_user_mail)    # Find user, hash and salt in DB

    cursor.execute(query)
    results = cursor.fetchall()

    if results is ():  # Here we come if there is no such e-mail in DB.
        db.close()
        return simple_response(403, "error", "No such user in database")

    elif results[0] == 0: # If account not activated
        db.close()
        return simple_response(403, "error", "E-mail is not activated")

    else:  # If account activated - check password
        hash = results[0][1]
        hash = hash.encode()
        salt_one = results[0][2]
        password = project_salt + user_password + salt_one             ######## THIS IS HOW PASSWORDS ########
        if bcrypt.checkpw(password.encode(), hash):                    ########    MUST BE CHECKED    ########
            # If it match
            value = random_string_generator(43)
            escaped_value = db.escape(value)
            expire_date = expires(1)
            print('value length = ' + str(len(escaped_value)))
            print('timestamp length = ' + str(len(expire_date)))

            query = """INSERT INTO sessions (value, time_stamp)
                       VALUES ("{VALUE}", "{TIME_STAMP}") """.format(\
                                                    VALUE = escaped_value, TIME_STAMP = expire_date)
            print(query)
            cursor.execute(query)
            db.commit()
            db.close()

            URL = get_setting(path, 'Settings', 'URL')
            my_cookie = {'domain':URL,
                         'expires':expire_date,
                         'name':'pony_color_determinator',
                         'path':'/',
                         'value': value,
                         'version':0}

            return simple_response(200, "success", "Signed in successfully").set_cookie(my_cookie)

        else:    # If password doesn't match
            db.close()
            return simple_response(403, "error", "Wrong password")


@app.route('/api/signout')
def sign_out():
    cookies = request.cookies
    if 'value' in cookies:
        db = pymysql.connect(host="127.0.0.1", port=3306, user="root", password=DB_password,\
                                                                   database="pony_color_db", charset="utf8")
        escaped_value = db.escape(cookies['value'])
        cursor = db.cursor()
        query = """DELETE FROM sessions WHERE key="{KEY}" """.format(KEY = escaped_value)    # Find user, hash and salt in DB
        cursor.execute(query)
        db.commit()
        db.close()
        return simple_response(200, "success", "Signed out successfully")


# Adress of fun: http://localhost:5000/api/get_pony_by_color?color=053550
