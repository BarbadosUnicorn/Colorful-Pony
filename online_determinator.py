import atexit, bcrypt, configparser, json, os, pymysql, random, re, smtplib, string, time
from flask import Flask, jsonify, request
from email.mime.text import MIMEText

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
    if not app.testing:
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
    else:
        print('Message sending not allowed while testing!')


def random_string_generator(length):    # Making string of [A-Z, a-z, 0-9] with desired length. Len >= 0
    token = ""
    for x in range(length):
        token += random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
    return token


def test_email(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    if re.match(pattern, email):
        return True
    else:
        return False


def simple_response(status_code, status, description):
    message = {"status":status,"description":description}
    resp = jsonify(message)
    resp.status_code = status_code
    return resp


def expires(days):
    lease = days * 24 * 60 * 60  # days in seconds
    end = time.gmtime(time.time() + lease)
    expires = time.strftime("%a, %d-%b-%Y %T GMT", end)
    return expires


project_mail = get_setting(path, 'Settings', 'project_mail')
project_mail_password = get_setting(path, 'Settings', 'mail_password')
project_salt = get_setting(path, 'Settings', 'salt')
URL = get_setting(path, 'Settings', 'URL')
DB_password = get_setting(path, 'Settings', 'DB_password')

db = pymysql.connect(host="127.0.0.1", port=3306, user="root", password=DB_password,\
                                       database="pony_color_db", charset="utf8") # Connecting to DB when app started
cursor = db.cursor()


def role_finder(cookies):  # Roles are 'user' or 'admin'. If resp['code'] == 200 - user logged in.
    resp = {'role': '', 'code': 403, 'description': 'error', 'message': ''}

    if 'pony_color_determinator' not in cookies:  # If you have no cookies
        resp['message'] = "Not authorised"
        return resp

    else:
        escaped_value = db.escape(cookies['pony_color_determinator'])

        query = """SELECT users.role, users.ban, users.email, users.active
                   FROM sessions
                   INNER JOIN users     ON sessions.user_id = users.id
                   WHERE value="{VALUE}" """.format(VALUE = escaped_value)  # Find users role in DB

        cursor.execute(query)
        results = cursor.fetchall()

        if not results:  # Here we come if user not logged in.
            resp['message'] = "Not authorised"
            return resp

        elif results[0][3] == 2:  # Here we come user banned permanently
            resp['message'] = "You are banned permanently"
            return resp

        elif results[0][1] > int(time.time()):  # Here we come user banned
            resp['message'] = "You are banned until: %s UTC" \
                              %time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(results[0][1])))
            return resp

        else:    # Here we come user logged in
            resp = {'role': results[0][0], 'code': 200, 'description': 'success', 'message': 'Role founded', 'email': results[0][2]}
            return resp

########################################################################################################################

########################################################################################################################


@app.route('/api/get_pony_by_color')  # Function to find closest color in database.
def closest_color_online_determinator():

    color_input = request.args.get('color')
    cookies = request.cookies
    role = role_finder(cookies)

    if role['code'] == 403:
        return simple_response(role['code'], role['description'], role['message'])

    else:    # Here we come if everything OK.
        try:
            color = color_retriever(color_input)    # Try-except block for better input color processing

        except:
            return simple_response(403, "error", "Invalid color code.")

        color = RGBtoLab(color)

        query =  """SELECT color.id, color.name, pony.name, body_part.name, color.RGB
                    FROM pony_color
                    INNER JOIN color     ON pony_color.color_id = color.id
                    INNER JOIN pony      ON pony_color.pony_id  = pony.id
                    INNER JOIN body_part ON pony_color.type_id  = body_part.id
                    GROUP BY color.id, pony.id, body_part.id
                    ORDER BY MIN((L - {L})*(L - {L})+(a - {a})*(a - {a})+(b - {b})*(b - {b})) LIMIT 1""".format(L = color['L'],\
                                                                                                  a = color['a'], b = color['b'])

        cursor.execute(query)
        results = cursor.fetchall()

        response = []
        for row in results:

            #color_id    = row[0]
            color_name  = row[1]
            name        = row[2]
            body_part   = row[3]
            color       = row[4]

            response_part = {"body_part": body_part, "color": color, "name": name, "color_name": color_name}
            response.append(response_part)

        return str(response)


