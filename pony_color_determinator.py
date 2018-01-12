import pymysql

def printer():    # Use only while database is connected
    # Prepare a cursor object using cursor() method
    cursor = db.cursor()
    # Prepare SQL query to Execute by MySQL server with current database connected
    join_query = """SELECT pony.name, body_part.name, color.name, color.value 
                FROM (((pony_color
                INNER JOIN color     ON pony_color.color_id = color.id    )
                INNER JOIN pony      ON pony_color.pony_id  = pony.id     )
                INNER JOIN body_part ON pony_color.type_id  = body_part.id);"""

    try:
        # Execute the JOIN command
        cursor.execute(join_query)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()

        for row in results:
            name        = row[0]
            body_part   = row[1]
            color_name  = row[2]
            color_value = row[3]
            # Now print fetched result
            print ("name = %s, body_part = %s, color_name = %s, color_value = %s" % \
                                                            (name, body_part, color_name, color_value))
    except:
        print("Error: wrong JOIN query")

def pony_color_determinator():
    print('Enter color of pony in HEX format without "#" symbol:')
    color = input()    # Вводим цвет
    # Prepare a cursor object using cursor() method
    cursor = db.cursor()
    # Prepare SQL query to Execute by MySQL server with current database connected
    query = """SELECT pony.name, body_part.name, color.name, color.value 
               FROM (((pony_color
               INNER JOIN color     ON pony_color.color_id = color.id    )
               INNER JOIN pony      ON pony_color.pony_id  = pony.id     )
               INNER JOIN body_part ON pony_color.type_id  = body_part.id)
               WHERE value='%s';""" %color

    try:
        # Execute the query
        cursor.execute(query)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()

        if len(results) > 0:

            for row in results:
                name        = row[0]
                body_part   = row[1]
                color_name  = row[2]
                color_value = row[3]
                # Now print fetched result
                print ('It`s %s of %s!' %(row[1], row[0]))
        else:
            print('Didn`t found ponys with this color')

    except:
        print("Error: wrong JOIN query")



# Open database connection
db = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="password", database="pony_color_db", charset="utf8")    # charset='utf8' - for correct encoding

# Processing data from 'results' table
#printer()    # Если вы не знаете какие цвета есть в базе данных - раскоментируйте эту строчку.
pony_color_determinator()
#input()    # Если после ввода цвета все быстро закрывается - раскомментируйте эту строчку.

# Disconnect from server
db.close()


