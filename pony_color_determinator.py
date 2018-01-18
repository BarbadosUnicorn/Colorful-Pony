import pymysql, traceback

def printer():    # Print names, body parts, color id`s and values for each pony in database. Use only while database is connected
    # Prepare a cursor object using cursor() method
    cursor = db.cursor()
    # Prepare SQL query to Execute by MySQL server with current database connected
    join_query = """SELECT pony.name, body_part.name, color.name, color.id, color.L, color.a, color.b
                        FROM (((pony_color
                        INNER JOIN color     ON pony_color.color_id = color.id    )
                        INNER JOIN pony      ON pony_color.pony_id  = pony.id     )
                        INNER JOIN body_part ON pony_color.type_id  = body_part.id)"""
    cursor.execute(join_query)
    results = cursor.fetchall()
    for row in results:
        name        = row[0]
        body_part   = row[1]
        #color_name  = row[2]
        color_id    = row[3]
        L           = row[4]
        a           = row[5]
        b           = row[6]
        # Now print fetched result
        print ("name = %s, body_part = %s, color_id = %s, L = %s, a = %s, b = %s" % \
                                                            (name, body_part, color_id, L, a, b))

def pony_color_determinator(): # Used to work with old DB. But now it`s not, since DB don`t contain 'value' column with
                               # RGB value of color. Use only if your know what to do.
                               # Use only while database is connected
    print('Enter color of pony in HEX format with "#" symbol:')
    color = input()    # Вводим цвет
    # Prepare a cursor object using cursor() method
    cursor = db.cursor()
    q = db.escape(color)    # SQL injection protection by shielding. Jusn like this '\' thing
    # Prepare SQL query to Execute by MySQL server with current database connected
    query = """SELECT pony.name, body_part.name, color.name, color.value 
               FROM (((pony_color
               INNER JOIN color     ON pony_color.color_id = color.id    )
               INNER JOIN pony      ON pony_color.pony_id  = pony.id     )
               INNER JOIN body_part ON pony_color.type_id  = body_part.id)
               WHERE value={}""".format(q)    # Some replacement for %s statement...
    try:
        # Execute the query
        cursor.execute(query)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()

        if len(results) > 0:

            for row in results:
                name        = row[0]
                body_part   = row[1]
                #color_name  = row[2]
                #color_value = row[3]
                # Now print fetched result
                print ('It`s %s of %s!' %(body_part, name))
        else:
            print('Didn`t found ponys with this color')

    except:
        print("Error: wrong JOIN query")

def RGBtoLab(color):    # Converter from RGB to CIE Lab. Reference white used D65/2° standard illuminant

    try:  # Making R, G and B variables from input string
        rgb = str(color).rstrip()
        R16 = rgb[len(rgb) - 6:len(rgb) - 4]
        G16 = rgb[len(rgb) - 4:len(rgb) - 2]
        B16 = rgb[len(rgb) - 2:]

        # RGB to XYZ
        r = int(R16, 16) / 255
        g = int(G16, 16) / 255
        b = int(B16, 16) / 255

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

    except:
        print('Wrong input')
        raise SystemExit

def migration():    # Since migration completed it`s just an example of migration scrypt.
                    # Use only while database is connected

    cursor = db.cursor()

    alter_query_L = 'ALTER TABLE color ADD L DOUBLE;'
    alter_query_a = 'ALTER TABLE color ADD a DOUBLE;'
    alter_query_b = 'ALTER TABLE color ADD b DOUBLE;'
    select_query = 'SELECT * FROM color;'

    try:
        cursor.execute(alter_query_L)
        cursor.execute(alter_query_a)
        cursor.execute(alter_query_b)
        cursor.execute(select_query)
        results = cursor.fetchall()

        for row in results:
            id    = row[0]
            #name  = row[1]
            value = row[2]
            #L     = row[3]
            #a     = row[4]
            #b     = row[5]
            Lab_color = RGBtoLab(value)
            update_query = '''UPDATE color
                              SET L = %s, a = %s, b = %s
                              WHERE id = %s;''' % \
                                                (str(Lab_color['L']), str(Lab_color['a']), str(Lab_color['b']), str(id))
            cursor.execute(update_query)

        cursor.execute('''ALTER TABLE color
                          DROP COLUMN value;''')

    except:
        traceback.print_exc()

def closest_color_determinator(): # Function to find closest color in database. Use only while database is connected
    print('Enter color of pony in HEX format with "#" symbol:')
    color = input()
    color = RGBtoLab(color)    # Вводим цвет
    # Prepare a cursor object using cursor() method
    cursor = db.cursor()
    # Prepare SQL query to Execute by MySQL server with current database connected

    '''
    query = """SELECT MIN((L - {L})*(L - {L})+(a - {a})*(a - {a})+(b - {b})*(b - {b}))
               FROM color""".format(L = color['L'], a = color['a'], b = color['b'])
    cursor.execute(query)
    print('radius =', cursor.fetchall()[0][0]) # This thing is able to find the smallest radius. Only radius
    '''

    query = """SELECT color.id, color.name, pony.name, body_part.name
               FROM pony_color
               INNER JOIN color     ON pony_color.color_id = color.id
               INNER JOIN pony      ON pony_color.pony_id  = pony.id
               INNER JOIN body_part ON pony_color.type_id  = body_part.id
               GROUP BY color.id, pony.id, body_part.id
               ORDER BY MIN((L - {L})*(L - {L})+(a - {a})*(a - {a})+(b - {b})*(b - {b})) LIMIT 1""".format(L = color['L'], a = color['a'], b = color['b'])

    cursor.execute(query)
    results = cursor.fetchall()

    for row in results:

        color_id    = row[0]
        color_name  = row[1]
        name        = row[2]
        body_part   = row[3]
        # Now print fetched result
        print ("It`s %s of %s!" %(body_part, name))

# Open database connection
db = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="password",\
                     database="pony_color_db", charset="utf8")    # charset='utf8' - for correct encoding

# Processing data from 'results' table
closest_color_determinator()
#input()    # If you run console - uncomment this to see result before it closes. Simply press Enter button to close it

# Disconnect from server
db.close()