@app.route('/api/signup', methods = ['POST'])   # Creates non-activated user in DB and sends activation code via link. Code also writes in DB. E-mail is username.
def user_creator():

    user_mail = request.args.get('mail')
    user_password = request.args.get('password')
    escaped_user_mail = db.escape(user_mail)
    user_password = db.escape(user_password)

    if len(str(user_password)) < 8:  # If it's shorter then 8 symbols - rise error!
        return simple_response(403, "error", "Password must be at least 8 symbols long.")

    if not test_email(user_mail):    # Check if email match RFC 6531 standards.
        return simple_response(403, "error", "Email doesn't match RFC 6531 standards.")

    query = """SELECT active, verification_code FROM users WHERE email="{MAIL}" """.format(MAIL = escaped_user_mail)    # Check if it's already in DB

    cursor.execute(query)
    results = cursor.fetchall()

    if not results:  # Here we come if there is no such e-mail in DB. It's user-creation time!
        salt_one = random_string_generator(32)
        to_hash = project_salt + user_password + salt_one             ######## THIS IS HOW PASSWORDS ########
        hashed = bcrypt.hashpw(to_hash.encode(), bcrypt.gensalt())    ########    MUST BE HASHED     ########
        hash = hashed.decode()
        verification_code =  random_string_generator(70)
        escaped_verification_code = db.escape(verification_code)
        active = 0

        query = """INSERT INTO users (email, hash, salt_one, verification_code, active, role)
                   VALUES ("{MAIL}", "{HASH}", "{SALT_ONE}", "{VERIFICATION_CODE}", "{ACTIVE}", "{ROLE}") """.format(\
                                                    MAIL = escaped_user_mail, HASH = hash, SALT_ONE = salt_one, \
                                                    VERIFICATION_CODE = escaped_verification_code, ACTIVE = active,\
                                                    ROLE = 'user')

        cursor.execute(query)
        db.commit()    # Always commit changes!

        verification_URL = URL + '/api/verify?code=' + verification_code
        send_email(verification_URL, project_mail, project_mail_password, user_mail) # Sending link to verify e-mail

        return simple_response(200, "success", "Account created. Activation link sent to your email.")

    elif results[0][0] == 1:    # If e-mail already activated - 403 [e-mail is used]
        return simple_response(403, "error", "E-mail is used")

    else:    # Send new activation code
        verification_code =  random_string_generator(70)
        escaped_verification_code = db.escape(verification_code)

        query = """UPDATE users
                   SET verification_code="{VERIFICATION_CODE}"
                   WHERE email="{MAIL}" """.format(VERIFICATION_CODE = escaped_verification_code, MAIL = escaped_user_mail)

        cursor.execute(query)   # Changing activation key
        db.commit()    # Always commit changes!

        verification_URL = URL + '/api/verify?code=' + verification_code
        send_email(verification_URL, project_mail, project_mail_password, user_mail)  # Sending link to verify e-mail

        return simple_response(403, "error", "E-mail is not activated. Check your mailbox for new activation code. It may be in spam folder.")


@app.route('/api/verify')    # Get verification code, activate user if E-mail and code match DB record.
def verification():

    verification_code = request.args.get('code')
    verification_code = db.escape(verification_code)

    query = """SELECT id FROM users WHERE verification_code="{CODE}" """.format(CODE = verification_code)

    cursor.execute(query)
    results = cursor.fetchall()

    if not results:
        return simple_response(403, "error", "Invalid verification code.")

    else:
        query = """UPDATE users 
                   SET active = 1, verification_code = 0
                   WHERE verification_code="{CODE}" """.format(CODE = verification_code)     # Here the table should be modified.
        cursor.execute(query)
        db.commit()
        return simple_response(200, "success", "Verification complete")


