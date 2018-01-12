import pymysql

def printer(table):
    for row in table:
       name        = row[0]
       body_part   = row[1]
       color_name  = row[2]
       color_value = row[3]
       # Now print fetched result
       print ("name = %s, body_part = %s, color_name = %s, color_value = %s" % \
              (name, body_part, color_name, color_value))

def pony_color_determinator(table):
    print('Enter color of pony in HEX format without "#" symbol:')
    color = input()    # Вводим цвет
    response = 'Didn`t found ponys with this color'

    for row in table:
        color_value = row[3]
        if color_value == color:
            response = 'It`s %s of %s!' %(row[1], row[0])

    print(response)

# Open database connection
db = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="00000000", database="pony_color_db", charset="utf8")    #  <=>  ("localhost","root","00000000","pony_color_db" )    # charset='utf8' - for correct encoding

# prepare a cursor object using cursor() method
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
except:
    print("Error: wrong JOIN query")

# Disconnect from server
db.close()

# Processing data from 'results' table
#printer(results)    # Если вы не знаете какие цвета есть в базе данных - раскоментируйте эту строчку.
pony_color_determinator(results)
#input()    # Если после ввода цвета все быстро закрывается - раскомментируйте эту строчку.
