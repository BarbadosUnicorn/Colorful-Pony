import pymysql, traceback
from pony_color_determinator import RGBtoLab

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

db = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="password",\
                     database="pony_color_db", charset="utf8")    # charset='utf8' - for correct encoding

migration()

db.close()

'''
    query = """SELECT MIN((L - {L})*(L - {L})+(a - {a})*(a - {a})+(b - {b})*(b - {b}))
               FROM color""".format(L = color['L'], a = color['a'], b = color['b'])
    cursor.execute(query)
    print('radius =', cursor.fetchall()[0][0]) # This thing is able to find the smallest radius. Only radius
'''