@app.route('/api/resend')    # Sends new verification code and changes it in DB. For non-existing users ni DB say that they are not in DB.
def resend_verification_code():

    user_mail = request.args.get('mail')
    escaped_user_mail = db.escape(user_mail)

    query = """SELECT active FROM users WHERE email="{MAIL}" """.format(MAIL = escaped_user_mail)    # Check if it's already in DB

    cursor.execute(query)
    results = cursor.fetchall()

    if not results:  # Here we come if there is no such e-mail in DB.  if results is ():
        return simple_response(403, "error", "No such user in database")

    elif results[0][0] == 1:  # If e-mail already already activated - 403 [e-mail is used]
        return simple_response(403, "error", "This account is already activated")

    else:    # Send new activation code
        verification_code =  random_string_generator(70)
        escaped_verification_code = db.escape(verification_code)

        query = """UPDATE users
                   SET verification_code="{VERIFICATION_CODE}"
                   WHERE email="{MAIL}" """.format(VERIFICATION_CODE = escaped_verification_code, MAIL = escaped_user_mail)
        cursor.execute(query)    # Changing activation key
        db.commit()

        verification_URL = URL + '/api/verify?code=' + verification_code
        send_email(verification_URL, project_mail, project_mail_password, user_mail) # Sending link to verify e-mail

        return simple_response(200, "success", "Check your mailbox for new activation code. It may be in spam folder.")


@app.route('/api/signin', methods = ['POST'])
def sign_in():

    user_mail = request.args.get('mail')
    user_password = request.args.get('password')
    escaped_user_mail = db.escape(user_mail)
    user_password = db.escape(user_password)

    query = """SELECT active, hash, salt_one, id, ban
               FROM users
               WHERE email="{MAIL}" """.format(MAIL = escaped_user_mail)    # Find user, hash and salt in DB

    cursor.execute(query)
    results = cursor.fetchall()

    if not results:  # Here we come if there is no such e-mail in DB.
        return simple_response(403, "error", "No such user in database")

    elif results[0][0] == 0: # If account not activated
        return simple_response(403, "error", "E-mail is not activated")

    elif results[0][4] > int(time.time()): # If user is banned
        return simple_response(403, "error", "You are banned until: %s UTC" \
                              %time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(results[0][4]))))

    elif results[0][1] == 2:  # If user is banned permanently
         return simple_response(403, "error", "You are banned permanently")

    else:  # If account activated - check password
        hash = results[0][1].encode()
        salt_one = results[0][2]
        password = project_salt + user_password + salt_one             ######## THIS IS HOW PASSWORDS ########
        if bcrypt.checkpw(password.encode(), hash):                    ########    MUST BE CHECKED    ########
            # If it match
            value = random_string_generator(43)
            escaped_value = db.escape(value)
            expire_date = expires(1)
            user_id = results[0][3]

            query = """INSERT INTO sessions (value, time_stamp, user_id)
                       VALUES ("{VALUE}", "{TIME_STAMP}", "{USER_ID}") """.format(VALUE = escaped_value,\
                                                                                  TIME_STAMP = expire_date,\
                                                                                  USER_ID = user_id)
            cursor.execute(query)
            db.commit()

            response = simple_response(200, "success", "Signed in successfully")
            response.set_cookie('pony_color_determinator', value=value, max_age=None, expires=expire_date, path='/',\
                                 domain=None, secure=False, httponly=False, samesite=None) # Because  .set_cookie() doesn't return 'response' object

            if results[0][4] != '':  # If user was banned

                query = """UPDATE users 
                           SET ban = ""
                           WHERE email="{USER_ID}" """.format(USER_ID = user_id)

                cursor.execute(query)
                db.commit()

            return response

        else:    # If password doesn't match
            return simple_response(403, "error", "Wrong password")


@app.route('/api/signout', methods = ['GET'])
def sign_out():

    cookies = request.cookies

    if 'pony_color_determinator' in cookies:
        escaped_value = db.escape(cookies['pony_color_determinator'])

        query = """DELETE FROM sessions WHERE value="{VALUE}" """.format(VALUE = escaped_value)    # Find user, hash and salt in DB

        cursor.execute(query)
        db.commit()
        return simple_response(200, "success", "Signed out successfully")
    else:
        return simple_response(403, "error", "Not authorised")

########################################################################################################################


@app.route('/api/get_all_ponies', methods = ['GET'])  # Function to view all ponies in DB
def pony_viewer():

    page_number = request.args.get('page')
    number_of_ponies = request.args.get('ponies_per_page')
    cookies = request.cookies
    role = role_finder(cookies)

    if role['code'] == 403:
        return simple_response(role['code'], role['description'], role['message'])

    else:
        try:
            page_number = int(page_number)
            number_of_ponies = int(number_of_ponies)
            if page_number <= 0 or number_of_ponies <= 0: raise ValueError

        except ValueError:
            return simple_response(403, "error", "Page and ponies_per_page should be integer")

        query = """SELECT id
                   FROM pony"""  # To get all pony_id's

        cursor.execute(query)
        results = cursor.fetchall()

        ponies_total = len(results)
        start_id = number_of_ponies * (page_number - 1)

        if start_id > ponies_total:
            return simple_response(403, "error", "There is only %s ponies in database!" % str(ponies_total))

        end_id = start_id + number_of_ponies -1

        if end_id >= ponies_total:
            end_id = ponies_total - 1

        first_pony_id = results[start_id][0]
        last_pony_id  = results[end_id][0]

        query = """SELECT pony.id, pony.name, body_part.name, color.RGB, color.name
                   FROM pony_color
                   INNER JOIN color     ON pony_color.color_id = color.id
                   INNER JOIN pony      ON pony_color.pony_id  = pony.id
                   INNER JOIN body_part ON pony_color.type_id  = body_part.id
                   WHERE pony.id >= {START}
                   GROUP BY pony.id, body_part.id, color_id
                   HAVING pony.id <= {END};""".format(START = first_pony_id, END = last_pony_id)

        cursor.execute(query)
        results = cursor.fetchall()

        pony_dict = {}
        for line in results:

            pony_id,  pony_name,  body_part,  RGB_color,  color_name = line[0], line[1], line[2], line[3], line[4]

            if pony_id in pony_dict:  # Searching for 'pony_id' in dictionary
                if body_part in pony_dict[pony_id]["body_part"]:  # Searching for 'body_part' in 'body_parts' of current pony in dictionary
                    pony_dict[pony_id]["body_part"][body_part].append({RGB_color: color_name})  # If we have this 'body_part' - adding current 'color_dict' to 'color_list'
                else:
                    pony_dict[pony_id]["body_part"][body_part] = [{RGB_color: color_name}]  # If no such 'body_part' - adding current 'body_part' to 'body_part_dictionary'
            else:
                pony_dict[pony_id] = {"pony_id": pony_id, "pony_name": pony_name, "body_part": {body_part: [{RGB_color: color_name}]}}  # If no such 'pony' - add it to 'pony_dict'

        response = list(pony_dict.values())  # ~~~Dark magic of converting dictionaries to lists~~~

        return str(response)


@app.route('/api/edit_pony', methods = ['POST', 'PUT', 'DELETE'])    # Editing ponies data in DB
def pony_editor():

    cookies = request.cookies
    role = role_finder(cookies)

    if role['code'] == 403:
        return simple_response(role['code'], role['description'], role['message'])

    elif role['role'] == 'user':    # Here we come if role 'user'
        return simple_response(role['code'], role['description'], "Pony editing allowed only for admin's")

    else:  # If role is 'admin'
        if request.method == 'POST':  # adding
            # parse 'pony object', disassemble it, create pony_object entry                                   DONE
            # create lists of content for pony, color and pony_color,                                         PROCESSING
            # search for same name and colors, modify list for pony_color
            # add data
            pony_input = request.args.get('pony')

            try:
                pony_object = json.loads(pony_input)

            except:
                try:
                    pony_object = json.loads(pony_input.replace("'", '"'))  # Change all ' to ". Because parser is dumb.

                except:  # Here we come if input is not JSON
                    return simple_response(403, "error", "Wrong pony object. You can see example on /api/get_all_ponies")

            pony_object  = pony_object  # Now it's pony_object like:
# {'pony_id': 4, 'pony_name': 'Pinkie Pie', 'body_part': {'body': [{'#F3B6CF': 'Амарантово-розовый'}], 'hair': [{'#ED458B': 'Глубокий пурпурно-розовый'}], 'eye': [{'#186F98': 'Небесно-синий'}, {'#82D1F4': 'Светло-голубой'}]}}
            pony_name = pony_object['pony_name']

            query = """INSERT INTO pony (name) VALUES ("{NAME}") """.format(NAME = pony_name)
            cursor.execute(query)
            db.commit()

            query = """SELECT id FROM pony WHERE name = "{NAME}" """.format(NAME = pony_name)
            cursor.execute(query)
            results = cursor.fetchall()
            id = results[0][0]  # New pony's id



            return simple_response(200, "success", "Here comes pony adding")

        elif request.method == 'PUT':  # editing
            return simple_response(200, "success", "Here comes pony editing")

        elif request.method == 'DELETE':  # deleting
            return simple_response(200, "success", "Here is how pony become deleted")

    query = '''DELETE s 
               FROM spawnlist AS s 
               INNER JOIN npc AS n ON s.npc_templateid = n.idTemplate 
               WHERE n.type = "monster";'''


@app.route('/api/edit_role', methods = ['PUT'])    # Editing user roles in DB
def role_editor():

    set_role = request.args.get('role')
    mail = request.args.get('mail')
    escaped_mail = db.escape(mail)
    cookies = request.cookies
    role = role_finder(cookies)

    if role['code'] == 403:
        return simple_response(role['code'], role['description'], role['message'])

    elif role['role'] == 'user':    # Here we come if role 'user'
        return simple_response(role['code'], role['description'], "Role editing allowed only for admin's")

    elif role['email'] == escaped_mail:
        return simple_response(403, 'error', "You can't edit your own role")

    else:  # If role is 'admin'
        if request.method == 'PUT':

            query = """SELECT active
                       FROM users
                       WHERE email="{MAIL}" """.format(MAIL = escaped_mail)

            cursor.execute(query)
            results = cursor.fetchall()

            if not results:
                return simple_response(403, 'error', 'User not found')

            elif results[0][0] == 0:
                return simple_response(403, 'error', "Can't edit role of not activated users")

            elif results[0][0] == 2:
                return simple_response(403, 'error', "Can't edit role of banned users")

            elif set_role == 'admin' or set_role == 'user':

                query = """UPDATE users 
                           SET role = {ROLE}
                           WHERE email="{MAIL}" """.format(ROLE = set_role, MAIL = escaped_mail)

                cursor.execute(query)
                db.commit()
                return simple_response(200, "success", "Role edited")

            else:
                return simple_response(403, 'error', "Role %s is not allowed" %set_role)


@app.route('/api/ban', methods = ['POST', 'DELETE'])    # Banhammer: active == 2 - is 'permaban'
def ban_editor():

    mail = request.args.get('mail')
    escaped_mail = db.escape(mail)
    timestamp_input = request.args.get('unix_timestamp')
    cookies = request.cookies
    role = role_finder(cookies)

    if role['code'] == 403:
        return simple_response(role['code'], role['description'], role['message'])

    elif role['role'] == 'user':    # Here we come if role 'user'
        return simple_response(role['code'], role['description'], "Banning allowed only for admin's")

    elif role['email'] == escaped_mail:
        return simple_response(403, 'error', "You can't ban yourself")

    else:  # If role is 'admin'

        query = """SELECT ban, active
                   FROM users
                   WHERE email="{MAIL}" """.format(MAIL = escaped_mail)

        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            return simple_response(403, 'error', 'User not found')

        elif results[0][1] == 0:
            return simple_response(403, 'error', "Can't ban not activated users")

        elif results[0][0] > int(time.time()):  # If user is banned

            if request.method == 'DELETE':

                query = """UPDATE users 
                           SET ban = "", active = 1
                           WHERE email="{MAIL}" """.format(MAIL = escaped_mail)

                cursor.execute(query)
                db.commit()

                return simple_response(200, "success", "%s is unbanned" % mail)

            else:
                return simple_response(403, 'error', "Already banned")

        elif request.method == 'POST':

            try:
                timestamp = int(timestamp_input)  # Trying to get integer timestamp

                if timestamp > int(time.time()):  # If we ban until future date

                    query = """UPDATE users 
                               SET ban = {DATE_TIME}
                               WHERE email="{MAIL}" """.format(DATE_TIME = timestamp, MAIL = escaped_mail)

                    cursor.execute(query)
                    db.commit()

                    return simple_response(200, "success", "%s is banned" % mail)

                else:
                    return simple_response(403, 'error', "You can't ban until time before now")

            except ValueError:

                if timestamp_input == 'PERM':  # To ban permanently

                    query = """UPDATE user 
                               SET active = 2
                               WHERE email="{MAIL}" """.format(MAIL = escaped_mail)

                    cursor.execute(query)
                    db.commit()

                    return simple_response(200, "success", "%s is banned permanently" % mail)

                else:
                    return simple_response(403, 'error', "Timestamp should be 10 digit positive integer or 'PERM'")


@atexit.register    # Closing DB connection when app shunting down
def teardown_db():
    if db is not None:
        db.close()
        print('DATABASE CLOSED')


# Address of fun: http://localhost:5000/api/get_pony_by_color?color=053550
